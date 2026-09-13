"""Configure terminal, application, and error logging."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_LOG_DIRECTORY = Path(__file__).with_name("logs")
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    log_directory: str | Path = DEFAULT_LOG_DIRECTORY,
    *,
    console: bool = True,
) -> dict[str, Path]:
    """Configure required log files and return their paths."""
    directory = Path(log_directory).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    application_log = directory / "application.log"
    error_log = directory / "error.log"

    application_handler = logging.FileHandler(application_log, encoding="utf-8")
    application_handler.setLevel(logging.DEBUG)

    error_handler = logging.FileHandler(error_log, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)

    handlers: list[logging.Handler] = [application_handler, error_handler]
    if console:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=handlers,
        force=True,
    )
    logger.debug(f"Logging configured in {directory}")
    return {"application": application_log, "error": error_log}
