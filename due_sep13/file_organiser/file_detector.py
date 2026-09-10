"""Detect file categories from filename extensions."""

import logging
from pathlib import Path

from .exceptions import UnsupportedFileError

logger = logging.getLogger(__name__)

EXTENSION_CATEGORIES: dict[str, str] = {
    # Images
    ".bmp": "Images",
    ".gif": "Images",
    ".jpeg": "Images",
    ".jpg": "Images",
    ".png": "Images",
    ".svg": "Images",
    ".webp": "Images",
    # Plain text
    ".log": "Text",
    ".md": "Text",
    ".rtf": "Text",
    ".txt": "Text",
    # Documents
    ".doc": "Documents",
    ".docx": "Documents",
    ".pdf": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    # Structured data
    ".csv": "Data",
    ".json": "Data",
    ".tsv": "Data",
    ".xls": "Data",
    ".xlsx": "Data",
    ".xml": "Data",
}


def detect_file_category(file_path: str | Path) -> str:
    """Return the configured category for an existing file."""
    path = Path(file_path)
    logger.debug(f"Starting file detection: {path}")
    if not path.exists():
        logger.warning(f"File does not exist: {path}")
        raise FileNotFoundError(f"file does not exist: {path}")
    if not path.is_file():
        logger.warning(f"Expected a file but received a directory: {path}")
        raise IsADirectoryError(f"expected a file, received a directory: {path}")

    extension = path.suffix.lower()
    try:
        category = EXTENSION_CATEGORIES[extension]
    except KeyError as error:
        displayed_extension = extension or "<no extension>"
        logger.warning(
            f"Unsupported extension {displayed_extension!r}: {path.name}"
        )
        raise UnsupportedFileError(
            f"unsupported file extension {displayed_extension!r}: {path.name}"
        ) from error

    logger.debug(f"Detected {path} as category {category}")
    return category


def detect_file_type(file_path: str | Path) -> str:
    """Compatibility alias for :func:`detect_file_category`."""
    logger.debug(f"Starting detect_file_type: {file_path!r}")
    return detect_file_category(file_path)
