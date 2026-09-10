"""Coordinate file detection and movement."""

import logging
from pathlib import Path

from .exceptions import UnsupportedFileError
from .file_detector import detect_file_category
from .file_mover import DuplicatePolicy, move_file

logger = logging.getLogger(__name__)


def count_processed(report: dict[str, object]) -> int:
    """Return the number of files represented in an organization report."""
    logger.debug(f"Counting processed files in report")
    return sum(
        len(report[key])
        for key in ("moved", "skipped_duplicates", "unsupported", "failed")
    )


def organize_folder(
    source_folder: str | Path,
    output_folder: str | Path | None = None,
    *,
    create_destinations: bool = True,
    duplicate_policy: DuplicatePolicy = "rename",
) -> dict[str, object]:
    """Organize the immediate files in *source_folder* by extension."""
    source = Path(source_folder)
    output = Path(output_folder) if output_folder is not None else source
    logger.debug(
        f"Starting folder organization: source={source}, output={output}, "
        f"create_destinations={create_destinations}, "
        f"duplicate_policy={duplicate_policy!r}"
    )
    if not source.exists():
        logger.warning(f"Source folder does not exist: {source}")
        raise FileNotFoundError(f"source folder does not exist: {source}")
    if not source.is_dir():
        logger.warning(f"Source path is not a folder: {source}")
        raise NotADirectoryError(f"source path is not a folder: {source}")
    files = [path for path in source.iterdir() if path.is_file()]

    report = {
        "moved": [],
        "skipped_duplicates": [],
        "unsupported": [],
        "failed": {},
    }
    logger.info(f"Organizing {len(files)} files from {source} into {output}")

    for file_path in files:
        try:
            category = detect_file_category(file_path)
            final_path = move_file(
                file_path,
                output / category,
                create_destination=create_destinations,
                duplicate_policy=duplicate_policy,
            )
            if final_path is None:
                report["skipped_duplicates"].append(file_path)
            else:
                report["moved"].append(final_path)
        except UnsupportedFileError as error:
            report["unsupported"].append(file_path)
            logger.debug(f"Unsupported file left in place: {file_path} ({error})")
        except (
            FileNotFoundError,
            IsADirectoryError,
            PermissionError,
            OSError,
            ValueError,
        ) as error:
            report["failed"][file_path] = str(error)
            logger.error(f"Failed to organize file: {file_path}", exc_info=True)

    logger.info(
        f"Organization finished: moved={len(report['moved'])}, "
        f"duplicates_skipped={len(report['skipped_duplicates'])}, "
        f"unsupported={len(report['unsupported'])}, failed={len(report['failed'])}"
    )
    return report


def organise_folder(
    source_folder: str | Path,
    output_folder: str | Path | None = None,
    **kwargs: object,
) -> dict[str, object]:
    """British-spelling alias for :func:`organize_folder`."""
    logger.debug(
        f"Starting organise_folder: source={source_folder!r}, "
        f"output={output_folder!r}, options={kwargs!r}"
    )
    return organize_folder(source_folder, output_folder, **kwargs)
