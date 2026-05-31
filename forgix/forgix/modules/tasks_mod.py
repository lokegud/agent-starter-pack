"""
Forgix Tasks module — local JSON task list.
Permissions: read_tasks, write_tasks
No external API required.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from forgix.modules.base import BaseModule, ModuleManifest, tool_schema

TASKS_FILE = Path.home() / ".forgix" / "tasks.json"


class TasksModule(BaseModule):
    manifest = ModuleManifest(
        name="tasks",
        version="0.1.0",
        description="Local task list — create, list, and complete tasks",
        required_permissions=["read_tasks", "write_tasks"],
    )

    def _load(self) -> list[dict]:
        if TASKS_FILE.exists():
            try:
                return json.loads(TASKS_FILE.read_text())
            except Exception:
                pass
        return []

    def _save(self, tasks: list[dict]) -> None:
        TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
        TASKS_FILE.write_text(json.dumps(tasks, indent=2))

    def get_tools(self) -> dict[str, Callable]:
        return {
            "tasks.list": self.list_tasks,
            "tasks.add": self.add_task,
            "tasks.complete": self.complete_task,
            "tasks.delete": self.delete_task,
        }

    @tool_schema("tasks.list", "List all tasks",
        {"filter": {"type": "string", "description": "all|pending|done (default: pending)"}},
        required=[])
    async def list_tasks(self, filter: str = "pending") -> str:
        tasks = self._load()
        if filter == "done":
            tasks = [t for t in tasks if t.get("done")]
        elif filter == "pending":
            tasks = [t for t in tasks if not t.get("done")]
        if not tasks:
            return f"No {filter} tasks."
        return "\n".join(
            f"[{'x' if t.get('done') else ' '}] {t['id'][:8]} {t['title']}"
            + (f" (due: {t['due']})" if t.get('due') else "")
            for t in tasks
        )

    @tool_schema("tasks.add", "Add a new task",
        {"title": {"type": "string"}, "due": {"type": "string", "description": "Optional due date (ISO)"}},
        required=["title"])
    async def add_task(self, title: str, due: str = "") -> str:
        tasks = self._load()
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "done": False,
            "created": datetime.now(timezone.utc).isoformat(),
            "due": due,
        }
        tasks.append(task)
        self._save(tasks)
        return f"Task added: {task['id'][:8]} — {title}"

    @tool_schema("tasks.complete", "Mark a task as done",
        {"task_id": {"type": "string", "description": "Task ID (or prefix)"}},
        required=["task_id"])
    async def complete_task(self, task_id: str) -> str:
        tasks = self._load()
        for t in tasks:
            if t["id"].startswith(task_id):
                t["done"] = True
                t["completed_at"] = datetime.now(timezone.utc).isoformat()
                self._save(tasks)
                return f"Task completed: {t['title']}"
        return f"[Task not found: {task_id}]"

    @tool_schema("tasks.delete", "Delete a task",
        {"task_id": {"type": "string"}},
        required=["task_id"])
    async def delete_task(self, task_id: str) -> str:
        tasks = self._load()
        before = len(tasks)
        tasks = [t for t in tasks if not t["id"].startswith(task_id)]
        if len(tasks) == before:
            return f"[Task not found: {task_id}]"
        self._save(tasks)
        return f"Task deleted."
