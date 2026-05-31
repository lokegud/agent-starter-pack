#!/usr/bin/env python3
"""Forgix Bootstrap — first-time setup wizard. Run via: forgix setup"""
from __future__ import annotations

import json
import os
import platform
import secrets
import subprocess
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
except ImportError:
    print("Installing 'rich'...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "rich"], check=True)
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint

console = Console()

FORGIX_DIR = Path.home() / ".forgix"
CONFIG_PATH = FORGIX_DIR / "config.json"
DB_PATH = FORGIX_DIR / "memory.db"

MODULE_CREDENTIALS: dict[str, list[tuple[str, str]]] = {
    "github":   [("github_token", "GitHub Personal Access Token (repo scope)")],
    "calendar": [("google_client_id", "Google OAuth Client ID"), ("google_client_secret", "Google OAuth Client Secret")],
    "email":    [("email_address", "Email address"), ("email_password_or_token", "App password or OAuth token")],
    "slack":    [("slack_bot_token", "Slack Bot Token (xoxb-...)")],
    "notes":    [("notes_vault_path", "Path to your markdown/Obsidian vault")],
    "tasks":    [],
}

AVAILABLE_MODULES = ["github", "calendar", "email", "slack", "notes", "tasks"]


def is_android_termux() -> bool:
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix or os.path.exists("/data/data/com.termux")


def get_ram_gb() -> float:
    try:
        import psutil
        return psutil.virtual_memory().total / (1024 ** 3)
    except ImportError:
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        return int(line.split()[1]) / (1024 ** 2)
        except Exception:
            pass
        return 4.0


def store_secret(key: str, value: str) -> None:
    import keyring
    keyring.set_password("forgix", key, value)


def get_secret(key: str) -> str | None:
    import keyring
    return keyring.get_password("forgix", key)


def ollama_installed() -> bool:
    try:
        return subprocess.run(["ollama", "--version"], capture_output=True, timeout=5).returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def install_ollama() -> None:
    if platform.system() == "Linux":
        console.print("[cyan]Installing Ollama...[/cyan]")
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
    else:
        console.print("[yellow]Please install Ollama from https://ollama.com/download then re-run: forgix setup[/yellow]")
        sys.exit(1)


def pull_ollama_model(model_tag: str) -> None:
    console.print(f"[cyan]Pulling {model_tag}...[/cyan]")
    with console.status(f"[bold green]Downloading {model_tag}..."):
        subprocess.run(["ollama", "pull", model_tag], check=True)
    console.print(f"[green]✓ {model_tag} ready[/green]")


GGUF_REPOS = {
    "e2b": ("google/gemma-4-e2b-it-gguf", "gemma-4-e2b-it-q4_k_m.gguf"),
    "e4b": ("google/gemma-4-e4b-it-gguf", "gemma-4-e4b-it-q4_k_m.gguf"),
}


def download_gguf(variant: str, dest_dir: Path) -> Path:
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "huggingface_hub>=0.24"], check=True)
        from huggingface_hub import hf_hub_download

    dest_dir.mkdir(parents=True, exist_ok=True)
    repo_id, filename = GGUF_REPOS[variant]
    dest = dest_dir / filename
    if dest.exists():
        console.print(f"[green]✓ Model already present: {dest}[/green]")
        return dest

    console.print(f"[cyan]Downloading {filename} from HuggingFace (~1.3 GB for E2B)...[/cyan]")
    with console.status("[bold green]Downloading... (this takes a while on first run)"):
        path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=str(dest_dir))
    console.print(f"[green]✓ Model downloaded: {path}[/green]")
    return Path(path)


def run_setup() -> None:
    console.print(Panel.fit(
        "[bold cyan]Forgix Setup Wizard[/bold cyan]\n"
        "The private, secure, self-building AI agent.\n"
        "[dim]Designed to fix everything OpenClaw got wrong.[/dim]",
        border_style="cyan"
    ))
    console.print()

    is_android = is_android_termux()
    ram_gb = get_ram_gb()
    platform_name = "Android/Termux" if is_android else platform.system()
    console.print(f"[dim]Platform: {platform_name} | RAM: {ram_gb:.1f} GB[/dim]\n")

    # Model selection
    console.print("[bold]Step 1: Choose your model[/bold]\n")
    e4b_ok = ram_gb >= 7.0
    console.print(f"  [{'green' if True else 'red'}]gemma4-E2B[/] — 2B params, ~1.3 GB,  ~3 GB RAM needed")
    console.print(f"  [{'green' if e4b_ok else 'yellow'}]gemma4-E4B[/] — 4B params, ~2.5 GB, ~7 GB RAM needed{'  ← recommended' if e4b_ok else '  (may be slow)'}\n")
    variant = Prompt.ask("Choose variant", choices=["e2b", "e4b"], default="e4b" if e4b_ok else "e2b")

    # Backend setup
    console.print()
    console.print("[bold]Step 2: Inference backend[/bold]")
    models_dir = FORGIX_DIR / "models"
    gguf_path: Path | None = None
    model_tag = ""

    if is_android:
        console.print("[cyan]Android → llama.cpp backend[/cyan]")
        gguf_path = download_gguf(variant, models_dir)
        model_tag = str(gguf_path)
    else:
        console.print("[cyan]Desktop → Ollama backend[/cyan]")
        if not ollama_installed():
            install_ollama()
        else:
            console.print("[green]✓ Ollama installed[/green]")
        ollama_tag = "gemma4:2b" if variant == "e2b" else "gemma4:4b"
        pull_ollama_model(ollama_tag)
        model_tag = ollama_tag

    # Security tokens
    console.print()
    console.print("[bold]Step 3: Security tokens[/bold]")
    if get_secret("session_token") and not Confirm.ask("Token exists — regenerate?", default=False):
        console.print("[green]✓ Existing token kept[/green]")
    else:
        store_secret("session_token", secrets.token_urlsafe(32))
        console.print("[green]✓ Session token → OS keychain[/green]")
    store_secret("csrf_token", secrets.token_urlsafe(32))
    console.print("[green]✓ CSRF token → OS keychain[/green]")

    from cryptography.fernet import Fernet
    if not get_secret("db_fernet_key"):
        store_secret("db_fernet_key", Fernet.generate_key().decode())
        console.print("[green]✓ DB encryption key → OS keychain[/green]")

    # Database
    console.print()
    console.print("[bold]Step 4: Encrypted database[/bold]")
    FORGIX_DIR.mkdir(parents=True, exist_ok=True)
    try:
        import asyncio
        sys.path.insert(0, str(Path(__file__).parent))
        from forgix.core.memory import MemoryStore
        asyncio.run(MemoryStore.initialize())
        console.print(f"[green]✓ Encrypted DB at {DB_PATH}[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠ DB will initialize on first run: {e}[/yellow]")

    # Modules
    console.print()
    console.print("[bold]Step 5: Productivity modules[/bold]")
    console.print("[dim](change anytime with: forgix modules enable/disable <name>)[/dim]\n")
    enabled_modules: list[str] = []
    for mod in AVAILABLE_MODULES:
        creds = MODULE_CREDENTIALS.get(mod, [])
        note = f" [dim]({len(creds)} credential{'s' if len(creds)!=1 else ''})[/dim]" if creds else " [dim](no setup needed)[/dim]"
        if Confirm.ask(f"  Enable [cyan]{mod}[/cyan]?{note}", default=False):
            enabled_modules.append(mod)
            for key, label in creds:
                store_secret(f"module_{mod}_{key}", Prompt.ask(f"    {label}", password=True))
                console.print("    [green]✓ Stored in keychain[/green]")

    # Persona & theme
    console.print()
    console.print("[bold]Step 6: Persona & UI theme[/bold] [dim](randomized each start by default)[/dim]\n")
    persona = Prompt.ask("Persona", default="random")
    theme = Prompt.ask("Theme",   default="random")

    # Write config
    config = {
        "version": "0.1.0",
        "model_variant": variant,
        "model_tag": model_tag,
        "backend": "llamacpp" if is_android else "ollama",
        "gguf_path": str(gguf_path) if gguf_path else None,
        "enabled_modules": enabled_modules,
        "persona": persona,
        "theme": theme,
        "port": 7433,
        "setup_complete": True,
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    console.print(f"\n[green]✓ Config → {CONFIG_PATH}[/green]")

    console.print(Panel.fit(
        "[bold green]✓ Setup complete![/bold green]\n\n"
        "Start:          [bold]forgix start[/bold]\n"
        "LAN / iPhone:   [bold]forgix start --lan[/bold]\n"
        "Modules:        [bold]forgix modules list[/bold]\n"
        "Security:       [bold]forgix security status[/bold]",
        border_style="green"
    ))


if __name__ == "__main__":
    run_setup()
