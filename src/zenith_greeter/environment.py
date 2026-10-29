"""Typed access to environment variables."""

import logging
import os
from typing import Optional


_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Read an environment variable, returning default when it is unset."""
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")
    return os.environ.get(name, default)


def get_env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable using common true/false spellings."""
    if not isinstance(default, bool):
        raise TypeError("default must be a boolean")
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    raise ValueError(
        "{} must be a boolean value (true/false, yes/no, on/off, or 1/0)".format(name)
    )


def get_env_int(name: str, default: Optional[int] = None) -> Optional[int]:
    """Read an integer environment variable, raising ValueError if malformed."""
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")
    if default is not None and (not isinstance(default, int) or isinstance(default, bool)):
        raise TypeError("default must be an integer or None")
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value.strip())
    except ValueError as exc:
        raise ValueError("{} must contain an integer".format(name)) from exc


def setup_logger(name: str = "zenith_greeter", level: str = "INFO") -> logging.Logger:
    """Create and configure a simple logger for the application.

    Args:
        name: Logger name.
        level: Logging level as a string ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").

    Returns:
        A :class:`logging.Logger` instance configured with a StreamHandler.

    Example:
        >>> logger = setup_logger("myapp", "DEBUG")
        >>> logger.info("Application started")
        INFO:myapp:Application started
    """
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")
    if not isinstance(level, str):
        raise TypeError("level must be a string")

    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("invalid log level: {}".format(level))

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    # Avoid adding duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(levelname)s:%(name)s:%(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger