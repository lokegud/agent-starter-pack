"""
Forgix Slack module — Slack Web API.
Permissions: read_slack, write_slack
"""
from __future__ import annotations

from typing import Callable

import httpx

from forgix.modules.base import BaseModule, ModuleManifest, tool_schema


class SlackModule(BaseModule):
    manifest = ModuleManifest(
        name="slack",
        version="0.1.0",
        description="Slack Web API — read channels, send messages",
        required_permissions=["read_slack", "write_slack", "network"],
    )

    def __init__(self):
        token = self._get_secret("module_slack_slack_bot_token") or ""
        self._headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"} if token else {}
        self._base = "https://slack.com/api"

    def get_tools(self) -> dict[str, Callable]:
        return {
            "slack.list_channels": self.list_channels,
            "slack.read_channel": self.read_channel,
            "slack.send_message": self.send_message,
        }

    @tool_schema("slack.list_channels", "List Slack channels", {}, required=[])
    async def list_channels(self) -> str:
        if not self._headers:
            return "[Slack not configured. Run: forgix modules configure slack]"
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{self._base}/conversations.list", params={"limit": 20}, headers=self._headers)
            r.raise_for_status()
            data = r.json()
        if not data.get("ok"):
            return f"[Slack error: {data.get('error')}]"
        return "\n".join(f"#{ch['name']} ({ch.get('num_members', 0)} members)" for ch in data.get("channels", []))

    @tool_schema("slack.read_channel", "Read recent messages from a Slack channel",
        {"channel": {"type": "string", "description": "Channel name or ID"},
         "limit": {"type": "integer"}},
        required=["channel"])
    async def read_channel(self, channel: str, limit: int = 10) -> str:
        if not self._headers:
            return "[Slack not configured]"
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{self._base}/conversations.history",
                params={"channel": channel, "limit": limit}, headers=self._headers)
            r.raise_for_status()
            data = r.json()
        if not data.get("ok"):
            return f"[Slack error: {data.get('error')}]"
        msgs = data.get("messages", [])
        return "\n".join(f"{m.get('user', '?')}: {m.get('text', '')}" for m in reversed(msgs)) or "No messages."

    @tool_schema("slack.send_message", "Send a message to a Slack channel",
        {"channel": {"type": "string"}, "text": {"type": "string"}},
        required=["channel", "text"])
    async def send_message(self, channel: str, text: str) -> str:
        if not self._headers:
            return "[Slack not configured]"
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.post(f"{self._base}/chat.postMessage",
                json={"channel": channel, "text": text}, headers=self._headers)
            r.raise_for_status()
            data = r.json()
        return "Message sent." if data.get("ok") else f"[Slack error: {data.get('error')}]"
