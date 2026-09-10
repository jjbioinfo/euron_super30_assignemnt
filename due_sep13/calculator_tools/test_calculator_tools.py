"""Function-based tests for calculator_tools."""

import math
import traceback
from collections.abc import Callable

import calculator_tools as calculator


def assert_equal(actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(f"expected {expected!r}, observed {actual!r}")


def assert_almost_equal(actual: float, expected: float, tolerance: float = 1e-9) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise AssertionError(f"expected approximately {expected}, observed {actual}")


def assert_raises(
    expected_exception: type[BaseException],
    function: Callable[..., object],
    *arguments: object,
    **keywords: object,
) -> None:
    try:
        function(*arguments, **keywords)
    except expected_exception:
        return
    except Exception as error:
        raise AssertionError(
            f"expected {expected_exception.__name__}, observed {type(error).__name__}"
        ) from error
    raise AssertionError(f"expected {expected_exception.__name__} to be raised")


def test_arithmetic_normal_cases() -> None:
    assert_equal(calculator.add(2, 3), 5)
    assert_equal(calculator.subtract(7, 2), 5)
    assert_equal(calculator.multiply(4, 2.5), 10)
    assert_equal(calculator.divide(9, 3), 3)


def test_percentages() -> None:
    assert_equal(calculator.percentage(25, 200), 12.5)
    assert_equal(calculator.calculate_percentage(200, 25), 50)
    assert_raises(ZeroDivisionError, calculator.percentage, 25, 0)


def test_arithmetic_errors() -> None:
    assert_raises(ZeroDivisionError, calculator.divide, 10, 0)
    assert_raises(calculator.InvalidOperationError, calculator.calculate, "power", 2, 3)
    for value in (True, "2", None, math.inf, math.nan):
        expected = ValueError if isinstance(value, float) else TypeError
        assert_raises(expected, calculator.add, value, 2)


def test_average() -> None:
    assert_equal(calculator.average(number for number in [2, 4, 6]), 4)
    assert_raises(ValueError, calculator.average, [])
    assert_raises(TypeError, calculator.average, [1, "two", 3])


def test_temperature_conversion() -> None:
    assert_almost_equal(calculator.convert_temperature(0, "C", "F"), 32)
    assert_almost_equal(calculator.convert_temperature(32, "F", "C"), 0)
    assert_almost_equal(calculator.convert_temperature(0, "K", "C"), -273.15)
    assert_raises(ValueError, calculator.convert_temperature, -0.01, "K", "C")
    assert_raises(TypeError, calculator.convert_temperature, "hot", "C", "F")
    assert_raises(
        calculator.InvalidOperationError,
        calculator.convert_temperature,
        20,
        "C",
        "Rankine",
    )


def test_length_conversion() -> None:
    assert_almost_equal(calculator.convert_unit(1, "mile", "km"), 1.609344)
    assert_equal(calculator.convert_length(0, "m", "ft"), 0)
    assert_raises(ValueError, calculator.convert_length, -1, "m", "cm")
    assert_raises(calculator.InvalidOperationError, calculator.convert_unit, 1, "kg", "m")


def run_tests() -> int:
    tests = [
        test_arithmetic_normal_cases,
        test_percentages,
        test_arithmetic_errors,
        test_average,
        test_temperature_conversion,
        test_length_conversion,
    ]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception:
            failures += 1
            print(f"FAIL: {test.__name__}")
            traceback.print_exc()
    print(f"Ran {len(tests)} test groups; failures={failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(run_tests())

