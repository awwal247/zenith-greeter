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
    """Bound value between inclusive minimum and maximum."""
    value = _real_number("value", value)
    minimum = _real_number("minimum", minimum)
    maximum = _real_number("maximum", maximum)
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return max(minimum, min(value, maximum))

def percentage(part: Real, whole: Real, decimals: int = 2) -> float:
    """Return part as a percentage of whole."""
    part, whole = _real_number("part", part), _real_number("whole", whole)
    if whole == 0:
        raise ValueError("whole cannot be zero")
    if not isinstance(decimals, int) or isinstance(decimals, bool):
        raise TypeError("decimals must be an integer")
    if decimals < 0:
        raise ValueError("decimals cannot be negative")
    return round((part / whole) * 100, decimals)

def in_range(value: Real, minimum: Real, maximum: Real) -> bool:
    """Return whether value lies between inclusive bounds."""
    value = _real_number("value", value)
    minimum = _real_number("minimum", minimum)
    maximum = _real_number("maximum", maximum)
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return minimum <= value <= maximum

def is_even(value: int) -> bool:
    """Return whether value is an even integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return value % 2 == 0

def is_odd(value: int) -> bool:
    """Return whether value is an odd integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return value % 2 != 0

def avg(*values: Real) -> float:
    """Return the arithmetic mean of one or more numeric values."""
    if not values:
        raise ValueError("at least one value must be provided")
    checked = [_real_number("value", value) for value in values]
    return float(sum(checked) / len(checked))

def median(*values: Real) -> float:
    """Return the median of one or more numeric values."""
    if not values:
        raise ValueError("at least one value must be provided")
    ordered = sorted(_real_number("value", value) for value in values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[middle])
    return float((ordered[middle - 1] + ordered[middle]) / 2)

def round_to(value: Real, ndigits: int = 0) -> float:
    """Round a real number to a given number of decimal places."""
    value = _real_number("value", value)
    if not isinstance(ndigits, int) or isinstance(ndigits, bool):
        raise TypeError("ndigits must be an integer")
    if ndigits < 0:
        raise ValueError("ndigits cannot be negative")
    return round(value, ndigits)
