"""
Forgix Email module — IMAP read + SMTP send.
Permissions: read_email, send_email
"""
from __future__ import annotations

import imaplib
import smtplib
import email as _email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Callable

from forgix.modules.base import BaseModule, ModuleManifest, tool_schema


class EmailModule(BaseModule):
    manifest = ModuleManifest(
        name="email",
        version="0.1.0",
        description="Read and send email via IMAP/SMTP",
        required_permissions=["read_email", "send_email", "network"],
    )

    def get_tools(self) -> dict[str, Callable]:
        return {
            "email.list_inbox": self.list_inbox,
            "email.send": self.send,
        }

    @tool_schema("email.list_inbox", "List recent emails from inbox",
        {"limit": {"type": "integer", "description": "Number of emails (default 5)"}},
        required=[])
    async def list_inbox(self, limit: int = 5) -> str:
        address = self._get_secret("module_email_email_address")
        password = self._get_secret("module_email_email_password_or_token")
        if not address or not password:
            return "[Email not configured. Run: forgix modules configure email]"

        import asyncio
        return await asyncio.get_event_loop().run_in_executor(None, self._fetch_inbox, address, password, limit)

    def _fetch_inbox(self, address: str, password: str, limit: int) -> str:
        # Auto-detect IMAP server from email domain
        domain = address.split("@")[-1]
        imap_servers = {
            "gmail.com": "imap.gmail.com", "googlemail.com": "imap.gmail.com",
            "outlook.com": "imap-mail.outlook.com", "hotmail.com": "imap-mail.outlook.com",
            "yahoo.com": "imap.mail.yahoo.com",
        }
        server = imap_servers.get(domain, f"imap.{domain}")
        try:
            with imaplib.IMAP4_SSL(server) as imap:
                imap.login(address, password)
                imap.select("INBOX")
                _, nums = imap.search(None, "ALL")
                ids = nums[0].split()[-limit:]
                results = []
                for uid in reversed(ids):
                    _, data = imap.fetch(uid, "(RFC822.HEADER)")
                    msg = _email.message_from_bytes(data[0][1])
                    results.append(f"From: {msg['From']}\nSubject: {msg['Subject']}\nDate: {msg['Date']}")
                return "\n\n".join(results) or "Inbox is empty."
        except Exception as e:
            return f"[Email error: {e}]"

    @tool_schema("email.send", "Send an email",
        {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}},
        required=["to", "subject", "body"])
    async def send(self, to: str, subject: str, body: str) -> str:
        address = self._get_secret("module_email_email_address")
        password = self._get_secret("module_email_email_password_or_token")
        if not address or not password:
            return "[Email not configured. Run: forgix modules configure email]"

        domain = address.split("@")[-1]
        smtp_servers = {
            "gmail.com": ("smtp.gmail.com", 587), "googlemail.com": ("smtp.gmail.com", 587),
            "outlook.com": ("smtp-mail.outlook.com", 587), "hotmail.com": ("smtp-mail.outlook.com", 587),
            "yahoo.com": ("smtp.mail.yahoo.com", 587),
        }
        smtp_host, smtp_port = smtp_servers.get(domain, (f"smtp.{domain}", 587))

        import asyncio
        return await asyncio.get_event_loop().run_in_executor(
            None, self._send_email, address, password, smtp_host, smtp_port, to, subject, body
        )

    def _send_email(self, address, password, host, port, to, subject, body) -> str:
        try:
            msg = MIMEMultipart()
            msg["From"] = address
            msg["To"] = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            with smtplib.SMTP(host, port) as smtp:
                smtp.starttls()
                smtp.login(address, password)
                smtp.sendmail(address, to, msg.as_string())
            return f"Email sent to {to}."
        except Exception as e:
            return f"[Email send error: {e}]"
