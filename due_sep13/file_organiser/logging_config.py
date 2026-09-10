"""Logging configuration for the file-organizer application."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_LOG_FILE = Path(__file__).with_name("file_organiser.log")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    log_file: str | Path = DEFAULT_LOG_FILE,
    *,
    level: int = logging.DEBUG,
    console: bool = True,
) -> Path:
    """Configure terminal and rotating-file logging."""
    try:
        path = Path(log_file).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            path,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handlers: list[logging.Handler] = [file_handler]
        if console:
            handlers.append(logging.StreamHandler())

        logging.basicConfig(
            level=level,
            format=LOG_FORMAT,
            datefmt=DATE_FORMAT,
            handlers=handlers,
            force=True,
        )
        logger.debug(f"Logging configured at level {logging.getLevelName(level)}: {path}")
        return path
    except (TypeError, ValueError, OSError):
        logger.error(
            f"Logging configuration failed: log_file={log_file!r}, level={level!r}",
            exc_info=True,
        )
        raise
