# Calculator Tools Python Package

`calculator_tools` is a reusable Python package containing separate modules for
arithmetic, statistics, conversions, and custom exceptions. It uses only the
Python standard library.

## Structure

```text
calculator_tools/
├── __init__.py
├── _validation.py
├── arithmetic.py
├── converter.py
├── exceptions.py
├── main.py
├── statistics.py
└── test_calculator_tools.py
```

- A **function** is a reusable block of code, such as `add()`.
- A **module** is one Python file, such as `arithmetic.py`.
- A **package** is a directory of related modules, identified here by
  `__init__.py`.
- An **import** makes code from another module or package available for reuse.

## Run the demonstration

From the `assignment/week4` directory:

```bash
python -m calculator_tools.main
```

The demonstration shows successful arithmetic, percentage, average,
temperature, and length calculations. It also intentionally triggers and
handles division-by-zero, bad-type, bad-value, and unsupported-operation errors.
Detailed `DEBUG` records are displayed in the terminal and saved to
`calculator_tools/calculator_tools.log`. The file rotates at 1 MB and retains
up to three backups. Validation warnings and operation failures are concise;
handled failures include one complete traceback at the application boundary in both
destinations to support debugging and analysis. Each operation logs its input
at `DEBUG` level before validation and logs either its result or failure.

## Run the tests

From the `assignment/week4` directory:

```bash
python -m calculator_tools.test_calculator_tools
```

## Public API examples

```python
import calculator_tools as calculator

calculator.add(2, 3)                         # 5
calculator.percentage(25, 200)               # 12.5
calculator.calculate_percentage(200, 25)     # 50.0
calculator.average([10, 20, 30])             # 20.0
calculator.convert_temperature(0, "C", "F") # 32.0
calculator.convert_unit(1, "mile", "km")    # 1.609344
```

## Submission links

- GitHub Link: ______________________________
- YouTube Video: ____________________________
