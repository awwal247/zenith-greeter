"""Numeric helpers with explicit input checks."""

import math
from numbers import Real


def _real_number(name: str, value: object) -> Real:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("{} must be a real number".format(name))
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("{} must be finite".format(name))
    return value


def clamp(value: Real, minimum: Real, maximum: Real) -> Real:
    """Return value bounded by minimum and maximum, inclusive."""
    value = _real_number("value", value)
    minimum = _real_number("minimum", minimum)
    maximum = _real_number("maximum", maximum)
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return max(minimum, min(value, maximum))


def percentage(part: Real, whole: Real, decimals: int = 2) -> float:
    """Return part as a percentage of whole; whole cannot be zero."""
    part = _real_number("part", part)
    whole = _real_number("whole", whole)
    if whole == 0:
        raise ValueError("whole cannot be zero")
    if not isinstance(decimals, int) or isinstance(decimals, bool):
        raise TypeError("decimals must be an integer")
    if decimals < 0:
        raise ValueError("decimals cannot be negative")
    return round((part / whole) * 100, decimals)


def in_range(value: Real, minimum: Real, maximum: Real) -> bool:
    """Return whether value lies between the inclusive bounds."""
    value = _real_number("value", value)
    minimum = _real_number("minimum", minimum)
    maximum = _real_number("maximum", maximum)
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return minimum <= value <= maximum


def is_even(value: int) -> bool:
    """Return whether value is an even integer (booleans are rejected)."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return value % 2 == 0


def is_odd(value: int) -> bool:
    """Return whether value is an odd integer (booleans are rejected)."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return value % 2 != 0
