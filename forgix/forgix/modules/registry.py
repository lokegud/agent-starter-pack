"""
Forgix module registry — load and verify external modules from GitHub.

External modules must:
1. Include a manifest.json with sha256 hash
2. Pass SHA-256 hash verification
3. Receive explicit user approval
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import logging
from pathlib import Path

import httpx

log = logging.getLogger(__name__)
FORGIX_DIR = Path.home() / ".forgix"
EXT_MODULES_DIR = FORGIX_DIR / "modules"


class ModuleRegistry:

    @staticmethod
    async def install_from_github(source: str) -> None:
        """
        Install a module from GitHub.
        Format: github:owner/repo/module_name
        """
        from rich.console import Console
        from rich.prompt import Confirm
        console = Console()

        if not source.startswith("github:"):
            raise ValueError(f"Unknown source scheme: {source}")

        path_part = source[len("github:"):]
        parts = path_part.split("/")
        if len(parts) < 3:
            raise ValueError("Format: github:owner/repo/module_name")

        owner, repo, module_name = parts[0], parts[1], "/".join(parts[2:])
        raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{module_name}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch manifest
            manifest_url = f"{raw_base}/manifest.json"
            console.print(f"[cyan]Fetching manifest from {manifest_url}[/cyan]")
            resp = await client.get(manifest_url)
            resp.raise_for_status()
            manifest = resp.json()

            expected_sha256 = manifest.get("sha256")
            if not expected_sha256:
                raise ValueError("Module manifest missing sha256 hash")

            # Fetch module code
            module_url = f"{raw_base}/module.py"
            console.print(f"[cyan]Fetching module code...[/cyan]")
            code_resp = await client.get(module_url)
            code_resp.raise_for_status()
            code_bytes = code_resp.content

        # Verify SHA-256
        actual_sha256 = hashlib.sha256(code_bytes).hexdigest()
        if actual_sha256 != expected_sha256:
            raise ValueError(
                f"SHA-256 mismatch!\n  Expected: {expected_sha256}\n  Got:      {actual_sha256}\n"
                f"Module may have been tampered with. Installation aborted."
            )
        console.print(f"[green]✓ SHA-256 verified[/green]")

        # Show manifest and request approval
        console.print(f"\nModule: [bold]{manifest.get('name', module_name)}[/bold]")
        console.print(f"Version: {manifest.get('version', '?')}")
        console.print(f"Author: {manifest.get('author', 'unknown')}")
        console.print(f"Description: {manifest.get('description', '')}")
        perms = manifest.get('required_permissions', [])
        if perms:
            console.print(f"[yellow]Permissions requested: {', '.join(perms)}[/yellow]")

        if not Confirm.ask("\nInstall this module?", default=False):
            console.print("[yellow]Installation cancelled.[/yellow]")
            return

        # Save
        EXT_MODULES_DIR.mkdir(parents=True, exist_ok=True)
        module_path = EXT_MODULES_DIR / f"{module_name.replace('/', '_')}.py"
        module_path.write_bytes(code_bytes)
        meta_path = EXT_MODULES_DIR / f"{module_name.replace('/', '_')}.json"
        meta_path.write_text(json.dumps(manifest, indent=2))

        console.print(f"[green]✓ Module installed: {module_path}[/green]")

    @staticmethod
    def load_module(module_path: Path):
        """Load a module from a file path using importlib."""
        spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
        if not spec or not spec.loader:
            raise ImportError(f"Cannot load module from {module_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod
