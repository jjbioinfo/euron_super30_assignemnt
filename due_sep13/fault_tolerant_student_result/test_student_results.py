"""Function-based tests for the student-result processor."""

import json
import logging
import tempfile
import traceback
from collections.abc import Callable
from pathlib import Path

import fault_tolerant_student_result as student_results


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


def test_marks_validation() -> None:
    assert student_results.validate_marks([0, 25, 50, 75, 100]) == [0, 25, 50, 75, 100]
    assert_raises(student_results.InvalidMarksError, student_results.validate_marks, [1, 2])
    assert_raises(
        student_results.InvalidMarksError,
        student_results.validate_marks,
        [90, "absent", 80, 70, 60],
    )
    assert_raises(
        student_results.InvalidMarksError,
        student_results.validate_marks,
        [90, 101, 80, 70, 60],
    )


def test_missing_student_information() -> None:
    assert_raises(
        ValueError,
        student_results.validate_student,
        {"student_id": "S1", "marks": [50, 60, 70, 80, 90]},
    )
    assert_raises(
        ValueError,
        student_results.validate_student,
        {"student_id": "S1", "name": " ", "marks": [50, 60, 70, 80, 90]},
    )


def test_result_calculations() -> None:
    marks = [90, 80, 70, 60, 50]
    assert student_results.calculate_total(marks) == 350
    assert_raises(
        student_results.InvalidMarksError,
        student_results.calculate_total,
        [90, "absent", 70, 60, 50],
    )
    assert_raises(
        student_results.InvalidMarksError,
        student_results.calculate_total,
        [90, 101, 70, 60, 50],
    )
    assert_raises(
        student_results.InvalidMarksError,
        student_results.calculate_total,
        [90, 80, 70, 60],
    )
    assert student_results.calculate_percentage(350) == 70
    assert student_results.calculate_grade(90) == "A+"
    assert student_results.calculate_grade(40) == "E"
    assert student_results.determine_status(marks) == "Pass"
    assert student_results.determine_status([90, 80, 35, 95, 100]) == "Fail"
    assert_raises(ZeroDivisionError, student_results.calculate_percentage, 100, 0)


def test_fault_tolerant_batch() -> None:
    students = [
        {"student_id": "S1", "name": "Valid One", "marks": [80, 70, 60, 90, 75]},
        {"student_id": "S2", "name": "Invalid", "marks": [80, 101, 60, 90, 75]},
        {"student_id": "S3", "name": "Valid Two", "marks": [50, 55, 60, 65, 70]},
    ]
    report = student_results.process_students(students)
    assert len(report["results"]) == 2
    assert len(report["errors"]) == 1
    assert report["results"][1]["student_id"] == "S3"


def test_json_loading() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        folder = Path(temporary_directory)
        valid_file = folder / "students.json"
        invalid_file = folder / "invalid.json"
        valid_file.write_text(json.dumps([{"student_id": "S1"}]), encoding="utf-8")
        invalid_file.write_text("not valid JSON", encoding="utf-8")
        assert len(student_results.load_students(valid_file)) == 1
        assert_raises(ValueError, student_results.load_students, invalid_file)
        assert_raises(FileNotFoundError, student_results.load_students, folder / "missing.json")


def test_failure_logging() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        log_file = Path(temporary_directory) / "student_test.log"
        student_results.configure_logging(log_file, console=False)
        report = student_results.process_students(
            [{"student_id": "S1", "name": "Invalid", "marks": [50, 60, 200, 70, 80]}]
        )
        for handler in logging.getLogger().handlers:
            handler.flush()
        contents = log_file.read_text(encoding="utf-8")
        assert len(report["errors"]) == 1
        assert "Skipping invalid student record" in contents
        assert "InvalidMarksError" in contents
        assert "Traceback" in contents


def run_tests() -> int:
    tests = [
        test_marks_validation,
        test_missing_student_information,
        test_result_calculations,
        test_fault_tolerant_batch,
        test_json_loading,
        test_failure_logging,
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
