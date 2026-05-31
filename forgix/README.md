# Forgix 🔥

**A private, secure, self-building AI agent. The anti-OpenClaw.**

Forgix runs a local Gemma 4 model on your own hardware — desktop or Android phone —
with a security model built as the direct inverse of every mistake OpenClaw made.

## Why Forgix exists

OpenClaw exposed 42,665 instances to the internet with full remote code execution.
It bound to `0.0.0.0` by default, had no authentication, no prompt-injection defense,
stored API keys in plaintext, and ran with full system privileges. Forgix inverts
every one of those failures. See [SECURITY.md](SECURITY.md).

## Features

- **Local & private** — Gemma 4 (E2B/E4B) via Ollama (desktop) or llama.cpp (Android)
- **Runs on your phone** — Android via Termux; iPhone access via LAN mode
- **Secure by default** — 127.0.0.1 only, keychain-stored tokens, encrypted SQLite,
  prompt-injection guard, capability-based module permissions, encrypted audit log
- **Modular** — GitHub, Calendar, Email, Slack, Notes, Tasks (enable only what you want)
- **Self-building** — install verified modules from GitHub (SHA-256 checked)
- **Random personality** — a different one of 20 famous figures every boot
- **Random UI** — a different one of 10 visual themes every boot
- **Built-in skills** — web search, safe calculator, sandboxed file ops

## Quick start

```bash
# One-curl install (desktop or Termux)
curl -fsSL https://raw.githubusercontent.com/lokegud/agent-starter-pack/claude/self-building-ai-agent-d8sBn/forgix/install.sh | bash

forgix setup     # download model + configure modules
forgix start     # open chat UI at http://127.0.0.1:7433
```

### On Android (Termux)

```bash
pkg install python git
curl -fsSL .../forgix/install.sh | bash
forgix setup            # downloads gemma-4-e2b GGUF (~1.3 GB)
forgix start --lan      # access from other devices on your WiFi (incl. iPhone)
```

## Platform support

| Platform | Inference | Notes |
|---|---|---|
| macOS / Linux / Windows | Ollama | `forgix start` |
| Android (Termux) | llama.cpp | on-device |
| iPhone / iPad | — | browser client via `forgix start --lan` |

## CLI

```bash
forgix setup | start [--lan] [--port N]
forgix modules list | enable <m> | disable <m> | configure <m> | install github:o/r/m
forgix persona show | random
forgix ui theme | random
forgix security status | rotate
forgix model status | pull
```

## Architecture

```
forgix/
├── core/      model (multi-backend), agent (ReAct), memory (encrypted),
│             security (tokens/CSRF/rate-limit), prompt_guard (injection defense)
├── modules/   github, calendar, email, slack, notes, tasks + registry
├── interface/ FastAPI server, random UI generator
├── persona/   20 famous-figure personas
└── skills/    web search, calculator, file ops (always on)
```

## License

MIT
