"""Initialize the calculator_tools package and define its public interface."""

import logging

# Re-export the supported operations as a stable package-level API.
from .arithmetic import (
    add,
    calculate,
    calculate_percentage,
    divide,
    multiply,
    percentage,
    subtract,
)
from .converter import (
    celsius_to_fahrenheit,
    convert_length,
    convert_temperature,
    convert_unit,
    fahrenheit_to_celsius,
)
from .exceptions import InvalidOperationError
from .statistics import average, calculate_average

# Declare the package's public API.
__all__ = [
    "InvalidOperationError",
    "add",
    "average",
    "calculate",
    "calculate_average",
    "calculate_percentage",
    "celsius_to_fahrenheit",
    "convert_length",
    "convert_temperature",
    "convert_unit",
    "divide",
    "fahrenheit_to_celsius",
    "multiply",
    "percentage",
    "subtract",
]

# Package release version.
__version__ = "1.0.0"

# Leave logging configuration to the consuming application.
logging.getLogger(__name__).addHandler(logging.NullHandler())

