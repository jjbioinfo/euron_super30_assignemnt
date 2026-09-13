# Application Activity Logger

This function-based Python application provides a login, calculator, file-read,
file-write, and logout menu. A failed activity is logged without terminating
the menu.

## Structure

```text
application_activity_logger/
├── __init__.py
├── authentication.py
├── calculator.py
├── file_operations.py
├── logging_config.py
├── menu.py
├── main.py
├── logs/
│   ├── application.log
│   └── error.log
└── test_activity_logger.py
```

No classes are defined. All application behavior is implemented with functions
and plain dictionaries.

## Log routing

- Terminal: `DEBUG` and higher
- `logs/application.log`: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`
- `logs/error.log`: `ERROR` and `CRITICAL` only

Logs use f-string messages. Failed operations include full tracebacks through
`exc_info=True`.

## Run interactively

From `assignment/week4`:

```bash
python -m application_activity_logger.main
```

## Run the demonstration

```bash
python -m application_activity_logger.main --demo
```

The demonstration generates all five required logging levels safely.

## Run tests

```bash
python -m application_activity_logger.test_activity_logger
```

## Submission links

- GitHub Link: ______________________________
- YouTube Video: ____________________________
