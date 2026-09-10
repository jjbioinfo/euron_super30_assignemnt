"""Arithmetic and percentage functions."""

import logging
from collections.abc import Callable
from numbers import Real

from ._validation import require_number
from .exceptions import InvalidOperationError

logger = logging.getLogger(__name__)


def add(a: object, b: object) -> Real:
    """Return the sum of two finite real numbers."""
    try:
        logger.debug(f"Starting addition with a={a!r}, b={b!r}")
        result = require_number(a, "a") + require_number(b, "b")
        logger.debug(f"Addition completed: {a} + {b} = {result}")
        return result
    except (TypeError, ValueError):
        logger.error(f"Addition failed for a={a!r} and b={b!r}")
        raise


def subtract(a: object, b: object) -> Real:
    """Return *b* subtracted from *a*."""
    try:
        logger.debug(f"Starting subtraction with a={a!r}, b={b!r}")
        result = require_number(a, "a") - require_number(b, "b")
        logger.debug(f"Subtraction completed: {a} - {b} = {result}")
        return result
    except (TypeError, ValueError):
        logger.error(f"Subtraction failed for a={a!r} and b={b!r}")
        raise


def multiply(a: object, b: object) -> Real:
    """Return the product of two finite real numbers."""
    try:
        logger.debug(f"Starting multiplication with a={a!r}, b={b!r}")
        result = require_number(a, "a") * require_number(b, "b")
        logger.debug(f"Multiplication completed: {a} * {b} = {result}")
        return result
    except (TypeError, ValueError):
        logger.error(f"Multiplication failed for a={a!r} and b={b!r}")
        raise


def divide(a: object, b: object) -> Real:
    """Return *a* divided by *b*.

    Raises:
        ZeroDivisionError: If *b* is zero.
    """
    try:
        logger.debug(f"Starting division with a={a!r}, b={b!r}")
        dividend = require_number(a, "a")
        divisor = require_number(b, "b")
        if divisor == 0:
            logger.warning(f"Division rejected because divisor is zero: b={b!r}")
            raise ZeroDivisionError("cannot divide by zero")
        result = dividend / divisor
        logger.debug(f"Division completed: {a} / {b} = {result}")
        return result
    except (TypeError, ValueError, ZeroDivisionError):
        logger.error(f"Division failed for a={a!r} and b={b!r}")
        raise


def percentage(part: object, whole: object) -> float:
    """Return *part* as a percentage of *whole*.

    For example, ``percentage(25, 200)`` returns ``12.5``.
    """
    try:
        logger.debug(f"Starting percentage with part={part!r}, whole={whole!r}")
        numerator = require_number(part, "part")
        denominator = require_number(whole, "whole")
        if denominator == 0:
            logger.warning(f"Percentage rejected because whole is zero: whole={whole!r}")
            raise ZeroDivisionError("whole cannot be zero")
        result = numerator / denominator * 100
        logger.debug(f"Percentage completed: {part} of {whole} = {result}%")
        return result
    except (TypeError, ValueError, ZeroDivisionError):
        logger.error(
            f"Percentage failed for part={part!r} and whole={whole!r}"
        )
        raise


def calculate_percentage(value: object, percent: object) -> float:
    """Return *percent* percent of *value*.

    For example, ``calculate_percentage(200, 25)`` returns ``50.0``. Use
    :func:`percentage` instead to determine what percentage a part is of a
    whole.
    """
    try:
        logger.debug(
            f"Starting percentage amount with value={value!r}, percent={percent!r}"
        )
        number = require_number(value, "value")
        percentage_value = require_number(percent, "percent")
        result = number * percentage_value / 100
        logger.debug(f"Percentage amount completed: {percent}% of {value} = {result}")
        return result
    except (TypeError, ValueError):
        logger.error(
            f"Percentage amount failed for value={value!r} and percent={percent!r}"
        )
        raise


def calculate(operation: object, a: object, b: object) -> Real:
    """Apply a named arithmetic operation to *a* and *b*.

    Supported names are ``add``, ``subtract``, ``multiply``, ``divide``, and
    ``percentage``. Common mathematical symbols are accepted too.
    """
    logger.debug(
        f"Starting calculation with operation={operation!r}, a={a!r}, b={b!r}"
    )
    if not isinstance(operation, str):
        logger.warning(
            f"Operation must be a string, received {type(operation).__name__}"
        )
        raise TypeError("operation must be a string")

    operations: dict[str, Callable[[object, object], Real]] = {
        "add": add,
        "+": add,
        "subtract": subtract,
        "-": subtract,
        "multiply": multiply,
        "*": multiply,
        "divide": divide,
        "/": divide,
        "percentage": percentage,
        "%": percentage,
    }
    normalized_operation = operation.strip().lower()
    try:
        function = operations[normalized_operation]
    except KeyError as error:
        logger.warning(f"Unsupported arithmetic operation: {operation!r}")
        raise InvalidOperationError(
            f"unsupported arithmetic operation: {operation!r}"
        ) from error
    return function(a, b)
