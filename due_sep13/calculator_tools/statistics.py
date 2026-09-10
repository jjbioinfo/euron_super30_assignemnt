"""Simple statistical functions."""

import logging
from collections.abc import Iterable

from ._validation import require_number

logger = logging.getLogger(__name__)


def average(values: object) -> float:
    """Return the arithmetic mean of a non-empty iterable of numbers."""
    try:
        logger.debug(f"Starting average calculation with values={values!r}")
        if isinstance(values, (str, bytes)) or not isinstance(values, Iterable):
            logger.warning(f"Average received a non-numeric iterable: {values!r}")
            raise TypeError("values must be an iterable of real numbers")

        validated_values = [
            require_number(value, f"values[{index}]")
            for index, value in enumerate(values)
        ]
        if not validated_values:
            logger.warning(f"Average received an empty collection")
            raise ValueError("cannot calculate the average of an empty collection")

        result = sum(validated_values) / len(validated_values)
        logger.debug(f"Average completed for {len(validated_values)} values: {result}")
        return result
    except (TypeError, ValueError):
        logger.error(f"Average calculation failed for values={values!r}")
        raise


def calculate_average(values: object) -> float:
    """Alias for :func:`average` with a descriptive name."""
    logger.debug(f"Starting calculate_average with values={values!r}")
    return average(values)
