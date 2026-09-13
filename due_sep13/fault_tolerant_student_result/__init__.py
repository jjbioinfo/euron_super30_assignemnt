"""Public interface for the fault-tolerant student-result processor."""

import logging

from .exceptions import InvalidMarksError
from .logging_config import DEFAULT_LOG_FILE, configure_logging
from .result_calculation import (
    PASS_MARK,
    calculate_grade,
    calculate_percentage,
    calculate_result,
    calculate_total,
    determine_status,
)
from .student_operations import (
    SUBJECT_COUNT,
    load_students,
    process_student,
    process_students,
    validate_marks,
    validate_student,
)

__all__ = [
    "DEFAULT_LOG_FILE",
    "InvalidMarksError",
    "PASS_MARK",
    "SUBJECT_COUNT",
    "calculate_grade",
    "calculate_percentage",
    "calculate_result",
    "calculate_total",
    "configure_logging",
    "determine_status",
    "load_students",
    "process_student",
    "process_students",
    "validate_marks",
    "validate_student",
]

__version__ = "1.0.0"

logging.getLogger(__name__).addHandler(logging.NullHandler())
