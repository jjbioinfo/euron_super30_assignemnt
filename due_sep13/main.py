"""Start the interactive application or its safe demonstration."""

import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import application_activity_logger as activity_logger

logger = logging.getLogger(__name__)


def run_demo() -> None:
    """Demonstrate every activity and all five logging levels."""
    logger.debug(f"Activity logger demonstration started")
    session: dict[str, object] = {"username": None, "logged_in": False}

    activity_logger.login_user(session, "demo_user")
    activity_logger.calculate(12, "/", 4)

    with TemporaryDirectory(prefix="activity_logger_demo_") as directory:
        folder = Path(directory)
        empty_file = folder / "empty.txt"
        empty_file.touch()
        activity_logger.read_file(empty_file)
        activity_logger.write_file(folder / "notes.txt", "Logged file activity")

        try:
            activity_logger.read_file(folder / "missing.txt")
        except FileNotFoundError as error:
            logger.error(f"File could not be opened: {error}", exc_info=True)

    try:
        raise RuntimeError("controlled demonstration failure")
    except RuntimeError as error:
        logger.critical(f"Unexpected application failure: {error}", exc_info=True)

    activity_logger.logout_user(session)
    logger.info(f"Activity logger demonstration completed")


def main() -> int:
    """Configure logging and run interactive or demonstration mode."""
    activity_logger.configure_logging()
    logger.debug(f"Application started")

    try:
        if "--demo" in sys.argv[1:]:
            run_demo()
            return 0
        return activity_logger.run_menu()
    except Exception as error:
        logger.critical(f"Application stopped unexpectedly: {error}", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
