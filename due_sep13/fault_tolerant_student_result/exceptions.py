"""Custom exceptions for student-result validation."""


class InvalidMarksError(Exception):
    """Raised when subject marks are missing, invalid, or outside 0–100."""

