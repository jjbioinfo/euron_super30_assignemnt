"""Start the Simple Inventory Manager."""

import logging
from pathlib import Path

from inventory_app.cli import run_cli
from inventory_app.exceptions import InventoryError
from inventory_app.logging_config import configure_logging

DATA_FILE = Path(__file__).with_name("inventory.json")


def main() -> int:
    """Configure logging and start the menu."""
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Simple Inventory Manager started")
    try:
        return run_cli(DATA_FILE)
    except InventoryError as error:
        logger.critical(f"Application could not continue: {error}")
        print(f"Application error: {error}")
        return 1
    except Exception as error:
        logger.critical(f"Unexpected application failure: {error}", exc_info=True)
        print(f"Unexpected error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
