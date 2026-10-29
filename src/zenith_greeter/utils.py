"""Utility decorators and lightweight type checks."""

from functools import wraps


def memoize(func):
    """Cache the results of a function call based on its arguments.

    Only hashable arguments are supported. Unhashable arguments (e.g. lists)
    fall back to calling the function directly without caching.

    Example:
        @memoize
        def expensive(n):
            return n * n
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            key = (args, tuple(sorted(kwargs.items())))
        except TypeError:
            # Unhashable arguments cannot be cached
            return func(*args, **kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def is_int(value: object) -> bool:
    """Return True if value is a non-boolean integer."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_bool(value: object) -> bool:
    """Return True if value is a boolean."""
    return isinstance(value, bool)


def is_float(value: object) -> bool:
    """Return True if value is a float."""
    return isinstance(value, float)


def is_datetime(value: object) -> bool:
    """Return True if value is a datetime.datetime instance."""
    from datetime import datetime

    return isinstance(value, datetime)