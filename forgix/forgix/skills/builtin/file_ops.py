"""
Forgix file_ops skill — sandboxed file read/write.

All operations are confined to a sandbox directory (~/.forgix/workspace by default).
Path jail prevents escaping via '..' or absolute paths.
"""
from __future__ import annotations

from pathlib import Path

from forgix.modules.base import tool_schema

SANDBOX = Path.home() / ".forgix" / "workspace"


def _safe_path(filename: str) -> Path:
    """Resolve a path within the sandbox. Raises ValueError on escape attempts."""
    SANDBOX.mkdir(parents=True, exist_ok=True)
    target = (SANDBOX / filename).resolve()
    if not str(target).startswith(str(SANDBOX.resolve())):
        raise ValueError(f"Path escapes sandbox: {filename}")
    return target


@tool_schema(
    "skill.read_file",
    "Read a file from the Forgix workspace sandbox.",
    {"filename": {"type": "string", "description": "Path relative to workspace"}},
    required=["filename"],
)
async def read_file(filename: str) -> str:
    """Read a file from the sandbox."""
    try:
        path = _safe_path(filename)
        if not path.exists():
            return f"[File not found: {filename}]"
        return path.read_text(encoding="utf-8", errors="replace")[:8000]
    except ValueError as e:
        return f"[Security: {e}]"
    except OSError as e:
        return f"[File error: {e}]"


@tool_schema(
    "skill.write_file",
    "Write content to a file in the Forgix workspace sandbox.",
    {"filename": {"type": "string"}, "content": {"type": "string"},
     "append": {"type": "boolean", "description": "Append instead of overwrite"}},
    required=["filename", "content"],
)
async def write_file(filename: str, content: str, append: bool = False) -> str:
    """Write a file in the sandbox."""
    try:
        path = _safe_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        if append:
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
        else:
            path.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} chars to {filename}"
    except ValueError as e:
        return f"[Security: {e}]"
    except OSError as e:
        return f"[File error: {e}]"


@tool_schema(
    "skill.list_dir",
    "List files in the Forgix workspace sandbox.",
    {"subdir": {"type": "string", "description": "Subdirectory (optional)"}},
    required=[],
)
async def list_dir(subdir: str = "") -> str:
    """List files in the sandbox."""
    try:
        base = _safe_path(subdir) if subdir else SANDBOX
        SANDBOX.mkdir(parents=True, exist_ok=True)
        if not base.exists():
            return f"[Directory not found: {subdir}]"
        entries = sorted(base.iterdir())
        if not entries:
            return "(empty)"
        return "\n".join(
            f"{'[dir] ' if e.is_dir() else '      '}{e.relative_to(SANDBOX)}"
            for e in entries
        )
    except ValueError as e:
        return f"[Security: {e}]"
    except OSError as e:
        return f"[File error: {e}]"
