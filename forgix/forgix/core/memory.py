"""
Forgix memory — encrypted SQLite.

Tables: conversations (message history), audit_log (every tool call).
All content is Fernet-encrypted at rest. The key lives in the OS keychain only.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import aiosqlite
from cryptography.fernet import Fernet

log = logging.getLogger(__name__)

FORGIX_DIR = Path.home() / ".forgix"
DB_PATH = FORGIX_DIR / "memory.db"


def _get_fernet() -> Fernet:
    import keyring
    key = keyring.get_password("forgix", "db_fernet_key")
    if not key:
        raise RuntimeError("DB key not found — run 'forgix setup'")
    return Fernet(key.encode())


def _enc(data: str) -> str:
    return _get_fernet().encrypt(data.encode()).decode()


def _dec(data: str) -> str:
    return _get_fernet().decrypt(data.encode()).decode()


class MemoryStore:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    @classmethod
    async def initialize(cls, db_path: Path = DB_PATH) -> "MemoryStore":
        db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(str(db_path)) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content_enc TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            await db.execute("CREATE INDEX IF NOT EXISTS idx_conv ON conversations (conversation_id, created_at)")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_enc TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            await db.commit()
        log.info("MemoryStore ready at %s", db_path)
        return cls(db_path)

    async def add_message(self, conversation_id: str, role: str, content: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        async with aiosqlite.connect(str(self.db_path)) as db:
            await db.execute(
                "INSERT INTO conversations (conversation_id, role, content_enc, created_at) VALUES (?, ?, ?, ?)",
                (conversation_id, role, _enc(content), now),
            )
            await db.commit()

    async def get_history(self, conversation_id: str, limit: int = 40) -> list[dict]:
        async with aiosqlite.connect(str(self.db_path)) as db:
            async with db.execute(
                "SELECT role, content_enc FROM conversations WHERE conversation_id=? ORDER BY created_at DESC LIMIT ?",
                (conversation_id, limit),
            ) as cur:
                rows = await cur.fetchall()
        messages = []
        for role, enc in reversed(rows):
            try:
                content = _dec(enc)
            except Exception:
                content = "[decryption error]"
            messages.append({"role": role, "content": content})
        return messages

    async def log_audit(self, event: str, details: dict | None = None) -> None:
        payload = json.dumps({"event": event, "details": details or {}, "ts": datetime.now(timezone.utc).isoformat()})
        now = datetime.now(timezone.utc).isoformat()
        async with aiosqlite.connect(str(self.db_path)) as db:
            await db.execute("INSERT INTO audit_log (event_enc, created_at) VALUES (?, ?)", (_enc(payload), now))
            await db.commit()

    async def get_audit_log(self, limit: int = 100) -> list[dict]:
        async with aiosqlite.connect(str(self.db_path)) as db:
            async with db.execute(
                "SELECT event_enc, created_at FROM audit_log ORDER BY created_at DESC LIMIT ?", (limit,)
            ) as cur:
                rows = await cur.fetchall()
        entries = []
        for enc, ts in rows:
            try:
                entries.append(json.loads(_dec(enc)))
            except Exception:
                entries.append({"event": "[decryption error]", "ts": ts})
        return entries

    async def list_conversations(self) -> list[str]:
        async with aiosqlite.connect(str(self.db_path)) as db:
            async with db.execute(
                "SELECT conversation_id, MIN(created_at) AS first_seen "
                "FROM conversations GROUP BY conversation_id ORDER BY first_seen DESC"
            ) as cur:
                rows = await cur.fetchall()
        return [r[0] for r in rows]
