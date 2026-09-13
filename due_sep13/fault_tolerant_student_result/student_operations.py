"""Load, validate, and process student records."""

import json
import logging
from pathlib import Path

from .exceptions import InvalidMarksError
from .result_calculation import calculate_result

logger = logging.getLogger(__name__)
SUBJECT_COUNT = 5


def validate_marks(marks: object) -> list[float]:
    """Return five validated marks between 0 and 100."""
    logger.debug(f"Validating marks: {marks!r}")

    if not isinstance(marks, list) or len(marks) != SUBJECT_COUNT:
        logger.warning(f"Exactly five marks are required: {marks!r}")
        raise InvalidMarksError("exactly five subject marks are required")

    validated_marks: list[float] = []
    for subject, mark in enumerate(marks, start=1):
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            logger.warning(f"Subject {subject} mark is not numeric: {mark!r}")
            raise InvalidMarksError(f"subject {subject} mark must be numeric")
        if not 0 <= mark <= 100:
            logger.warning(f"Subject {subject} mark is outside 0-100: {mark!r}")
            raise InvalidMarksError(
                f"subject {subject} mark must be between 0 and 100"
            )
        validated_marks.append(float(mark))

    return validated_marks


def validate_student(student: object) -> dict[str, object]:
    """Return a student record after validating its required information."""
    logger.debug(f"Validating student record: {student!r}")

    if not isinstance(student, dict):
        logger.warning(f"Student record is not a dictionary: {student!r}")
        raise TypeError("student record must be a dictionary")

    missing = [key for key in ("student_id", "name", "marks") if key not in student]
    if missing:
        logger.warning(f"Student information is missing: {missing!r}")
        raise ValueError(f"missing student information: {', '.join(missing)}")

    student_id = student["student_id"]
    name = student["name"]
    if isinstance(student_id, bool) or not isinstance(student_id, (str, int)):
        logger.warning(f"Student ID is invalid: {student_id!r}")
        raise ValueError("student_id must be a string or integer")
    if not str(student_id).strip():
        logger.warning(f"Student ID is empty")
        raise ValueError("student_id cannot be empty")
    if not isinstance(name, str) or not name.strip():
        logger.warning(f"Student name is missing or empty: {name!r}")
        raise ValueError("student name must be a non-empty string")

    return {
        "student_id": student_id,
        "name": name.strip(),
        "marks": validate_marks(student["marks"]),
    }


def process_student(student: object) -> dict[str, object]:
    """Validate one student and calculate the student's result."""
    validated_student = validate_student(student)
    result = calculate_result(validated_student)
    logger.info(f"Student processed successfully: {result['student_id']!r}")
    return result


def process_students(students: object) -> dict[str, list[dict[str, object]]]:
    """Process every student, logging invalid records and continuing."""
    if not isinstance(students, list):
        logger.warning(f"Student collection must be a list: {students!r}")
        raise TypeError("students must be provided as a list")

    results: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    logger.debug(f"Processing {len(students)} student records")

    for record_number, student in enumerate(students, start=1):
        try:
            results.append(process_student(student))
        except (InvalidMarksError, TypeError, ValueError, ArithmeticError) as error:
            errors.append(
                {"record": record_number, "student": student, "error": str(error)}
            )
            logger.error(
                f"Skipping invalid student record {record_number}: {error}",
                exc_info=True,
            )

    logger.info(
        f"Processing finished: successful={len(results)}, failed={len(errors)}"
    )
    return {"results": results, "errors": errors}


def load_students(file_path: str | Path) -> list[object]:
    """Load a list of student records from a JSON file."""
    path = Path(file_path)
    logger.debug(f"Loading student records from {path}")

    if not path.exists():
        logger.warning(f"Student file does not exist: {path}")
        raise FileNotFoundError(f"student file does not exist: {path}")

    try:
        with path.open("r", encoding="utf-8") as input_file:
            students = json.load(input_file)
    except json.JSONDecodeError:
        logger.warning(f"Student file contains invalid JSON: {path}")
        raise

    if not isinstance(students, list):
        logger.warning(f"Student JSON must contain a list: {path}")
        raise ValueError("student JSON must contain a list of records")

    logger.info(f"Loaded {len(students)} student records from {path}")
    return students
