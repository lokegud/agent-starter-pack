"""
Forgix Skill Manager — registry for built-in skills.

Built-in skills are always available regardless of enabled modules:
- web_search : DuckDuckGo (no API key)
- calculator : safe math evaluation (no eval/exec)
- file_ops   : sandboxed file read/write with path jail
"""
from __future__ import annotations

from typing import Callable


class SkillManager:
    def __init__(self):
        from forgix.skills.builtin import search, calculator, file_ops
        self._search = search
        self._calculator = calculator
        self._file_ops = file_ops

    def get_tools(self) -> dict[str, Callable]:
        tools: dict[str, Callable] = {}
        tools["skill.web_search"] = self._search.web_search
        tools["skill.calculate"] = self._calculator.calculate
        tools["skill.read_file"] = self._file_ops.read_file
        tools["skill.write_file"] = self._file_ops.write_file
        tools["skill.list_dir"] = self._file_ops.list_dir
        return tools
