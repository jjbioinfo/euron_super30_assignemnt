"""Text-file reading and writing functions."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def read_file(file_path: str | Path) -> str:
    """Read and return UTF-8 text from a file."""
    path = Path(file_path).expanduser()
    logger.debug(f"Reading file: {path}")
    if not path.exists():
        logger.warning(f"File does not exist: {path}")
        raise FileNotFoundError(f"file does not exist: {path}")
    if not path.is_file():
        logger.warning(f"Read path is not a file: {path}")
        raise IsADirectoryError(f"path is not a file: {path}")

    content = path.read_text(encoding="utf-8")
    if content:
        logger.info(f"File read successfully: {path}")
    else:
        logger.warning(f"File was empty: {path}")
    return content


def write_file(
    file_path: str | Path,
    content: object,
    *,
    append: bool = False,
) -> Path:
    """Write UTF-8 text and return the file path."""
    path = Path(file_path).expanduser()
    logger.debug(f"Writing file: path={path}, append={append}")
    if not isinstance(content, str):
        logger.warning(f"File content is not text: {type(content).__name__}")
        raise TypeError("file content must be a string")
    if path.exists() and path.is_dir():
        logger.warning(f"Cannot write to a directory: {path}")
        raise IsADirectoryError(f"cannot write text to a directory: {path}")
    if path.exists() and not append:
        logger.warning(f"Existing file will be overwritten: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with path.open(mode, encoding="utf-8") as output_file:
        output_file.write(content)

    logger.info(f"File written successfully: path={path}, append={append}")
    return path
