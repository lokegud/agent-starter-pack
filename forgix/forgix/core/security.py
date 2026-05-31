"""
Forgix security — token management, CSRF, rate limiting, localhost guard.

Hardcoded security guarantees:
- assert_localhost_only() rejects any non-localhost bind (OpenClaw's fatal mistake)
- Session token stored in OS keychain only, never on disk
- LAN mode requires explicit --lan flag; auto-generates self-signed TLS cert
"""
from __future__ import annotations

import ipaddress
import logging
import secrets
import time
from collections import defaultdict
from pathlib import Path

log = logging.getLogger(__name__)

FORGIX_DIR = Path.home() / ".forgix"
TLS_DIR = FORGIX_DIR / "tls"


class SecurityManager:

    @staticmethod
    def get_session_token() -> str:
        import keyring
        token = keyring.get_password("forgix", "session_token")
        if not token:
            raise RuntimeError("Session token not found — run 'forgix setup'")
        return token

    @staticmethod
    def store_session_token(token: str) -> None:
        import keyring
        keyring.set_password("forgix", "session_token", token)

    @staticmethod
    def get_csrf_token() -> str:
        import keyring
        token = keyring.get_password("forgix", "csrf_token")
        if not token:
            token = secrets.token_urlsafe(32)
            keyring.set_password("forgix", "csrf_token", token)
        return token

    @staticmethod
    def verify_bearer_token(authorization_header: str | None) -> bool:
        if not authorization_header:
            return False
        parts = authorization_header.strip().split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return False
        try:
            expected = SecurityManager.get_session_token()
        except RuntimeError:
            return False
        return secrets.compare_digest(parts[1], expected)

    @staticmethod
    def verify_websocket_auth(token: str, csrf: str) -> bool:
        try:
            return (
                secrets.compare_digest(token, SecurityManager.get_session_token()) and
                secrets.compare_digest(csrf, SecurityManager.get_csrf_token())
            )
        except RuntimeError:
            return False

    @staticmethod
    def assert_localhost_only(host: str) -> None:
        """
        Reject any non-localhost bind attempt.
        This is the hard guard against the OpenClaw 0.0.0.0 disaster.
        """
        if host not in {"127.0.0.1", "::1", "localhost"}:
            raise ValueError(
                f"SECURITY VIOLATION: Forgix refuses to bind to '{host}'. "
                f"Only 127.0.0.1 is allowed in default mode. Use --lan for LAN access."
            )

    @staticmethod
    def is_lan_subnet(ip: str) -> bool:
        try:
            return ipaddress.ip_address(ip).is_private
        except ValueError:
            return False


class RateLimiter:
    def __init__(self, requests_per_minute: int = 120):
        self.rpm = requests_per_minute
        self._counts: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, ip: str) -> bool:
        now = time.monotonic()
        window = now - 60.0
        self._counts[ip] = [t for t in self._counts[ip] if t > window]
        if len(self._counts[ip]) >= self.rpm:
            return False
        self._counts[ip].append(now)
        return True


_localhost_limiter = RateLimiter(requests_per_minute=120)
_lan_limiter = RateLimiter(requests_per_minute=30)


def get_rate_limiter(ip: str) -> RateLimiter:
    return _localhost_limiter if ip in ("127.0.0.1", "::1") else _lan_limiter


def generate_lan_tls_cert() -> tuple[Path, Path]:
    """Generate self-signed TLS cert for --lan mode. Stored at ~/.forgix/tls/."""
    import datetime
    import socket
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    TLS_DIR.mkdir(parents=True, exist_ok=True)
    cert_path = TLS_DIR / "cert.pem"
    key_path = TLS_DIR / "key.pem"

    if cert_path.exists() and key_path.exists():
        return cert_path, key_path

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    local_ip = socket.gethostbyname(socket.gethostname())

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "forgix-lan"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Forgix Local"),
    ])
    san = x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
        x509.IPAddress(ipaddress.ip_address(local_ip)),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject).issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(san, critical=False)
        .sign(key, hashes.SHA256(), default_backend())
    )

    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    key_path.chmod(0o600)
    log.info("TLS cert written to %s", TLS_DIR)
    return cert_path, key_path
