"""Logging configuration for the student-result processor."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_LOG_FILE = Path(__file__).with_name("student_results.log")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    log_file: str | Path = DEFAULT_LOG_FILE,
    *,
    console: bool = True,
) -> Path:
    """Configure terminal and rotating file logging."""
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
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=handlers,
        force=True,
    )
    logger.debug(f"Logging configured at DEBUG level: {path}")
    return path
