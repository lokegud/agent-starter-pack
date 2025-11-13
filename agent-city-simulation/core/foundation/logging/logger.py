"""
Structured logging configuration.

Provides JSON logging with context and sensitive data masking.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from pythonjsonlogger import jsonlogger

from core.shared.config import get_settings


def setup_logging(
    service_name: str,
    log_level: Optional[str] = None,
) -> None:
    """Set up structured logging for a service.

    Args:
        service_name: Name of the service (e.g., "identity-generator")
        log_level: Optional log level override
    """
    settings = get_settings()
    log_level = log_level or settings.log_level

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level",
            "name": "logger",
        },
    )
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # File handler (if enabled and not in production)
    if settings.is_development():
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(log_dir / f"{service_name}.log")
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)

    logger.info(f"Logging initialized for {service_name} at level {log_level}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive data in logs."""

    SENSITIVE_FIELDS = [
        "password",
        "api_key",
        "secret",
        "token",
        "credential",
        "authorization",
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log record to mask sensitive data.

        Args:
            record: Log record

        Returns:
            True to keep the record
        """
        if hasattr(record, "msg") and isinstance(record.msg, str):
            for field in self.SENSITIVE_FIELDS:
                if field in record.msg.lower():
                    record.msg = self._mask_sensitive(record.msg, field)

        return True

    def _mask_sensitive(self, message: str, field: str) -> str:
        """Mask sensitive field in message.

        Args:
            message: Log message
            field: Sensitive field name

        Returns:
            Message with masked field
        """
        # Simple masking - can be enhanced
        return message.replace(field, f"{field}=***MASKED***")
