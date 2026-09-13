"""Run the fault-tolerant student-result processor."""

import logging
import sys

import fault_tolerant_student_result as student_results

logger = logging.getLogger(__name__)


def demonstration_students() -> list[dict[str, object]]:
    """Return valid and invalid students for the demonstration."""
    return [
        {"student_id": "S001", "name": "Ada", "marks": [92, 88, 95, 90, 85]},
        {"student_id": "S002", "name": "Ben", "marks": [70, 65, 35, 80, 75]},
        {"student_id": "S003", "name": "Chen", "marks": [90, "absent", 80, 70, 60]},
        {"student_id": "S004", "name": "Divya", "marks": [105, 80, 75, 90, 88]},
        {"student_id": "S005", "marks": [60, 70, 80, 90, 50]},
        {"student_id": "S006", "name": "Eli", "marks": [60, 70, 80, 90]},
        {"student_id": "S007", "name": "Fatima", "marks": [78, 82, 75, 88, 91]},
    ]


def print_report(report: dict[str, list[dict[str, object]]]) -> None:
    """Print successful results and skipped-record messages."""
    print("\nSTUDENT RESULTS")
    for result in report["results"]:
        print(
            f"{result['student_id']} | {result['name']} | "
            f"Total: {result['total']}/500 | "
            f"Percentage: {result['percentage']:.2f}% | "
            f"Grade: {result['grade']} | Status: {result['status']}"
        )

    print(f"\nSuccessful: {len(report['results'])}")
    print(f"Failed and skipped: {len(report['errors'])}")
    for error in report["errors"]:
        print(f"Record {error['record']} skipped: {error['error']}")


def main() -> int:
    """Load students, process every record, and return an exit code."""
    student_results.configure_logging()
    logger.debug(f"Student-result processor started")

    try:
        students = (
            student_results.load_students(sys.argv[1])
            if len(sys.argv) > 1
            else demonstration_students()
        )
        report = student_results.process_students(students)
        print_report(report)

        # Demonstrate that calculation errors are handled without a crash.
        try:
            student_results.calculate_percentage(100, 0)
        except ZeroDivisionError as error:
            logger.error(f"Calculation error handled: {error}", exc_info=True)

        logger.info(f"Student-result processor finished")
        return 0
    except (TypeError, ValueError, OSError, ArithmeticError) as error:
        logger.critical(f"Student-result processor stopped: {error}", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
