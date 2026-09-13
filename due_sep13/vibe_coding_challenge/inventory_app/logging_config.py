"""Simple terminal and file logging configuration."""

import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "logs" / "inventory.log"


def configure_logging(log_file: str | Path = LOG_FILE) -> Path:
    """Configure DEBUG-and-higher logging and return the log path."""
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(path, encoding="utf-8"),
        ],
        force=True,
    )
    logging.getLogger(__name__).debug(f"Logging configured: {path}")
    return path
