"""Custom exceptions for the file_organiser package."""


class UnsupportedFileError(Exception):
    """Raised when a file extension has no configured category."""
