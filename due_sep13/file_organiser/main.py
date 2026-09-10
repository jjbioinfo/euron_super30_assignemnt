"""Command-line entry point and safe demonstration for file_organiser."""

import argparse
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

import file_organiser

logger = logging.getLogger("file_organiser.main")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        help="folder to organize; omit it to run the safe temporary demo",
    )
    parser.add_argument("--output", type=Path, help="optional separate output folder")
    parser.add_argument(
        "--duplicate-policy",
        choices=("rename", "skip", "error"),
        default="rename",
        help="how to handle an existing destination filename",
    )
    parser.add_argument(
        "--no-create-destinations",
        action="store_true",
        help="report missing category folders instead of creating them",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=file_organiser.DEFAULT_LOG_FILE,
        help="path for the rotating operation log",
    )
    return parser


def _print_report(report: dict[str, object]) -> None:
    """Print a compact organization summary."""
    print(f"Files processed: {file_organiser.count_processed(report)}")
    print(f"Moved: {len(report['moved'])}")
    print(f"Duplicate files skipped: {len(report['skipped_duplicates'])}")
    print(f"Unsupported: {len(report['unsupported'])}")
    print(f"Failed: {len(report['failed'])}")
    for path in report["moved"]:
        print(f"  MOVED -> {path}")
    for path in report["unsupported"]:
        print(f"  UNSUPPORTED -> {path}")


def run_demo() -> None:
    """Demonstrate categorization, movement, duplicates, and failures safely."""
    logger.debug(f"Starting safe temporary demonstration")
    with TemporaryDirectory(prefix="file_organiser_demo_") as temporary_directory:
        workspace = Path(temporary_directory)
        inbox = workspace / "Inbox"
        output = workspace / "Organized"
        inbox.mkdir()

        examples = {
            "photo.jpg": "image example",
            "notes.txt": "text example",
            "report.pdf": "document example",
            "data.csv": "name,score\nAda,100\n",
            "unknown.xyz": "unsupported example",
        }
        for filename, content in examples.items():
            (inbox / filename).write_text(content, encoding="utf-8")

        # Pre-existing file demonstrates safe duplicate renaming.
        (output / "Images").mkdir(parents=True)
        (output / "Images" / "photo.jpg").write_text("existing", encoding="utf-8")

        report = file_organiser.organize_folder(inbox, output)
        _print_report(report)

        try:
            file_organiser.move_file(inbox / "missing.txt", output / "Text")
        except FileNotFoundError as error:
            logger.error(f"Demonstrated missing-file handling: {error}", exc_info=True)

        try:
            file_organiser.move_file(
                output / "Text" / "notes.txt",
                output / "MissingDestination",
                create_destination=False,
            )
        except FileNotFoundError as error:
            logger.error(
                f"Demonstrated missing-destination handling: {error}",
                exc_info=True,
            )


def main() -> int:
    """Parse arguments, configure logging, and run the requested operation."""
    arguments = _build_parser().parse_args()
    log_path = file_organiser.configure_logging(arguments.log_file)
    logger.debug(f"File organizer started at DEBUG level; log file: {log_path}")

    try:
        if arguments.source is None:
            run_demo()
        else:
            report = file_organiser.organize_folder(
                arguments.source,
                arguments.output,
                create_destinations=not arguments.no_create_destinations,
                duplicate_policy=arguments.duplicate_policy,
            )
            _print_report(report)
        logger.info(f"File organizer finished")
        return 0
    except (
        FileNotFoundError,
        NotADirectoryError,
        PermissionError,
        OSError,
        ValueError,
    ):
        logger.critical(f"File organizer stopped", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
