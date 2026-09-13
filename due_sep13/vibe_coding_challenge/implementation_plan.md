# Simple Inventory Manager — Requirement Analysis

## Required features

- Add, list, search, restock, sell, and remove products.
- Show total inventory value and low-stock products.
- Save products in `inventory.json` and load them on restart.
- Continue the menu after a recoverable error.

## Product input and output

Each product stores an ID, name, category, quantity, unit price, and low-stock
limit. Menu operations display confirmations, product rows, summaries, or clear
error messages.

## Required Python concepts

- An `inventory_app` package containing separate modules.
- Functions and imports between modules.
- One custom `InventoryError` exception.
- Meaningful `try`, `except`, and `finally` blocks.
- DEBUG-and-higher logging to `logs/inventory.log`.

## Errors and boundaries

Handle missing or empty values, wrong data types, negative or non-finite
numbers, fractional quantities, duplicate IDs, missing products, insufficient
stock, missing or damaged JSON, and file-operation failures.

## Final checklist

- [ ] At least four Python modules and one package
- [ ] Working menu and JSON persistence
- [ ] Custom exception and exception handling
- [ ] File logging from DEBUG level
- [ ] Tests and README with staged AI prompts
