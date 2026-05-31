"""
Forgix module base — BaseModule ABC and ModuleManifest.

All modules expose tools as async callables registered in a dict
keyed by 'namespace.action' (e.g. 'github.create_issue').
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ModuleManifest:
    name: str
    version: str
    description: str
    required_permissions: list[str] = field(default_factory=list)
    sha256: str = ""  # for externally loaded modules
    author: str = ""


class BaseModule(ABC):
    manifest: ModuleManifest

    @abstractmethod
    def get_tools(self) -> dict[str, Callable]:
        """
        Return a dict mapping 'namespace.action' → async callable.
        Each callable may have a _forgix_schema attribute with the full
        JSON schema for the LLM.
        """
        ...

    def _get_secret(self, key: str) -> str | None:
        import keyring
        return keyring.get_password("forgix", key)


def tool_schema(name: str, description: str, properties: dict, required: list[str] | None = None):
    """Decorator that attaches a _forgix_schema to a function."""
    def decorator(fn):
        fn._forgix_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required or [],
                },
            },
        }
        return fn
    return decorator
