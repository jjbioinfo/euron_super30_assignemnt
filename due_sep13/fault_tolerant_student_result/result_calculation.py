"""Calculate totals, percentages, grades, and pass/fail status."""

import logging
from math import isfinite

logger = logging.getLogger(__name__)
PASS_MARK = 40.0
MAXIMUM_TOTAL = 500.0


def _require_number(value: object, name: str) -> float:
    """Return a finite number or raise a validation error."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        logger.warning(f"{name} is not numeric: {value!r}")
        raise TypeError(f"{name} must be numeric")
    if not isfinite(value):
        logger.warning(f"{name} is not finite: {value!r}")
        raise ValueError(f"{name} must be finite")
    return float(value)


def calculate_total(marks: object) -> float:
    """Validate five subject marks and return their total."""
    # Import here to avoid a circular module import: student_operations also
    # imports calculate_result when it processes a validated student.
    from .student_operations import validate_marks

    validated_marks = validate_marks(marks)
    total = float(sum(validated_marks))
    logger.debug(f"Calculated total: {total}")
    return total


def calculate_percentage(total: object, maximum_total: object = MAXIMUM_TOTAL) -> float:
    """Return the percentage for a total and maximum possible total."""
    numeric_total = _require_number(total, "total")
    numeric_maximum = _require_number(maximum_total, "maximum_total")
    if numeric_maximum == 0:
        logger.warning(f"Cannot calculate percentage with a zero maximum total")
        raise ZeroDivisionError("maximum_total cannot be zero")
    return numeric_total / numeric_maximum * 100


def calculate_grade(percentage: object) -> str:
    """Return a grade for a percentage between 0 and 100."""
    value = _require_number(percentage, "percentage")
    if not 0 <= value <= 100:
        logger.warning(f"Percentage is outside 0-100: {value}")
        raise ValueError("percentage must be between 0 and 100")
    if value >= 90:
        return "A+"
    if value >= 80:
        return "A"
    if value >= 70:
        return "B"
    if value >= 60:
        return "C"
    if value >= 50:
        return "D"
    if value >= 40:
        return "E"
    return "F"


def determine_status(marks: list[float], pass_mark: float = PASS_MARK) -> str:
    """Return Pass only when every subject mark meets the pass mark."""
    return "Pass" if all(mark >= pass_mark for mark in marks) else "Fail"


def calculate_result(student: dict[str, object]) -> dict[str, object]:
    """Calculate a complete result for an already validated student."""
    marks = student["marks"]
    total = calculate_total(marks)
    percentage = calculate_percentage(total)
    return {
        **student,
        "total": total,
        "percentage": percentage,
        "grade": calculate_grade(percentage),
        "status": determine_status(marks),
    }
