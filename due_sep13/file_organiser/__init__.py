"""Public interface for the file_organiser package."""

import logging

from .exceptions import UnsupportedFileError
from .file_detector import EXTENSION_CATEGORIES, detect_file_category, detect_file_type
from .file_mover import DuplicatePolicy, move_file
from .logging_config import DEFAULT_LOG_FILE, configure_logging
from .organizer import (
    count_processed,
    organise_folder,
    organize_folder,
)

__all__ = [
    "DEFAULT_LOG_FILE",
    "DuplicatePolicy",
    "EXTENSION_CATEGORIES",
    "UnsupportedFileError",
    "configure_logging",
    "count_processed",
    "detect_file_category",
    "detect_file_type",
    "move_file",
    "organise_folder",
    "organize_folder",
]

__version__ = "1.0.0"

logging.getLogger(__name__).addHandler(logging.NullHandler())
