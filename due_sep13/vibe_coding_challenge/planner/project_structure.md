# Project Structure

```text
vibe_coding_challenge/
├── inventory_app/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── validators.py
│   ├── inventory.py
│   ├── storage.py
│   ├── logging_config.py
│   └── cli.py
├── logs/inventory.log
├── inventory.json
├── main.py
├── test_inventory.py
├── PROMPTS.md
└── README.md
```

- `exceptions.py` defines the required custom exception.
- `validators.py` validates user and stored values.
- `inventory.py` contains product and stock operations.
- `storage.py` imports inventory validation and handles JSON persistence.
- `logging_config.py` configures terminal and file logging.
- `cli.py` imports inventory and storage functions for the menu.
- `__init__.py` exposes the package's public functions.
- `main.py` imports logging and CLI functions and starts the program.
- `test_inventory.py` verifies normal, boundary, and failure cases.
