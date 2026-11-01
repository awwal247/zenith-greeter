"""Reusable decorators for common function behaviour."""
import warnings
from functools import wraps

def deprecated(reason="This function is deprecated"):
    """Emit DeprecationWarning whenever the decorated function is called."""
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            warnings.warn("{}: {}".format(function.__qualname__, reason),
                          DeprecationWarning, stacklevel=2)
            return function(*args, **kwargs)
        return wrapper
    return decorate

def count_calls(function):
    """Expose the number of calls through wrapper.call_count."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return function(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper

def memoize(function):
    """Cache results for hashable arguments; bypass cache for unhashable ones."""
    cache = {}
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            key = (args, tuple(sorted(kwargs.items())))
            hash(key)
        except TypeError:
            return function(*args, **kwargs)
        if key not in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]
    wrapper.cache_clear = cache.clear
    return wrapper
