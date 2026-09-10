"""Temperature and length conversion functions."""

import logging
from numbers import Real

from ._validation import require_number
from .exceptions import InvalidOperationError

logger = logging.getLogger(__name__)

_TEMPERATURE_UNITS = {
    "c": "celsius",
    "celsius": "celsius",
    "f": "fahrenheit",
    "fahrenheit": "fahrenheit",
    "k": "kelvin",
    "kelvin": "kelvin",
}

_LENGTH_IN_METRES = {
    "mm": 0.001,
    "millimeter": 0.001,
    "millimeters": 0.001,
    "cm": 0.01,
    "centimeter": 0.01,
    "centimeters": 0.01,
    "m": 1.0,
    "meter": 1.0,
    "meters": 1.0,
    "km": 1_000.0,
    "kilometer": 1_000.0,
    "kilometers": 1_000.0,
    "in": 0.0254,
    "inch": 0.0254,
    "inches": 0.0254,
    "ft": 0.3048,
    "foot": 0.3048,
    "feet": 0.3048,
    "yd": 0.9144,
    "yard": 0.9144,
    "yards": 0.9144,
    "mi": 1_609.344,
    "mile": 1_609.344,
    "miles": 1_609.344,
}


def _normalize_unit(unit: object, units: dict[str, object], kind: str) -> str:
    """Return a normalized, supported unit name."""
    if not isinstance(unit, str):
        logger.warning(f"{kind.title()} unit must be a string: {unit!r}")
        raise TypeError(f"{kind} unit must be a string")
    normalized_unit = unit.strip().lower().replace("°", "")
    if normalized_unit not in units:
        logger.warning(f"Unsupported {kind} unit: {unit!r}")
        raise InvalidOperationError(f"unsupported {kind} unit: {unit!r}")
    return normalized_unit


def convert_temperature(value: object, from_unit: object, to_unit: object) -> float:
    """Convert a temperature among Celsius, Fahrenheit, and Kelvin."""
    try:
        logger.debug(
            f"Starting temperature conversion: value={value!r}, "
            f"from={from_unit!r}, to={to_unit!r}"
        )
        temperature = require_number(value, "value")
        source_key = _normalize_unit(from_unit, _TEMPERATURE_UNITS, "temperature")
        target_key = _normalize_unit(to_unit, _TEMPERATURE_UNITS, "temperature")
        source = _TEMPERATURE_UNITS[source_key]
        target = _TEMPERATURE_UNITS[target_key]

        if source == "celsius":
            celsius = temperature
        elif source == "fahrenheit":
            celsius = (temperature - 32) * 5 / 9
        else:
            celsius = temperature - 273.15

        if celsius < -273.15:
            logger.warning(f"Temperature is below absolute zero: {celsius} Celsius")
            raise ValueError("temperature cannot be below absolute zero")

        if target == "celsius":
            result = celsius
        elif target == "fahrenheit":
            result = celsius * 9 / 5 + 32
        else:
            result = celsius + 273.15

        logger.debug(
            f"Temperature conversion completed: {value} {from_unit} = {result} {to_unit}"
        )
        return float(result)
    except (TypeError, ValueError, InvalidOperationError):
        logger.error(
            f"Temperature conversion failed: value={value!r}, "
            f"from={from_unit!r}, to={to_unit!r}"
        )
        raise


def celsius_to_fahrenheit(value: object) -> float:
    """Convert Celsius to Fahrenheit."""
    logger.debug(f"Starting Celsius-to-Fahrenheit conversion: value={value!r}")
    return convert_temperature(value, "celsius", "fahrenheit")


def fahrenheit_to_celsius(value: object) -> float:
    """Convert Fahrenheit to Celsius."""
    logger.debug(f"Starting Fahrenheit-to-Celsius conversion: value={value!r}")
    return convert_temperature(value, "fahrenheit", "celsius")


def convert_length(value: object, from_unit: object, to_unit: object) -> float:
    """Convert a length between metric and imperial units."""
    try:
        logger.debug(
            f"Starting length conversion: value={value!r}, "
            f"from={from_unit!r}, to={to_unit!r}"
        )
        length = require_number(value, "value")
        if length < 0:
            logger.warning(f"Length cannot be negative: {length}")
            raise ValueError("length cannot be negative")
        source = _normalize_unit(from_unit, _LENGTH_IN_METRES, "length")
        target = _normalize_unit(to_unit, _LENGTH_IN_METRES, "length")
        result = length * _LENGTH_IN_METRES[source] / _LENGTH_IN_METRES[target]
        logger.debug(
            f"Length conversion completed: {value} {from_unit} = {result} {to_unit}"
        )
        return float(result)
    except (TypeError, ValueError, InvalidOperationError):
        logger.error(
            f"Length conversion failed: value={value!r}, "
            f"from={from_unit!r}, to={to_unit!r}"
        )
        raise


def convert_unit(value: object, from_unit: object, to_unit: object) -> float:
    """Alias for :func:`convert_length` for simple unit conversion."""
    logger.debug(
        f"Starting unit conversion: value={value!r}, "
        f"from={from_unit!r}, to={to_unit!r}"
    )
    return convert_length(value, from_unit, to_unit)
