"""Function-based tests for file_organiser."""

import logging
import tempfile
import traceback
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import file_organiser


def assert_raises(
    expected_exception: type[BaseException],
    function: Callable[..., object],
    *arguments: object,
    **keywords: object,
) -> None:
    try:
        function(*arguments, **keywords)
    except expected_exception:
        return
    except Exception as error:
        raise AssertionError(
            f"expected {expected_exception.__name__}, observed {type(error).__name__}"
        ) from error
    raise AssertionError(f"expected {expected_exception.__name__} to be raised")


def test_file_detection() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        expected = {
            "photo.JPG": "Images",
            "notes.txt": "Text",
            "report.pdf": "Documents",
            "data.csv": "Data",
        }
        for filename, category in expected.items():
            path = folder / filename
            path.touch()
            assert file_organiser.detect_file_category(path) == category

        unsupported = folder / "archive.unknown"
        unsupported.touch()
        assert_raises(
            file_organiser.UnsupportedFileError,
            file_organiser.detect_file_category,
            unsupported,
        )
        assert_raises(
            FileNotFoundError,
            file_organiser.detect_file_category,
            folder / "missing.txt",
        )
        assert_raises(TypeError, file_organiser.detect_file_category, None)


def test_move_and_destination_creation() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        source = folder / "notes.txt"
        source.write_text("test", encoding="utf-8")
        result = file_organiser.move_file(source, folder / "Text")
        assert result == folder / "Text" / "notes.txt"
        assert result.is_file()
        assert not source.exists()


def test_duplicate_policies() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        destination = folder / "Images"
        destination.mkdir()
        (destination / "photo.jpg").write_text("original", encoding="utf-8")

        source = folder / "photo.jpg"
        source.write_text("rename", encoding="utf-8")
        renamed = file_organiser.move_file(source, destination)
        assert renamed is not None and renamed.name == "photo_1.jpg"

        source.write_text("skip", encoding="utf-8")
        skipped = file_organiser.move_file(source, destination, duplicate_policy="skip")
        assert skipped is None and source.exists()
        assert_raises(
            FileExistsError,
            file_organiser.move_file,
            source,
            destination,
            duplicate_policy="error",
        )


def test_missing_paths() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        source = folder / "notes.txt"
        source.touch()
        assert_raises(
            FileNotFoundError,
            file_organiser.move_file,
            source,
            folder / "Missing",
            create_destination=False,
        )
        assert_raises(FileNotFoundError, file_organiser.move_file, folder / "absent.txt", folder)
        assert_raises(TypeError, file_organiser.move_file, None, folder)


def test_permission_error_and_failure_log() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        inbox = folder / "Inbox"
        output = folder / "Output"
        log_file = folder / "permission.log"
        inbox.mkdir()
        source = inbox / "notes.txt"
        source.touch()
        file_organiser.configure_logging(log_file, console=False)

        with patch(
            "file_organiser.file_mover.shutil.move",
            side_effect=PermissionError("permission denied"),
        ):
            report = file_organiser.organize_folder(inbox, output)

        for handler in logging.getLogger().handlers:
            handler.flush()
        log_contents = log_file.read_text(encoding="utf-8")
        assert len(report["failed"]) == 1
        assert "Failed to organize file" in log_contents
        assert "PermissionError: permission denied" in log_contents
        assert "Traceback" in log_contents


def test_complete_organization() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        inbox = folder / "Inbox"
        output = folder / "Output"
        log_file = folder / "operations.log"
        inbox.mkdir()
        (inbox / "photo.jpg").touch()
        (inbox / "notes.txt").touch()
        (inbox / "unsupported.xyz").touch()

        assert file_organiser.configure_logging(log_file, console=False) == log_file.resolve()
        report = file_organiser.organize_folder(inbox, output)
        for handler in logging.getLogger().handlers:
            handler.flush()

        assert len(report["moved"]) == 2
        assert len(report["unsupported"]) == 1
        assert file_organiser.count_processed(report) == 3
        assert (output / "Images" / "photo.jpg").exists()
        assert (output / "Text" / "notes.txt").exists()
        log_contents = log_file.read_text(encoding="utf-8")
        assert "Moved file successfully" in log_contents
        assert "unsupported file extension" in log_contents


def run_tests() -> int:
    tests = [
        test_file_detection,
        test_move_and_destination_creation,
        test_duplicate_policies,
        test_missing_paths,
        test_permission_error_and_failure_log,
        test_complete_organization,
    ]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception:
            failures += 1
            print(f"FAIL: {test.__name__}")
            traceback.print_exc()
    print(f"Ran {len(tests)} test groups; failures={failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(run_tests())
