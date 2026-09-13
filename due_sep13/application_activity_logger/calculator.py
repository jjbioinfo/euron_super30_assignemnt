"""Calculator activity functions."""

import logging
from math import isfinite

logger = logging.getLogger(__name__)


def validate_number(value: object, name: str) -> float:
    """Return a finite number or raise a validation error."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        logger.warning(f"Calculator value is not numeric: {name}={value!r}")
        raise TypeError(f"{name} must be numeric")
    if not isfinite(value):
        logger.warning(f"Calculator value is not finite: {name}={value!r}")
        raise ValueError(f"{name} must be finite")
    return float(value)


def calculate(first: object, operation: object, second: object) -> float:
    """Perform addition, subtraction, multiplication, or division."""
    logger.debug(
        f"Calculation requested: first={first!r}, operation={operation!r}, "
        f"second={second!r}"
    )
    left = validate_number(first, "first")
    right = validate_number(second, "second")
    if not isinstance(operation, str):
        logger.warning(f"Calculator operation is not text: {operation!r}")
        raise TypeError("operation must be a string")

    operation = operation.strip().lower()
    if operation in {"+", "add"}:
        result = left + right
    elif operation in {"-", "subtract"}:
        result = left - right
    elif operation in {"*", "multiply"}:
        result = left * right
    elif operation in {"/", "divide"}:
        if right == 0:
            logger.warning(f"Division by zero was rejected")
            raise ZeroDivisionError("cannot divide by zero")
        result = left / right
    else:
        logger.warning(f"Unsupported calculator operation: {operation!r}")
        raise ValueError(f"unsupported operation: {operation!r}")

    if not isfinite(result):
        logger.warning(f"Calculation produced a non-finite result: {result!r}")
        raise ArithmeticError("calculation produced a non-finite result")

    logger.info(f"Calculation completed: {left} {operation} {right} = {result}")
    return result
