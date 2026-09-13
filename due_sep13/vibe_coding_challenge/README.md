# Simple Inventory Manager

A function-based Python CLI for adding, searching, updating, selling, and
removing inventory products. Products persist in `inventory.json`, and
application activity is recorded in `logs/inventory.log`.

## Structure

`inventory_app` is the package, and its Python files are modules. The modules
import and reuse each other's focused functions. `InventoryError` is the only
class because Python requires a class for a custom exception.

## Run

```sh
cd /Users/JJOHN41/Documents/my_learning/euron_super30/assignment/week4/vibe_coding_challenge
python main.py
```

## Test

```sh
python test_inventory.py
```

## Error handling and logging

The application handles invalid input, duplicate IDs, missing products,
insufficient stock, missing or corrupted JSON, and file errors. A failed menu
operation is logged and the menu continues. `finally` saves inventory when the
menu closes. Logs start at DEBUG and are written to `logs/inventory.log`.

## AI prompts used

The full staged prompt record is in `PROMPTS.md`. Example prompts:

1. "Analyze the assignment and list its requirements without writing code."
2. "Plan the package and modules without implementing the application."
3. "Create only the custom exception module."
4. "Create only the reusable validation module."
5. "Create only the inventory operations module and reuse validation."
6. "Create only JSON loading and saving with exception handling."
7. "Create only the DEBUG-level file logging configuration."
8. "Create the CLI by importing the existing functions."
9. "Run the application and fix only genuine observed errors."
10. "Test and review the completed application against all requirements."