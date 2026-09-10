"""Shared validation helpers for calculator modules."""

import logging
from math import isfinite
from numbers import Real

logger = logging.getLogger(__name__)


def require_number(value: object, name: str = "value") -> Real:
    """Return *value* when it is a finite real number.

    ``bool`` is deliberately rejected even though it is an ``int`` subclass;
    accepting ``True`` as the number 1 would usually hide an input mistake.
    """
    logger.debug(f"Validating numeric input: {name}={value!r}")
    if isinstance(value, bool) or not isinstance(value, Real):
        logger.warning(
            f"Invalid numeric type: {name} has type {type(value).__name__}"
        )
        raise TypeError(
            f"{name} must be a real number, not {type(value).__name__}"
        )
    try:
        finite = isfinite(value)
    except OverflowError as error:
        logger.warning(f"Numeric input is too large: {name}={value!r}")
        raise ValueError(f"{name} is too large to validate") from error
    if not finite:
        logger.warning(f"Numeric input is not finite: {name}={value!r}")
        raise ValueError(f"{name} must be finite")
    logger.debug(f"Numeric input accepted: {name}={value!r}")
    return value
