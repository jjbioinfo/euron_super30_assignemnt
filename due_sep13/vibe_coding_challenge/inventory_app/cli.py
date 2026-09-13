"""Command-line menu for the Simple Inventory Manager."""

import logging
from collections.abc import Callable
from pathlib import Path

from .exceptions import InventoryError
from .inventory import (
    add_product,
    create_product,
    get_low_stock_products,
    get_total_value,
    remove_product,
    search_products,
    update_stock,
)
from .storage import load_inventory, save_inventory
from .validators import require_non_negative_integer

logger = logging.getLogger(__name__)

MENU = """
1. Add product
2. List products
3. Search products
4. Restock product
5. Sell product
6. Remove product
7. Inventory summary
8. Save and exit
"""


def display_products(
    products: list[dict[str, object]],
    output_function: Callable[[str], object] = print,
) -> None:
    """Display products as a simple table."""
    if not products:
        output_function("No products found.")
        return
    output_function("ID | Name | Category | Quantity | Price")
    for product in products:
        output_function(
            f"{product['product_id']} | {product['name']} | "
            f"{product['category']} | {product['quantity']} | "
            f"{float(product['price']):.2f}"
        )


def require_positive_quantity(value: object, field_name: str) -> int:
    """Return a positive quantity for restocking or selling."""
    quantity = require_non_negative_integer(value, field_name)
    if quantity == 0:
        logger.warning(f"Zero quantity rejected: {field_name}")
        raise InventoryError(f"{field_name} must be greater than zero")
    return quantity


def run_cli(
    data_file: str | Path,
    input_function: Callable[[str], str] = input,
    output_function: Callable[[str], object] = print,
) -> int:
    """Run the menu and continue after recoverable operation errors."""
    products = load_inventory(data_file)
    logger.debug(f"Inventory menu started")

    try:
        while True:
            try:
                output_function(MENU)
                choice = input_function("Choose an option: ").strip()
                logger.debug(f"Menu choice: {choice!r}")

                if choice == "1":
                    product = create_product(
                        input_function("Product ID: "),
                        input_function("Name: "),
                        input_function("Category: "),
                        input_function("Quantity: "),
                        input_function("Unit price: "),
                        input_function("Low-stock limit: "),
                    )
                    add_product(products, product)
                    output_function("Product added.")
                elif choice == "2":
                    display_products(products, output_function)
                elif choice == "3":
                    matches = search_products(products, input_function("Search: "))
                    display_products(matches, output_function)
                elif choice == "4":
                    product_id = input_function("Product ID: ")
                    quantity = require_positive_quantity(
                        input_function("Quantity to add: "), "quantity to add"
                    )
                    new_quantity = update_stock(products, product_id, quantity)
                    output_function(f"New quantity: {new_quantity}")
                elif choice == "5":
                    product_id = input_function("Product ID: ")
                    quantity = require_positive_quantity(
                        input_function("Quantity to sell: "), "quantity to sell"
                    )
                    remaining = update_stock(products, product_id, -quantity)
                    output_function(f"Remaining quantity: {remaining}")
                elif choice == "6":
                    removed = remove_product(
                        products, input_function("Product ID: ")
                    )
                    output_function(f"Removed: {removed['name']}")
                elif choice == "7":
                    low_stock = get_low_stock_products(products)
                    output_function(f"Products: {len(products)}")
                    output_function(f"Total value: {get_total_value(products):.2f}")
                    output_function(f"Low-stock products: {len(low_stock)}")
                elif choice == "8":
                    return 0
                else:
                    logger.warning(f"Invalid menu choice: {choice!r}")
                    output_function("Invalid option. Enter a number from 1 to 8.")
            except (InventoryError, TypeError, ValueError, OSError) as error:
                logger.error(f"Inventory activity failed: {error}", exc_info=True)
                output_function(f"Error: {error}")
    except (EOFError, KeyboardInterrupt):
        logger.warning(f"Input ended; inventory will be saved")
        output_function("\nInput ended.")
        return 0
    finally:
        save_inventory(data_file, products)
        logger.debug(f"Inventory menu finished")
        output_function("Inventory saved. Goodbye.")
