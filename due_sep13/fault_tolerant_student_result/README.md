# Fault-Tolerant Student Result Processor

This function-based Python package reads student records containing marks for
five subjects and calculates total, percentage, grade, and pass/fail status.
Invalid records are logged and skipped without stopping the batch.

## Structure

```text
fault_tolerant_student_result/
├── __init__.py
├── exceptions.py
├── logging_config.py
├── student_operations.py
├── result_calculation.py
├── main.py
└── test_student_results.py
```

The only class defined by this project is the assignment-required
`InvalidMarksError` custom exception. Application logic uses functions and
plain dictionaries.

## Rules and assumptions

- Exactly five marks are required.
- Every mark must be numeric, finite, and between 0 and 100.
- A student passes only when every subject mark is at least 40.
- Grades: A+ (90+), A (80+), B (70+), C (60+), D (50+), E (40+), F (<40).
- Missing name, student ID, or marks makes that record invalid.
- Invalid records do not prevent later students from being processed.

## Logging

Logging starts at `DEBUG` and records processing steps, successful results,
validation warnings, and skipped records. A complete traceback is recorded once
where each failure is handled. Records appear in the terminal and in the rotating
`student_results.log` file.

## Run the demonstration

From `assignment/week4`:

```bash
python -m fault_tolerant_student_result.main
```

## Process a JSON file

```bash
python -m fault_tolerant_student_result.main /path/to/students.json
```

Input example:

```json
[
  {
    "student_id": "S001",
    "name": "Ada",
    "marks": [92, 88, 95, 90, 85]
  }
]
```

## Run tests

```bash
python -m fault_tolerant_student_result.test_student_results
```

## Submission links

- GitHub Link: ______________________________
- YouTube Video: ____________________________
