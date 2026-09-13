"""Reusable input validation functions."""

import logging
from math import isfinite

from .exceptions import InventoryError

logger = logging.getLogger(__name__)


def require_text(value: object, field_name: str) -> str:
    """Return stripped, non-empty text."""
    if not isinstance(value, str) or not value.strip():
        logger.warning(f"Invalid text: {field_name}={value!r}")
        raise InventoryError(f"{field_name} cannot be empty")
    return value.strip()


def require_non_negative_integer(value: object, field_name: str) -> int:
    """Return a whole number greater than or equal to zero."""
    if isinstance(value, bool):
        logger.warning(f"Invalid whole number: {field_name}={value!r}")
        raise InventoryError(f"{field_name} must be a whole number")
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError) as error:
        logger.warning(f"Invalid whole number: {field_name}={value!r}")
        raise InventoryError(f"{field_name} must be a whole number") from error
    if isinstance(value, float) and not value.is_integer():
        logger.warning(f"Fractional whole number: {field_name}={value!r}")
        raise InventoryError(f"{field_name} must be a whole number")
    if number < 0:
        logger.warning(f"Negative whole number: {field_name}={number}")
        raise InventoryError(f"{field_name} cannot be negative")
    return number


def require_non_negative_number(value: object, field_name: str) -> float:
    """Return a finite number greater than or equal to zero."""
    if isinstance(value, bool):
        logger.warning(f"Invalid number: {field_name}={value!r}")
        raise InventoryError(f"{field_name} must be numeric")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        logger.warning(f"Invalid number: {field_name}={value!r}")
        raise InventoryError(f"{field_name} must be numeric") from error
    if not isfinite(number) or number < 0:
        logger.warning(f"Invalid number range: {field_name}={number!r}")
        raise InventoryError(f"{field_name} must be finite and non-negative")
    return number
