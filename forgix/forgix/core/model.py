"""
Forgix inference backend abstraction.

Supports:
- OllamaBackend       : desktop (macOS/Linux/Windows)
- LlamaCppBackend     : Android/Termux via llama.cpp server subprocess
- OpenAICompatBackend : any OpenAI-compatible HTTP endpoint

auto_detect_backend(config) picks the right one automatically.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, AsyncIterator

import httpx

log = logging.getLogger(__name__)
FORGIX_DIR = Path.home() / ".forgix"


class InferenceBackend(ABC):
    base_url: str
    model_name: str

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        stream: bool = True,
    ) -> AsyncIterator[dict]: ...

    @abstractmethod
    async def is_available(self) -> bool: ...


class OllamaBackend(InferenceBackend):
    """Ollama HTTP API (desktop)."""

    def __init__(self, model_name: str = "gemma4:2b", base_url: str = "http://127.0.0.1:11434"):
        self.model_name = model_name
        self.base_url = base_url

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                r = await c.get(f"{self.base_url}/api/tags")
                return r.status_code == 200
        except Exception:
            return False

    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        stream: bool = True,
    ) -> AsyncIterator[dict]:
        payload: dict[str, Any] = {"model": self.model_name, "messages": messages, "stream": stream}
        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=120.0) as c:
            if stream:
                async with c.stream("POST", f"{self.base_url}/api/chat", json=payload) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line.strip():
                            continue
                        chunk = json.loads(line)
                        msg = chunk.get("message", {})
                        if msg.get("tool_calls"):
                            for tc in msg["tool_calls"]:
                                yield {"type": "tool_call", "name": tc["function"]["name"], "arguments": tc["function"].get("arguments", {})}
                        elif msg.get("content"):
                            yield {"type": "text", "content": msg["content"]}
                        if chunk.get("done"):
                            yield {"type": "done"}
                            return
            else:
                resp = await c.post(f"{self.base_url}/api/chat", json=payload)
                resp.raise_for_status()
                msg = resp.json().get("message", {})
                if msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        yield {"type": "tool_call", "name": tc["function"]["name"], "arguments": tc["function"].get("arguments", {})}
                elif msg.get("content"):
                    yield {"type": "text", "content": msg["content"]}
                yield {"type": "done"}


class LlamaCppBackend(InferenceBackend):
    """
    llama.cpp server backend for Android/Termux.
    Starts llama-server as a subprocess exposing OpenAI-compat API on 127.0.0.1:11434.
    """

    def __init__(self, gguf_path: str, model_name: str = "gemma4-e2b", base_url: str = "http://127.0.0.1:11434"):
        self.gguf_path = gguf_path
        self.model_name = model_name
        self.base_url = base_url
        self._proc: subprocess.Popen | None = None

    def _start_server(self) -> None:
        if self._proc and self._proc.poll() is None:
            return
        import shutil
        server_bin = shutil.which("llama-server")
        n_threads = str(max(2, os.cpu_count() or 4))
        if server_bin:
            cmd = [server_bin, "--model", self.gguf_path, "--host", "127.0.0.1", "--port", "11434", "--ctx-size", "8192", "--threads", n_threads]
        else:
            cmd = [sys.executable, "-m", "llama_cpp.server", "--model", self.gguf_path, "--host", "127.0.0.1", "--port", "11434", "--n_ctx", "8192"]
        self._proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(30):
            time.sleep(1)
            try:
                import urllib.request
                urllib.request.urlopen("http://127.0.0.1:11434/health", timeout=2)
                log.info("llama.cpp server ready")
                return
            except Exception:
                pass
        raise RuntimeError("llama.cpp server failed to start within 30s")

    async def is_available(self) -> bool:
        try:
            self._start_server()
            async with httpx.AsyncClient(timeout=5.0) as c:
                return (await c.get(f"{self.base_url}/health")).status_code == 200
        except Exception:
            return False

    async def chat(self, messages, tools=None, stream=True) -> AsyncIterator[dict]:
        self._start_server()
        async for chunk in OpenAICompatBackend(self.model_name, self.base_url).chat(messages, tools=tools, stream=stream):
            yield chunk


class OpenAICompatBackend(InferenceBackend):
    """
    Generic OpenAI-compatible HTTP backend.
    Works with: llama.cpp server, remote Ollama, LM Studio, iOS bridge app, etc.
    """

    def __init__(self, model_name: str, base_url: str, api_key: str = "forgix"):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                r = await c.get(f"{self.base_url}/v1/models", headers={"Authorization": f"Bearer {self.api_key}"})
                return r.status_code in (200, 401)
        except Exception:
            return False

    async def chat(self, messages, tools=None, stream=True) -> AsyncIterator[dict]:
        payload: dict[str, Any] = {"model": self.model_name, "messages": messages, "stream": stream}
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=120.0) as c:
            if stream:
                async with c.stream("POST", f"{self.base_url}/v1/chat/completions", json=payload, headers=headers) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            yield {"type": "done"}
                            return
                        chunk = json.loads(data_str)
                        choice = chunk.get("choices", [{}])[0]
                        delta = choice.get("delta", {})
                        if delta.get("tool_calls"):
                            for tc in delta["tool_calls"]:
                                fn = tc.get("function", {})
                                args = fn.get("arguments", "{}")
                                if isinstance(args, str):
                                    try:
                                        args = json.loads(args)
                                    except json.JSONDecodeError:
                                        args = {}
                                yield {"type": "tool_call", "name": fn.get("name", ""), "arguments": args}
                        elif delta.get("content"):
                            yield {"type": "text", "content": delta["content"]}
                        if choice.get("finish_reason") == "stop":
                            yield {"type": "done"}
                            return
            else:
                resp = await c.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                choice = resp.json().get("choices", [{}])[0]
                msg = choice.get("message", {})
                if msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        fn = tc.get("function", {})
                        args = fn.get("arguments", "{}")
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except json.JSONDecodeError:
                                args = {}
                        yield {"type": "tool_call", "name": fn.get("name", ""), "arguments": args}
                elif msg.get("content"):
                    yield {"type": "text", "content": msg["content"]}
                yield {"type": "done"}


def auto_detect_backend(config: dict) -> InferenceBackend:
    """
    Auto-detect the appropriate inference backend.

    Order: Android/Termux → explicit custom_endpoint → Ollama (default).
    """
    backend_type = config.get("backend", "")
    variant = config.get("model_variant", "e2b")
    model_tag = config.get("model_tag", "")

    prefix = os.environ.get("PREFIX", "")
    is_termux = "com.termux" in prefix or os.path.exists("/data/data/com.termux")

    if backend_type == "llamacpp" or is_termux:
        gguf_path = config.get("gguf_path") or str(FORGIX_DIR / "models" / f"gemma-4-{variant}-it-q4_k_m.gguf")
        return LlamaCppBackend(gguf_path=gguf_path, model_name=f"gemma4-{variant}")

    custom = config.get("custom_endpoint")
    if custom:
        return OpenAICompatBackend(model_name=model_tag or f"gemma4:{variant[-2:]}", base_url=custom)

    return OllamaBackend(model_name=model_tag or ("gemma4:2b" if variant == "e2b" else "gemma4:4b"))
