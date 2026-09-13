"""Product and stock operations for the inventory manager."""

import logging

from .exceptions import InventoryError
from .validators import (
    require_non_negative_integer,
    require_non_negative_number,
    require_text,
)

logger = logging.getLogger(__name__)


def create_product(
    product_id: object,
    name: object,
    category: object,
    quantity: object,
    price: object,
    low_stock_limit: object = 5,
) -> dict[str, object]:
    """Validate values and return a product dictionary."""
    logger.debug(f"Creating product: id={product_id!r}, name={name!r}")
    return {
        "product_id": require_text(product_id, "product ID"),
        "name": require_text(name, "name"),
        "category": require_text(category, "category"),
        "quantity": require_non_negative_integer(quantity, "quantity"),
        "price": require_non_negative_number(price, "price"),
        "low_stock_limit": require_non_negative_integer(
            low_stock_limit, "low-stock limit"
        ),
    }


def add_product(
    products: list[dict[str, object]], product: dict[str, object]
) -> None:
    """Add a product when its ID is unique."""
    product_id = str(product["product_id"])
    duplicate = any(
        str(existing["product_id"]).lower() == product_id.lower()
        for existing in products
    )
    if duplicate:
        logger.warning(f"Duplicate product ID: {product_id!r}")
        raise InventoryError(f"product ID already exists: {product_id}")
    products.append(product)
    logger.info(f"Product added: {product_id!r}")


def find_product(
    products: list[dict[str, object]], product_id: object
) -> dict[str, object]:
    """Return a product using a case-insensitive ID lookup."""
    wanted_id = require_text(product_id, "product ID").lower()
    for product in products:
        if str(product["product_id"]).lower() == wanted_id:
            return product
    logger.warning(f"Product not found: {product_id!r}")
    raise InventoryError(f"product not found: {product_id}")


def search_products(
    products: list[dict[str, object]], search_text: object
) -> list[dict[str, object]]:
    """Search product ID, name, and category."""
    query = require_text(search_text, "search text").lower()
    matches = [
        product
        for product in products
        if query in str(product["product_id"]).lower()
        or query in str(product["name"]).lower()
        or query in str(product["category"]).lower()
    ]
    logger.info(f"Search completed: query={query!r}, matches={len(matches)}")
    return matches


def update_stock(
    products: list[dict[str, object]], product_id: object, change: object
) -> int:
    """Apply a signed stock change and return the new quantity."""
    if isinstance(change, bool):
        logger.warning(f"Invalid stock change: {change!r}")
        raise InventoryError("stock change must be a whole number")
    try:
        stock_change = int(change)
    except (TypeError, ValueError, OverflowError) as error:
        logger.warning(f"Invalid stock change: {change!r}")
        raise InventoryError("stock change must be a whole number") from error
    if isinstance(change, float) and not change.is_integer():
        logger.warning(f"Fractional stock change: {change!r}")
        raise InventoryError("stock change must be a whole number")

    product = find_product(products, product_id)
    new_quantity = int(product["quantity"]) + stock_change
    if new_quantity < 0:
        logger.warning(
            f"Insufficient stock: id={product_id!r}, requested={-stock_change}"
        )
        raise InventoryError("not enough stock for this sale")
    product["quantity"] = new_quantity
    logger.info(f"Stock updated: id={product_id!r}, quantity={new_quantity}")
    return new_quantity


def remove_product(
    products: list[dict[str, object]], product_id: object
) -> dict[str, object]:
    """Remove and return a product."""
    product = find_product(products, product_id)
    products.remove(product)
    logger.info(f"Product removed: {product_id!r}")
    return product


def get_total_value(products: list[dict[str, object]]) -> float:
    """Return the total value of all available stock."""
    return sum(
        float(product["price"]) * int(product["quantity"])
        for product in products
    )


def get_low_stock_products(
    products: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return products at or below their low-stock limit."""
    return [
        product
        for product in products
        if int(product["quantity"]) <= int(product["low_stock_limit"])
    ]
