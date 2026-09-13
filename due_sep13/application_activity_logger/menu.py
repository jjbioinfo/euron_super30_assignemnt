"""Menu loop for the application activities."""

import logging
from collections.abc import Callable

from .authentication import login_user, logout_user, require_login
from .calculator import calculate
from .file_operations import read_file, write_file

logger = logging.getLogger(__name__)

MENU_TEXT = """
1. Login
2. Calculate
3. Read a File
4. Write a File
5. Logout
"""


def display_menu(output_function: Callable[[str], object] = print) -> None:
    """Display the five activity choices."""
    output_function(MENU_TEXT)


def run_menu(
    input_function: Callable[[str], str] = input,
    output_function: Callable[[str], object] = print,
) -> int:
    """Run the menu and continue after a failed activity."""
    session: dict[str, object] = {"username": None, "logged_in": False}
    logger.debug(f"Menu started")

    while True:
        try:
            display_menu(output_function)
            choice = input_function("Choose an activity: ").strip()
            logger.debug(f"Menu choice: {choice!r}")

            if choice == "1":
                username = login_user(session, input_function("Username: "))
                output_function(f"Logged in as {username}")
            elif choice == "2":
                require_login(session, "calculate")
                first = float(input_function("First number: "))
                operation = input_function("Operation (+, -, *, /): ")
                second = float(input_function("Second number: "))
                output_function(f"Result: {calculate(first, operation, second)}")
            elif choice == "3":
                require_login(session, "read a file")
                content = read_file(input_function("File path: "))
                output_function(f"File content: {content}")
            elif choice == "4":
                require_login(session, "write a file")
                path = input_function("File path: ")
                content = input_function("Content: ")
                output_function(f"File written: {write_file(path, content)}")
            elif choice == "5":
                logout_user(session)
                logger.info(f"Application closed normally")
                output_function("Application closed")
                return 0
            else:
                logger.warning(f"Invalid menu choice: {choice!r}")
                output_function("Invalid choice. Enter a number from 1 to 5.")
        except (TypeError, ValueError, PermissionError, OSError, ArithmeticError) as error:
            logger.error(f"Activity failed; menu continuing: {error}", exc_info=True)
            output_function(f"Activity failed: {error}")
        except (EOFError, KeyboardInterrupt):
            logger.warning(f"Input ended; application closing")
            logout_user(session)
            return 0
        except Exception as error:
            logger.critical(f"Unexpected application failure: {error}", exc_info=True)
            output_function(f"Unexpected error: {error}")
