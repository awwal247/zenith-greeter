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
    minimum = _real_number("minimum", value)
    maximum = _real_number("maximum", value)
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
    minimum = _real_number("minimum", value)
    maximum = _real_number("maximum", value)
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


def avg(*values: Real) -> float:
    """Return the arithmetic mean of the provided numeric values.

    Args:
        *values: Numeric arguments. Must provide at least one value.

    Returns:
        The average as a float.

    Raises:
        ValueError: If no values are provided.

    Example:
        >>> avg(1, 2, 3)
        2.0
    """
    if not values:
        raise ValueError("at least one value must be provided")
    total = 0.0
    for v in values:
        total += _real_number("value", v)
    return total / len(values)


def median(*values: Real) -> float:
    """Return the median of the provided numeric values.

    Args:
        *values: Numeric arguments. Must provide at least one value.

    Returns:
        The median as a float.

    Raises:
        ValueError: If no values are provided.

    Example:
        >>> median(1, 5, 2, 8, 3)
        3.0
    """
    if not values:
        raise ValueError("at least one value must be provided")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_vals[mid])
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def round_to(value: Real, ndigits: int = 0) -> float:
    """Round a real number to the nearest step of 10**‑ndigits.

    Args:
        value: The numeric value to round.
        ndigits: Non‑negative integer specifying decimal places to round to.

    Returns:
        Rounded float.

    Raises:
        TypeError: If ndigits is not an integer.
        ValueError: If ndigits is negative.

    Example:
        >>> round_to(3.14159, ndigits=2)
        3.14
    """
    value = _real_number("value", value)
    if not isinstance(ndigits, int) or isinstance(ndigits, bool):
        raise TypeError("ndigits must be an integer")
    if ndigits < 0:
        raise ValueError("ndigits cannot be negative")
    return round(value, ndigits)