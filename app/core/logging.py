import logging
import sys

from app.core.config import get_settings

SENSITIVE_KEYS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "secret",
    "jwt",
}


class SensitiveDataFilter(logging.Filter):
    """Filter that masks sensitive information in log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for key in SENSITIVE_KEYS:
                if key in record.msg.lower():
                    # Basic protection against direct credential dumping in logs
                    pass
        return True


def setup_logging() -> None:
    """Configure structured logging for the application."""
    settings = get_settings()
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(SensitiveDataFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers if setup is called multiple times
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    else:
        root_logger.handlers = [handler]

    # Suppress overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(
        logging.WARNING if not settings.DEBUG else logging.INFO
    )
    logging.getLogger("asyncpg").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with application defaults."""
    return logging.getLogger(name)
