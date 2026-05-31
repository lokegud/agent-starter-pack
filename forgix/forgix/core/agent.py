"""
Forgix agent — ReAct (Reason + Act) tool-use loop.

Flow: user message → PromptGuard → build context → backend.chat
      → dispatch tool calls (max 8 iter) → stream text → persist
"""
from __future__ import annotations

import json
import logging
from typing import Any, AsyncIterator

from forgix.core.model import InferenceBackend
from forgix.core.memory import MemoryStore
from forgix.core.prompt_guard import scan as guard_scan, RiskLevel, wrap_external

log = logging.getLogger(__name__)

MAX_TOOL_ITERATIONS = 8
HISTORY_WINDOW = 40


class Agent:
    def __init__(
        self,
        backend: InferenceBackend,
        system_prompt: str,
        memory: MemoryStore,
        tool_registry: dict[str, Any],
    ):
        self.backend = backend
        self.system_prompt = system_prompt
        self.memory = memory
        self.tool_registry = tool_registry

    async def run(self, user_message: str, conversation_id: str) -> AsyncIterator[str]:
        """Process a user message. Yields text chunks for WebSocket streaming."""
        # Guard user input
        result = guard_scan(user_message)
        if result.risk_level == RiskLevel.BLOCKED:
            log.warning("User message blocked: %s", result.matched_patterns)
            yield "[SECURITY] Message blocked: potential prompt injection detected."
            await self.memory.log_audit("prompt_injection_blocked", {"patterns": result.matched_patterns})
            return

        await self.memory.add_message(conversation_id, "user", user_message)
        history = await self.memory.get_history(conversation_id, limit=HISTORY_WINDOW)
        messages = [{"role": "system", "content": self.system_prompt}] + history
        tool_defs = self._build_tool_defs()
        full_response = ""
        iterations = 0

        while iterations < MAX_TOOL_ITERATIONS:
            iterations += 1
            tool_called = False

            async for chunk in self.backend.chat(messages, tools=tool_defs, stream=True):
                if chunk["type"] == "text":
                    full_response += chunk["content"]
                    yield chunk["content"]

                elif chunk["type"] == "tool_call":
                    tool_called = True
                    name, args = chunk["name"], chunk["arguments"]
                    log.info("Tool call: %s(%s)", name, args)
                    await self.memory.log_audit("tool_call", {"tool": name, "args": _redact(args)})

                    raw_result = await self._dispatch(name, args)
                    guarded = wrap_external(raw_result, source=name)

                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{"type": "function", "function": {"name": name, "arguments": json.dumps(args)}}],
                    })
                    messages.append({"role": "tool", "name": name, "content": guarded})

                elif chunk["type"] == "done":
                    break

            if not tool_called:
                break

        if full_response:
            await self.memory.add_message(conversation_id, "assistant", full_response)

    async def _dispatch(self, name: str, args: dict) -> str:
        handler = self.tool_registry.get(name)
        if not handler:
            return f"[Error: unknown tool '{name}']"
        try:
            result = await handler(**args)
            return str(result) if result is not None else ""
        except Exception as e:
            # Retry with no args on argument mismatch
            try:
                result = await handler()
                return str(result) if result is not None else ""
            except Exception:
                log.error("Tool %s raised: %s", name, e)
                return f"[Error calling {name}: {e}]"

    def _build_tool_defs(self) -> list[dict]:
        defs = []
        for full_name, handler in self.tool_registry.items():
            schema = getattr(handler, "_forgix_schema", None)
            if schema:
                defs.append(schema)
            else:
                defs.append({
                    "type": "function",
                    "function": {
                        "name": full_name,
                        "description": (handler.__doc__ or "").strip().split("\n")[0],
                        "parameters": {"type": "object", "properties": {}},
                    },
                })
        return defs


def _redact(args: dict) -> dict:
    SENSITIVE = {"password", "token", "key", "secret", "credential", "auth"}
    return {k: "***" if any(s in k.lower() for s in SENSITIVE) else v for k, v in args.items()}
