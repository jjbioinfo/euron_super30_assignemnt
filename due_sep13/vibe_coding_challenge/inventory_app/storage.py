"""JSON persistence for inventory products."""

import json
import logging
from pathlib import Path

from .exceptions import InventoryError
from .inventory import add_product, create_product

logger = logging.getLogger(__name__)


def load_inventory(file_path: str | Path) -> list[dict[str, object]]:
    """Load and validate products from a JSON file."""
    path = Path(file_path)
    logger.debug(f"Loading inventory: {path}")
    try:
        if not path.exists():
            logger.info(f"Inventory file is missing; starting empty: {path}")
            return []

        saved_products = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(saved_products, list):
            logger.warning(f"Inventory JSON does not contain a list: {path}")
            raise InventoryError("inventory file must contain a list")

        products: list[dict[str, object]] = []
        for saved_product in saved_products:
            product = create_product(
                saved_product["product_id"],
                saved_product["name"],
                saved_product["category"],
                saved_product["quantity"],
                saved_product["price"],
                saved_product.get("low_stock_limit", 5),
            )
            add_product(products, product)

        logger.info(f"Inventory loaded: path={path}, products={len(products)}")
        return products
    except InventoryError:
        logger.error(f"Stored inventory is invalid: {path}", exc_info=True)
        raise
    except (json.JSONDecodeError, KeyError, TypeError, OSError) as error:
        logger.error(f"Inventory could not be loaded: {path}", exc_info=True)
        raise InventoryError(f"could not load inventory: {error}") from error
    finally:
        logger.debug(f"Inventory load attempt finished: {path}")


def save_inventory(
    file_path: str | Path, products: list[dict[str, object]]
) -> Path:
    """Save products as readable JSON and return the file path."""
    path = Path(file_path)
    logger.debug(f"Saving inventory: path={path}, products={len(products)}")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(products, indent=2), encoding="utf-8")
        logger.info(f"Inventory saved: path={path}, products={len(products)}")
        return path
    except (TypeError, OSError) as error:
        logger.error(f"Inventory could not be saved: {path}", exc_info=True)
        raise InventoryError(f"could not save inventory: {error}") from error
    finally:
        logger.debug(f"Inventory save attempt finished: {path}")
