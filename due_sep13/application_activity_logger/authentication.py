"""Login and logout functions."""

import logging

logger = logging.getLogger(__name__)


def login_user(session: dict[str, object], username: object) -> str:
    """Log in a user and return the username."""
    logger.debug(f"Login requested: username={username!r}")
    if not isinstance(username, str) or not username.strip():
        logger.warning(f"Login rejected because the username is empty")
        raise ValueError("username must be a non-empty string")
    if session.get("logged_in"):
        logger.warning(f"Login requested while another user is logged in")
        raise PermissionError("a user is already logged in")

    normalized_username = username.strip()
    session["username"] = normalized_username
    session["logged_in"] = True
    logger.info(f"User logged in: {normalized_username!r}")
    return normalized_username


def require_login(session: dict[str, object], activity: str) -> None:
    """Raise an error when a protected activity is used before login."""
    if not session.get("logged_in"):
        logger.warning(f"Login required for activity: {activity}")
        raise PermissionError("please log in before performing this activity")


def logout_user(session: dict[str, object]) -> str | None:
    """Log out the current user and return the previous username."""
    if not session.get("logged_in"):
        logger.warning(f"Logout requested without an active user")
        return None

    username = session.get("username")
    session["username"] = None
    session["logged_in"] = False
    logger.info(f"User logged out: {username!r}")
    return str(username)
