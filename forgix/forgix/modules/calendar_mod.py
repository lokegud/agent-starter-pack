"""
Forgix Calendar module — Google Calendar / iCal.
Permissions: read_calendar, write_calendar
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from forgix.modules.base import BaseModule, ModuleManifest, tool_schema


class CalendarModule(BaseModule):
    manifest = ModuleManifest(
        name="calendar",
        version="0.1.0",
        description="Google Calendar integration — list and create events",
        required_permissions=["read_calendar", "write_calendar", "network"],
    )

    def get_tools(self) -> dict[str, Callable]:
        return {
            "calendar.list_events": self.list_events,
            "calendar.create_event": self.create_event,
        }

    @tool_schema("calendar.list_events", "List upcoming calendar events",
        {"days_ahead": {"type": "integer", "description": "How many days ahead to look (default 7)"}},
        required=[])
    async def list_events(self, days_ahead: int = 7) -> str:
        import httpx
        from datetime import timedelta
        client_id = self._get_secret("module_calendar_google_client_id")
        if not client_id:
            return "[Calendar not configured. Run: forgix modules configure calendar]"
        # Note: Full OAuth flow requires user setup — placeholder for token-based access
        return "[Calendar: full OAuth2 flow required. Configure via forgix modules configure calendar]"

    @tool_schema("calendar.create_event", "Create a calendar event",
        {"title": {"type": "string"}, "start": {"type": "string", "description": "ISO datetime"},
         "end": {"type": "string"}, "description": {"type": "string"}},
        required=["title", "start", "end"])
    async def create_event(self, title: str, start: str, end: str, description: str = "") -> str:
        client_id = self._get_secret("module_calendar_google_client_id")
        if not client_id:
            return "[Calendar not configured. Run: forgix modules configure calendar]"
        return "[Calendar: full OAuth2 flow required. Configure via forgix modules configure calendar]"
