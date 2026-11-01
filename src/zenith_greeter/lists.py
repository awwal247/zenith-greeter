"""Small helpers for common list and iterable operations."""
from itertools import islice

def unique(items, *, keep_order=True):
    """Return unique items, preserving first occurrence by default."""
    if not keep_order:
        return list(set(items))
    result, seen = [], set()
    for item in items:
        try:
            marker = (type(item), item)
            if marker not in seen:
                seen.add(marker)
                result.append(item)
        except TypeError:
            if item not in result:
                result.append(item)
    return result

def chunk(items, size):
    """Split an iterable into lists containing at most size items."""
    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        raise ValueError("size must be a positive integer")
    iterator, result = iter(items), []
    while True:
        part = list(islice(iterator, size))
        if not part:
            return result
        result.append(part)

def batch(items, size):
    """Alias for chunk."""
    return chunk(items, size)

def flatten(items, *, depth=1):
    """Flatten nested lists and tuples up to depth levels."""
    if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
        raise ValueError("depth must be a non-negative integer")
    result = []
    for item in items:
        if depth and isinstance(item, (list, tuple)):
            result.extend(flatten(item, depth=depth - 1))
        else:
            result.append(item)
    return result

def filter_by(items, key, value=True):
    """Filter dictionaries by the value stored under key."""
    return [item for item in items if isinstance(item, dict) and item.get(key) == value]

def partition(items, predicate):
    """Split items into (matching, non-matching) lists."""
    matching, other = [], []
    for item in items:
        (matching if predicate(item) else other).append(item)
    return matching, other
