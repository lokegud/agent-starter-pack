# Forgix Security Model

Forgix was designed as a direct response to OpenClaw's catastrophic security failures,
which exposed 42,665 instances with full RCE due to fundamental design mistakes.

## What We Fixed

| OpenClaw Failure | CVE / Impact | Forgix Response |
|---|---|---|
| Bound to `0.0.0.0` by default | 42,665 exposed instances | Hardcoded `127.0.0.1` — refuse all other bindings |
| No authentication | Full RCE on any machine | Mandatory session token stored in OS keychain |
| WebSocket cross-site hijacking | CVE-2026-25253 CVSS 8.8 | CSRF token required on WS handshake; CORS localhost-only |
| No prompt injection defense | Private keys stolen via email | `PromptGuard` layer wraps ALL external data |
| Unmoderated skills marketplace | 9 critical/high CVEs in 1 skill | SHA-256 hash + Ed25519 signature on every module |
| API keys in plaintext config | 1.5M keys exposed | OS keychain only — never written to disk |
| Full system admin by default | RCE with sysadmin privs | Capability-based permissions; sandbox for dangerous ops |
| No audit trail | Silent exfiltration possible | Every tool call logged to encrypted SQLite audit log |

## Network Binding

- **Default**: `127.0.0.1` only. Connections from other machines are refused.
- **LAN mode** (`--lan`): explicit opt-in only. Binds to local subnet IP, requires TLS.
- `0.0.0.0` is hardcoded to reject — cannot be enabled without modifying source.

## Authentication

1. Session token: `secrets.token_urlsafe(32)` generated at first setup
2. Stored in OS keychain (macOS Keychain / Windows Credential Manager / libsecret)
3. All API requests require `Authorization: Bearer <token>`
4. WebSocket connections require `{token, csrf}` in first frame before any processing
5. Rate limit: 120 req/min (localhost), 30 req/min (LAN)

## LAN Mode Security

When `--lan` is used:
- TLS via auto-generated self-signed certificate (`~/.forgix/tls/`)
- CORS restricted to RFC-1918 subnets only (`192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`)
- Rate limit tightened to 30 req/min
- QR code printed for one-tap mobile setup (includes token)

## Prompt Injection Defense

All external data (tool results, email bodies, web content, notes) passes through `PromptGuard`:
1. Scanned against 15+ injection pattern regexes
2. Wrapped in `<external_data source="...">` tags visible to the LLM
3. `blocked` (>2 patterns) or `suspicious` (1-2 patterns) — redacted or flagged
4. All injection attempts logged to the encrypted audit table

## Secret Storage

- **Never** written to disk in plaintext
- All secrets via `keyring` → OS native store
- Database Fernet key stored in keychain
- `~/.forgix/config.json` contains only non-secret settings

## Audit Logging

Every tool call is logged to an encrypted SQLite table at `~/.forgix/memory.db`.
Logs include: timestamp, tool name, redacted args, result status.
Logs cannot be disabled.

## Reporting Vulnerabilities

Please report security issues at: https://github.com/lokegud/agent-starter-pack/security
