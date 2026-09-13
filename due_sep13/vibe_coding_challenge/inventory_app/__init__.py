"""Public interface for the Simple Inventory Manager package."""

from .exceptions import InventoryError
from .inventory import (
    add_product,
    create_product,
    find_product,
    get_low_stock_products,
    get_total_value,
    remove_product,
    search_products,
    update_stock,
)
from .logging_config import configure_logging
from .storage import load_inventory, save_inventory

__all__ = [
    "InventoryError",
    "add_product",
    "configure_logging",
    "create_product",
    "find_product",
    "get_low_stock_products",
    "get_total_value",
    "load_inventory",
    "remove_product",
    "save_inventory",
    "search_products",
    "update_stock",
]
