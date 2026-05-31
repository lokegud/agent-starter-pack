"""Forgix CLI entry point."""
from __future__ import annotations

import json
import sys
import webbrowser
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()
FORGIX_DIR = Path.home() / ".forgix"
CONFIG_PATH = FORGIX_DIR / "config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        console.print("[red]Forgix not set up. Run: forgix setup[/red]")
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())


def save_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))


@click.group()
@click.version_option(package_name="forgix")
def cli():
    """Forgix — private, secure AI agent. The anti-OpenClaw."""


# ---------------------------------------------------------------------------
# setup
# ---------------------------------------------------------------------------

@cli.command()
def setup():
    """First-time setup wizard."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    import bootstrap
    bootstrap.run_setup()


# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------

@cli.command()
@click.option("--port", default=None, type=int, help="Port (default 7433)")
@click.option("--lan", is_flag=True, default=False, help="LAN mode: bind subnet IP + TLS (iPhone access)")
@click.option("--no-browser", is_flag=True, default=False)
def start(port, lan, no_browser):
    """Start the Forgix agent."""
    cfg = load_config()
    if not cfg.get("setup_complete"):
        console.print("[red]Run 'forgix setup' first.[/red]")
        sys.exit(1)

    actual_port = port or cfg.get("port", 7433)

    if lan:
        import socket
        from forgix.core.security import generate_lan_tls_cert
        host = socket.gethostbyname(socket.gethostname())
        console.print(f"[yellow]⚠  LAN mode — binding to {host}:{actual_port}[/yellow]")
        generate_lan_tls_cert()
        url = f"https://{host}:{actual_port}"
        try:
            import qrcode
            from forgix.core.security import SecurityManager
            token = SecurityManager.get_session_token()
            qr = qrcode.QRCode(border=1)
            qr.add_data(f"{url}?token={token}")
            qr.make(fit=True)
            console.print("\n[bold cyan]Scan on your phone:[/bold cyan]")
            qr.print_ascii(invert=True)
        except ImportError:
            console.print(f"[cyan]Open on phone: {url}[/cyan]")
    else:
        from forgix.core.security import SecurityManager
        SecurityManager.assert_localhost_only("127.0.0.1")
        host = "127.0.0.1"
        url = f"http://{host}:{actual_port}"

    console.print(f"[bold green]Forgix running at {url}[/bold green]")
    if not no_browser and not lan:
        webbrowser.open(url)

    from forgix.interface.server import create_app
    import uvicorn
    app = create_app(config=cfg, lan_mode=lan)
    uvicorn.run(
        app,
        host=host,
        port=actual_port,
        ssl_keyfile=str(FORGIX_DIR / "tls" / "key.pem") if lan else None,
        ssl_certfile=str(FORGIX_DIR / "tls" / "cert.pem") if lan else None,
        log_level="warning",
    )


# ---------------------------------------------------------------------------
# modules
# ---------------------------------------------------------------------------

@cli.group()
def modules():
    """Manage productivity modules."""


@modules.command("list")
def modules_list():
    """Show all modules and their status."""
    cfg = load_config()
    enabled = set(cfg.get("enabled_modules", []))
    table = Table(title="Forgix Modules", header_style="bold cyan")
    table.add_column("Module", style="cyan")
    table.add_column("Status")
    table.add_column("Permissions")
    perms = {
        "github": "read_github, write_github",
        "calendar": "read_calendar, write_calendar",
        "email": "read_email, send_email",
        "slack": "read_slack, write_slack",
        "notes": "read_files, write_files",
        "tasks": "read_tasks, write_tasks",
    }
    for mod in ["github", "calendar", "email", "slack", "notes", "tasks"]:
        status = "[green]enabled[/green]" if mod in enabled else "[dim]disabled[/dim]"
        table.add_row(mod, status, perms.get(mod, ""))
    console.print(table)


@modules.command("enable")
@click.argument("name")
def modules_enable(name):
    """Enable a module."""
    cfg = load_config()
    enabled = cfg.get("enabled_modules", [])
    if name not in enabled:
        enabled.append(name)
    cfg["enabled_modules"] = enabled
    save_config(cfg)
    console.print(f"[green]✓ '{name}' enabled[/green]")


@modules.command("disable")
@click.argument("name")
def modules_disable(name):
    """Disable a module."""
    cfg = load_config()
    cfg["enabled_modules"] = [m for m in cfg.get("enabled_modules", []) if m != name]
    save_config(cfg)
    console.print(f"[yellow]'{name}' disabled[/yellow]")


@modules.command("configure")
@click.argument("name")
def modules_configure(name):
    """Configure API credentials for a module."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from bootstrap import MODULE_CREDENTIALS, store_secret
    from rich.prompt import Prompt
    for key, label in MODULE_CREDENTIALS.get(name, []):
        store_secret(f"module_{name}_{key}", Prompt.ask(f"  {label}", password=True))
        console.print("  [green]✓ Stored in keychain[/green]")
    console.print(f"[green]✓ '{name}' configured[/green]")


@modules.command("grant")
@click.argument("name")
@click.argument("permission")
def modules_grant(name, permission):
    """Grant a permission to a module."""
    cfg = load_config()
    cfg.setdefault("module_grants", {}).setdefault(name, [])
    if permission not in cfg["module_grants"][name]:
        cfg["module_grants"][name].append(permission)
    save_config(cfg)
    console.print(f"[green]✓ '{permission}' granted to '{name}'[/green]")


@modules.command("install")
@click.argument("source")
def modules_install(source):
    """Install external module (e.g. github:user/repo/module)."""
    from forgix.modules.registry import ModuleRegistry
    import asyncio
    asyncio.run(ModuleRegistry.install_from_github(source))


# ---------------------------------------------------------------------------
# persona
# ---------------------------------------------------------------------------

@cli.group()
def persona():
    """Manage the agent persona."""


@persona.command("show")
def persona_show():
    """Show current persona."""
    cfg = load_config()
    console.print(f"Persona: [bold cyan]{cfg.get('persona', 'random')}[/bold cyan]")


@persona.command("random")
def persona_random():
    """Pick a new random persona."""
    from forgix.persona.generator import PersonaGenerator
    g = PersonaGenerator()
    console.print(f"[bold cyan]{g.current_figure}[/bold cyan]")


# ---------------------------------------------------------------------------
# ui
# ---------------------------------------------------------------------------

@cli.group()
def ui():
    """Manage the UI theme."""


@ui.command("theme")
def ui_theme():
    """Show current theme."""
    cfg = load_config()
    console.print(f"Theme: [bold cyan]{cfg.get('theme', 'random')}[/bold cyan]")


@ui.command("random")
def ui_random():
    """Pick a new random theme."""
    from forgix.interface.ui_generator import UIGenerator
    g = UIGenerator()
    console.print(f"[bold cyan]{g.current_theme['name']}[/bold cyan]")


# ---------------------------------------------------------------------------
# security
# ---------------------------------------------------------------------------

@cli.group()
def security():
    """Security status and management."""


@security.command("status")
def security_status():
    """Show security status."""
    from forgix.core.security import SecurityManager
    import keyring
    table = Table(title="Forgix Security Status", header_style="bold green")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")

    try:
        token = SecurityManager.get_session_token()
        table.add_row("Session token", "[green]✓ present[/green]", f"{token[:8]}... (keychain)")
    except Exception as e:
        table.add_row("Session token", "[red]✗ missing[/red]", str(e))

    try:
        kr = keyring.get_keyring()
        table.add_row("OS keychain", "[green]✓ connected[/green]", kr.__class__.__name__)
    except Exception as e:
        table.add_row("OS keychain", "[red]✗ error[/red]", str(e))

    db_path = FORGIX_DIR / "memory.db"
    table.add_row(
        "Encrypted DB",
        "[green]✓ exists[/green]" if db_path.exists() else "[yellow]not yet created[/yellow]",
        str(db_path),
    )
    table.add_row("Network binding", "[green]✓ localhost[/green]", "127.0.0.1 (LAN requires --lan flag)")
    console.print(table)


@security.command("rotate")
def security_rotate():
    """Rotate the session token."""
    import secrets as _secrets
    from forgix.core.security import SecurityManager
    SecurityManager.store_session_token(_secrets.token_urlsafe(32))
    console.print("[green]✓ Token rotated. Restart Forgix to apply.[/green]")


# ---------------------------------------------------------------------------
# model
# ---------------------------------------------------------------------------

@cli.group()
def model():
    """Model management."""


@model.command("status")
def model_status():
    """Show model and backend status."""
    cfg = load_config()
    console.print(f"Backend:  [bold]{cfg.get('backend')}[/bold]")
    console.print(f"Model:    [bold]{cfg.get('model_tag')}[/bold]")
    console.print(f"Variant:  [bold]{cfg.get('model_variant')}[/bold]")


@model.command("pull")
def model_pull():
    """Re-pull/update the Gemma4 model."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    cfg = load_config()
    if cfg.get("backend") == "llamacpp":
        from bootstrap import download_gguf
        download_gguf(cfg["model_variant"], FORGIX_DIR / "models")
    else:
        from bootstrap import pull_ollama_model
        pull_ollama_model(cfg["model_tag"])


if __name__ == "__main__":
    cli()
