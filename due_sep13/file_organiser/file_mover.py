"""Move files safely into destination folders."""

import logging
import shutil
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

DuplicatePolicy = Literal["rename", "skip", "error"]


def _unique_destination(path: Path) -> Path:
    """Return the first available ``name_N.ext`` destination path."""
    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def move_file(
    source: str | Path,
    destination_folder: str | Path,
    *,
    create_destination: bool = True,
    duplicate_policy: DuplicatePolicy = "rename",
) -> Path | None:
    """Move one file safely and return its final path.

    Duplicate policies:
        ``rename`` appends a numeric suffix, ``skip`` leaves the source in
        place, and ``error`` raises :class:`FileExistsError`.
    """
    source_path = Path(source)
    destination = Path(destination_folder)
    logger.debug(
        f"Starting file move: source={source_path}, destination={destination}, "
        f"create_destination={create_destination}, "
        f"duplicate_policy={duplicate_policy!r}"
    )
    if duplicate_policy not in {"rename", "skip", "error"}:
        logger.warning(f"Invalid duplicate policy: {duplicate_policy!r}")
        raise ValueError("duplicate_policy must be 'rename', 'skip', or 'error'")
    if not source_path.exists():
        logger.warning(f"Source file does not exist: {source_path}")
        raise FileNotFoundError(f"source file does not exist: {source_path}")
    if not source_path.is_file():
        logger.warning(f"Source path is not a file: {source_path}")
        raise IsADirectoryError(f"source is not a file: {source_path}")

    if destination.exists() and not destination.is_dir():
        logger.warning(f"Destination is not a folder: {destination}")
        raise NotADirectoryError(
            f"destination exists but is not a folder: {destination}"
        )
    if not destination.exists():
        if not create_destination:
            logger.warning(f"Destination folder does not exist: {destination}")
            raise FileNotFoundError(
                f"destination folder does not exist: {destination}"
            )
        destination.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created destination folder: {destination}")

    target = destination / source_path.name
    if target.exists():
        if duplicate_policy == "skip":
            logger.warning(
                f"Skipped duplicate file: source={source_path}, destination={target}"
            )
            return None
        if duplicate_policy == "error":
            logger.warning(f"Duplicate destination file found: {target}")
            raise FileExistsError(f"destination file already exists: {target}")
        renamed_target = _unique_destination(target)
        logger.info(f"Renaming duplicate destination: {target} -> {renamed_target}")
        target = renamed_target

    shutil.move(str(source_path), str(target))
    logger.info(f"Moved file successfully: {source_path} -> {target}")
    return target
