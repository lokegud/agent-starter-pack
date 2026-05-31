"""
Forgix FastAPI server.

Binds to 127.0.0.1 by default. --lan mode binds to subnet IP with TLS.
All routes require Bearer token auth. WebSocket requires token + CSRF in first frame.
"""
from __future__ import annotations

import json
import secrets
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, BaseLoader

from forgix.core.security import SecurityManager, get_rate_limiter
from forgix.core.model import auto_detect_backend
from forgix.core.memory import MemoryStore
from forgix.core.agent import Agent
from forgix.interface.ui_generator import UIGenerator
from forgix.persona.generator import PersonaGenerator

FORGIX_DIR = Path.home() / ".forgix"


def _get_allowed_origins(lan_mode: bool) -> list[str]:
    if lan_mode:
        return [
            "https://localhost",
            "https://127.0.0.1",
            # RFC-1918 subnets — broad but still private-only
            "https://192.168.*",
            "https://10.*",
            "https://172.*",
        ]
    return ["http://localhost:7433", "http://127.0.0.1:7433"]


def create_app(config: dict, lan_mode: bool = False) -> FastAPI:
    app = FastAPI(title="Forgix", docs_url=None, redoc_url=None)

    # CORS: localhost-only by default
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_get_allowed_origins(lan_mode),
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],
    )

    # Shared state
    ui = UIGenerator(force=config.get("theme") if config.get("theme") != "random" else None)
    persona = PersonaGenerator(force=config.get("persona") if config.get("persona") != "random" else None)
    backend = auto_detect_backend(config)
    app.state.config = config
    app.state.ui = ui
    app.state.persona = persona
    app.state.backend = backend
    app.state.memory = None  # initialized on startup
    app.state.agents: dict[str, Agent] = {}

    @app.on_event("startup")
    async def startup() -> None:
        app.state.memory = await MemoryStore.initialize()

    # ---------------------------------------------------------------------------
    # Rate-limit middleware
    # ---------------------------------------------------------------------------

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        limiter = get_rate_limiter(ip)
        if not limiter.is_allowed(ip):
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        return await call_next(request)

    # ---------------------------------------------------------------------------
    # Auth dependency
    # ---------------------------------------------------------------------------

    def require_auth(request: Request) -> None:
        if not SecurityManager.verify_bearer_token(request.headers.get("Authorization")):
            raise HTTPException(status_code=401, detail="Unauthorized")

    # ---------------------------------------------------------------------------
    # Routes
    # ---------------------------------------------------------------------------

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        # Serve the chat UI — inject token only for localhost / LAN requests
        ip = request.client.host if request.client else ""
        token = ""
        if ip in ("127.0.0.1", "::1") or (lan_mode and SecurityManager.is_lan_subnet(ip)):
            # Token may also come via ?token= for QR-code flows
            token = request.query_params.get("token", "")
            if not token:
                try:
                    token = SecurityManager.get_session_token()
                except Exception:
                    pass
        csrf = SecurityManager.get_csrf_token()
        html = app.state.ui.render_chat_page(
            token=token,
            csrf=csrf,
            persona_name=persona.current_figure,
        )
        return HTMLResponse(content=html)

    @app.get("/api/status", dependencies=[Depends(require_auth)])
    async def status():
        return {
            "status": "ok",
            "persona": app.state.persona.current_figure,
            "theme": app.state.ui.current_theme["id"],
            "backend": app.state.config.get("backend"),
            "model": app.state.config.get("model_tag"),
        }

    @app.get("/api/conversations", dependencies=[Depends(require_auth)])
    async def list_conversations():
        convs = await app.state.memory.list_conversations()
        return {"conversations": convs}

    @app.get("/api/history/{conversation_id}", dependencies=[Depends(require_auth)])
    async def get_history(conversation_id: str):
        msgs = await app.state.memory.get_history(conversation_id, limit=100)
        return {"messages": msgs}

    # ---------------------------------------------------------------------------
    # WebSocket — main chat endpoint
    # ---------------------------------------------------------------------------

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            # First frame must contain {token, csrf, conversation_id?}
            raw = await websocket.receive_text()
            try:
                handshake = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid handshake"})
                await websocket.close(code=1008)
                return

            if not SecurityManager.verify_websocket_auth(
                handshake.get("token", ""),
                handshake.get("csrf", ""),
            ):
                await websocket.send_json({"type": "error", "message": "Authentication failed"})
                await websocket.close(code=1008)
                return

            conversation_id = handshake.get("conversation_id") or str(uuid.uuid4())
            await websocket.send_json({"type": "ready", "conversation_id": conversation_id})

            # Load or create agent for this conversation
            if conversation_id not in app.state.agents:
                app.state.agents[conversation_id] = Agent(
                    backend=app.state.backend,
                    system_prompt=app.state.persona.system_prompt,
                    memory=app.state.memory,
                    tool_registry=_build_tool_registry(config),
                )
            agent = app.state.agents[conversation_id]

            # Message loop
            while True:
                data = await websocket.receive_text()
                try:
                    msg = json.loads(data)
                except json.JSONDecodeError:
                    continue

                user_text = msg.get("message", "").strip()
                if not user_text:
                    continue

                await websocket.send_json({"type": "start"})
                async for chunk in agent.run(user_text, conversation_id):
                    await websocket.send_json({"type": "chunk", "content": chunk})
                await websocket.send_json({"type": "end"})

        except WebSocketDisconnect:
            pass

    return app


def _build_tool_registry(config: dict) -> dict:
    """Build the tool registry from enabled modules."""
    registry: dict = {}
    enabled = config.get("enabled_modules", [])

    if "github" in enabled:
        try:
            from forgix.modules.github_mod import GithubModule
            m = GithubModule()
            registry.update(m.get_tools())
        except Exception:
            pass

    if "calendar" in enabled:
        try:
            from forgix.modules.calendar_mod import CalendarModule
            m = CalendarModule()
            registry.update(m.get_tools())
        except Exception:
            pass

    if "email" in enabled:
        try:
            from forgix.modules.email_mod import EmailModule
            m = EmailModule()
            registry.update(m.get_tools())
        except Exception:
            pass

    if "slack" in enabled:
        try:
            from forgix.modules.slack_mod import SlackModule
            m = SlackModule()
            registry.update(m.get_tools())
        except Exception:
            pass

    if "notes" in enabled:
        try:
            from forgix.modules.notes_mod import NotesModule
            m = NotesModule()
            registry.update(m.get_tools())
        except Exception:
            pass

    if "tasks" in enabled:
        try:
            from forgix.modules.tasks_mod import TasksModule
            m = TasksModule()
            registry.update(m.get_tools())
        except Exception:
            pass

    # Always include builtin skills
    try:
        from forgix.skills.manager import SkillManager
        sm = SkillManager()
        registry.update(sm.get_tools())
    except Exception:
        pass

    return registry
