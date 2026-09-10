import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import calculator_tools as calculator

logger = logging.getLogger(__name__)
LOG_FILE = Path(__file__).with_name("calculator_tools.log")


def configure_logging() -> None:
    """Configure detailed terminal and rotating file logging."""
    try:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.StreamHandler(), file_handler],
        )
        logger.debug(f"Logging configured at DEBUG level: {LOG_FILE}")
    except (OSError, ValueError):
        logger.error(f"Logging configuration failed: {LOG_FILE}", exc_info=True)
        raise


def demonstrate(label: str, function: object, *arguments: object) -> None:
    """Run one demonstration and handle its expected calculation errors."""
    try:
        if not callable(function):
            logger.warning(f"Demonstration target is not callable: {function!r}")
            raise TypeError("function must be callable")
        result = function(*arguments)
        print(f"{label}: {result}")
        logger.info(f"Demonstration succeeded: {label}")
    except (
        TypeError,
        ValueError,
        ZeroDivisionError,
        calculator.InvalidOperationError,
    ) as error:
        # Record the complete traceback once, at the application boundary.
        logger.error(f"{label}: {error}", exc_info=True)


def main() -> None:
    """Run successful examples and intentionally handled error examples."""
    configure_logging()
    logger.debug(f"Starting calculator_tools demonstration; log file: {LOG_FILE}")

    demonstrations = [
        ("Addition", calculator.add, 12, 4),
        ("Subtraction", calculator.subtract, 12, 4),
        ("Multiplication", calculator.multiply, 12, 4),
        ("Division", calculator.divide, 12, 4),
        ("25 is what percentage of 200", calculator.percentage, 25, 200),
        ("25 percent of 200", calculator.calculate_percentage, 200, 25),
        ("Average", calculator.average, [10, 20, 30, 40]),
        ("Celsius to Fahrenheit", calculator.convert_temperature, 25, "C", "F"),
        ("Fahrenheit to Celsius", calculator.fahrenheit_to_celsius, 77),
        ("Kilometres to miles", calculator.convert_unit, 5, "km", "mi"),
        ("Feet to metres", calculator.convert_length, 10, "ft", "m"),
        ("Named operation", calculator.calculate, "multiply", 6, 7),
    ]
    for label, function, *arguments in demonstrations:
        demonstrate(label, function, *arguments)

    print("\nHandled error examples (see log messages):")
    demonstrate("Division by zero", calculator.divide, 10, 0)
    demonstrate("Incorrect data type", calculator.add, "ten", 2)
    demonstrate("Invalid empty values", calculator.average, [])
    demonstrate("Below absolute zero", calculator.convert_temperature, -300, "C", "F")
    demonstrate("Unsupported operation", calculator.calculate, "power", 2, 3)
    demonstrate("Unsupported unit", calculator.convert_unit, 1, "kg", "m")

    logger.info(f"Calculator_tools demonstration finished")


if __name__ == "__main__":
    main()
