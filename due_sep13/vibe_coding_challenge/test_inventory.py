"""Function-based tests for the Simple Inventory Manager."""

import logging
import tempfile
import traceback
from collections.abc import Callable
from pathlib import Path

from inventory_app import (
    InventoryError,
    add_product,
    configure_logging,
    create_product,
    find_product,
    get_low_stock_products,
    get_total_value,
    load_inventory,
    remove_product,
    save_inventory,
    search_products,
    update_stock,
)
from inventory_app.cli import run_cli
from inventory_app.logging_config import LOG_FILE


def assert_raises(
    expected_exception: type[BaseException],
    function: Callable[..., object],
    *arguments: object,
) -> None:
    """Confirm that a function raises the expected exception."""
    try:
        function(*arguments)
    except expected_exception:
        return
    except Exception as error:
        raise AssertionError(
            f"expected {expected_exception.__name__}, got {type(error).__name__}"
        ) from error
    raise AssertionError(f"expected {expected_exception.__name__}")


def test_inventory_operations() -> None:
    products: list[dict[str, object]] = []
    pen = create_product("P1", "Pen", "Stationery", 3, 1.5, 3)
    add_product(products, pen)
    assert find_product(products, "p1") is pen
    assert search_products(products, "station") == [pen]
    assert get_low_stock_products(products) == [pen]
    assert get_total_value(products) == 4.5
    assert update_stock(products, "P1", 2) == 5
    assert update_stock(products, "P1", -1) == 4
    assert remove_product(products, "P1") is pen
    assert products == []


def test_invalid_operations() -> None:
    products: list[dict[str, object]] = []
    pen = create_product("P1", "Pen", "Stationery", 2, 1.5, 3)
    add_product(products, pen)
    assert_raises(InventoryError, add_product, products, pen)
    assert_raises(InventoryError, create_product, "P2", "", "Books", 1, 2)
    assert_raises(InventoryError, create_product, "P2", "Book", "Books", -1, 2)
    assert_raises(InventoryError, create_product, "P2", "Book", "Books", True, 2)
    assert_raises(InventoryError, create_product, "P2", "Book", "Books", 1, "free")
    assert_raises(
        InventoryError, create_product, "P2", "Book", "Books", 1, float("nan")
    )
    assert_raises(InventoryError, update_stock, products, "P1", 1.5)
    assert_raises(InventoryError, update_stock, products, "P1", -3)
    assert_raises(InventoryError, find_product, products, "missing")


def test_storage() -> None:
    with tempfile.TemporaryDirectory() as directory:
        folder = Path(directory)
        path = folder / "inventory.json"
        assert load_inventory(path) == []
        products = [create_product("P1", "Pen", "Stationery", 2, 1.5)]
        assert save_inventory(path, products) == path
        assert load_inventory(path) == products
        assert_raises(InventoryError, save_inventory, folder, products)
        path.write_text("not valid json", encoding="utf-8")
        assert_raises(InventoryError, load_inventory, path)


def test_cli_continues_after_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        data_file = Path(directory) / "inventory.json"
        inputs = iter(
            [
                "1", "P1", "Pen", "Stationery", "2", "1.5", "3",
                "1", "P1", "Pencil", "Stationery", "4", "1.0", "2",
                "7", "8",
            ]
        )
        outputs: list[str] = []
        result = run_cli(data_file, lambda prompt: next(inputs), outputs.append)
        assert result == 0
        assert any(message.startswith("Error:") for message in outputs)
        assert "Products: 1" in outputs
        assert outputs[-1] == "Inventory saved. Goodbye."
        assert len(load_inventory(data_file)) == 1


def test_logging() -> None:
    for handler in logging.getLogger().handlers:
        handler.flush()
    content = LOG_FILE.read_text(encoding="utf-8")
    assert "DEBUG" in content
    assert "INFO" in content
    assert "WARNING" in content
    assert "ERROR" in content


def run_tests() -> int:
    """Run each test group and return the number of failures."""
    configure_logging()
    tests = [
        test_inventory_operations,
        test_invalid_operations,
        test_storage,
        test_cli_continues_after_error,
        test_logging,
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
