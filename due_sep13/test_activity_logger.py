"""Function-based tests for the application activity logger."""

import logging
import tempfile
import traceback
from collections.abc import Callable
from pathlib import Path

import application_activity_logger as activity_logger
from application_activity_logger.main import run_demo


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


def test_login_and_logout() -> None:
    session: dict[str, object] = {"username": None, "logged_in": False}
    assert activity_logger.login_user(session, " Ada ") == "Ada"
    assert session["logged_in"] is True
    assert_raises(PermissionError, activity_logger.login_user, session, "Grace")
    assert activity_logger.logout_user(session) == "Ada"
    assert session["logged_in"] is False


def test_calculator() -> None:
    assert activity_logger.calculate(10, "+", 5) == 15
    assert activity_logger.calculate(10, "/", 4) == 2.5
    assert_raises(ZeroDivisionError, activity_logger.calculate, 10, "/", 0)
    assert_raises(ValueError, activity_logger.calculate, 10, "power", 2)
    assert_raises(TypeError, activity_logger.calculate, "ten", "+", 2)


def test_file_operations() -> None:
    with tempfile.TemporaryDirectory() as directory:
        folder = Path(directory)
        path = activity_logger.write_file(folder / "notes.txt", "hello")
        assert activity_logger.read_file(path) == "hello"
        activity_logger.write_file(path, " world", append=True)
        assert activity_logger.read_file(path) == "hello world"
        empty_file = folder / "empty.txt"
        empty_file.touch()
        assert activity_logger.read_file(empty_file) == ""
        assert_raises(FileNotFoundError, activity_logger.read_file, folder / "missing.txt")


def test_menu_continues_after_error() -> None:
    inputs = iter(["1", "Ada", "2", "10", "/", "0", "2", "10", "+", "5", "5"])
    outputs: list[str] = []

    def provide_input(prompt: str) -> str:
        return next(inputs)

    def capture_output(message: str) -> None:
        outputs.append(message)

    assert activity_logger.run_menu(provide_input, capture_output) == 0
    assert any("Activity failed" in message for message in outputs)
    assert "Result: 15.0" in outputs
    assert outputs[-1] == "Application closed"


def test_log_routing_and_all_levels() -> None:
    with tempfile.TemporaryDirectory() as directory:
        log_paths = activity_logger.configure_logging(directory, console=False)
        run_demo()
        for handler in logging.getLogger().handlers:
            handler.flush()

        application_log = log_paths["application"].read_text(encoding="utf-8")
        error_log = log_paths["error"].read_text(encoding="utf-8")
        for level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            assert level in application_log
        assert "ERROR" in error_log
        assert "CRITICAL" in error_log
        assert "Traceback" in error_log
        assert "DEBUG" not in error_log
        assert "INFO" not in error_log
        assert "WARNING" not in error_log


def run_tests() -> int:
    tests = [
        test_login_and_logout,
        test_calculator,
        test_file_operations,
        test_menu_continues_after_error,
        test_log_routing_and_all_levels,
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
