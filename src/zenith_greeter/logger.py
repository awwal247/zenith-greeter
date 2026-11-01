"""Convenient setup for Python's standard logging module."""
import logging
from pathlib import Path

def create_logger(name="zenith_greeter", level="INFO", log_file=None, console=True):
    """Create a configured logger without duplicating Zenith-managed handlers."""
    if not isinstance(name, str) or not name:
        raise ValueError("name must be a non-empty string")
    numeric_level = getattr(logging, level.upper(), None) if isinstance(level, str) else None
    if not isinstance(numeric_level, int):
        raise ValueError("invalid log level: {}".format(level))
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    logger.propagate = False
    if console and not any(getattr(handler, "_zenith_console", False) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler._zenith_console = True
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
    if log_file is not None:
        target = Path(log_file)
        target.parent.mkdir(parents=True, exist_ok=True)
        resolved = str(target.resolve())
        if not any(getattr(handler, "_zenith_file", None) == resolved for handler in logger.handlers):
            handler = logging.FileHandler(target, encoding="utf-8")
            handler._zenith_file = resolved
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
            logger.addHandler(handler)
    return logger
