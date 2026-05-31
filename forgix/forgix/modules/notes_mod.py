"""
Forgix Notes module — Obsidian / markdown files.
Permissions: read_files, write_files
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from forgix.modules.base import BaseModule, ModuleManifest, tool_schema


class NotesModule(BaseModule):
    manifest = ModuleManifest(
        name="notes",
        version="0.1.0",
        description="Read and write markdown notes (Obsidian vault or any markdown directory)",
        required_permissions=["read_files", "write_files"],
    )

    def __init__(self):
        vault_path = self._get_secret("module_notes_notes_vault_path") or ""
        self._vault = Path(vault_path).expanduser() if vault_path else None

    def get_tools(self) -> dict[str, Callable]:
        return {
            "notes.list": self.list_notes,
            "notes.read": self.read_note,
            "notes.write": self.write_note,
            "notes.search": self.search_notes,
        }

    def _check_vault(self) -> str | None:
        if not self._vault or not self._vault.exists():
            return "[Notes vault not configured or not found. Run: forgix modules configure notes]"
        return None

    def _safe_path(self, filename: str) -> Path:
        """Ensure the path stays within the vault (path jail)."""
        target = (self._vault / filename).resolve()
        if not str(target).startswith(str(self._vault.resolve())):
            raise ValueError(f"Path escapes vault: {filename}")
        return target

    @tool_schema("notes.list", "List notes in the vault",
        {"subdir": {"type": "string", "description": "Subdirectory to list (optional)"}},
        required=[])
    async def list_notes(self, subdir: str = "") -> str:
        err = self._check_vault()
        if err:
            return err
        base = self._safe_path(subdir) if subdir else self._vault
        files = sorted(base.rglob("*.md"))
        return "\n".join(str(f.relative_to(self._vault)) for f in files[:50]) or "No notes found."

    @tool_schema("notes.read", "Read a note by filename",
        {"filename": {"type": "string", "description": "Path relative to vault root"}},
        required=["filename"])
    async def read_note(self, filename: str) -> str:
        err = self._check_vault()
        if err:
            return err
        try:
            path = self._safe_path(filename)
            return path.read_text(encoding="utf-8")[:6000]
        except (ValueError, FileNotFoundError) as e:
            return f"[Notes error: {e}]"

    @tool_schema("notes.write", "Write or append to a note",
        {"filename": {"type": "string"}, "content": {"type": "string"}, "append": {"type": "boolean"}},
        required=["filename", "content"])
    async def write_note(self, filename: str, content: str, append: bool = False) -> str:
        err = self._check_vault()
        if err:
            return err
        try:
            path = self._safe_path(filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            if append:
                with open(path, "a", encoding="utf-8") as f:
                    f.write("\n" + content)
            else:
                path.write_text(content, encoding="utf-8")
            return f"Note {'appended' if append else 'written'}: {filename}"
        except (ValueError, OSError) as e:
            return f"[Notes error: {e}]"

    @tool_schema("notes.search", "Search notes for a keyword",
        {"query": {"type": "string"}},
        required=["query"])
    async def search_notes(self, query: str) -> str:
        err = self._check_vault()
        if err:
            return err
        results = []
        q = query.lower()
        for f in self._vault.rglob("*.md"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                if q in text.lower():
                    lines = [l for l in text.splitlines() if q in l.lower()][:3]
                    results.append(f"{f.relative_to(self._vault)}:\n  " + "\n  ".join(lines))
            except Exception:
                pass
            if len(results) >= 10:
                break
        return "\n\n".join(results) or f"No notes found containing '{query}'."
