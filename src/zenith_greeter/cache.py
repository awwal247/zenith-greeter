"""Bounded, thread-safe, in-process TTL cache."""
from collections import OrderedDict
from functools import wraps
from math import isfinite
from threading import RLock
from time import monotonic


class TTLCache:
    """A small least-recently-used cache with per-item expiry.

    The cache is local to the current Python process. It is not a shared
    cache for multiple workers or devices.
    """

    def __init__(self, ttl=300, maxsize=256):
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be a number")
        if not isfinite(ttl) or ttl < 0:
            raise ValueError("ttl must be finite and non-negative")
        if not isinstance(maxsize, int) or isinstance(maxsize, bool):
            raise TypeError("maxsize must be an integer")
        if maxsize < 1:
            raise ValueError("maxsize must be a positive integer")
        self.ttl, self.maxsize = float(ttl), maxsize
        self._data, self._lock = OrderedDict(), RLock()

    def set(self, key, value, ttl=None):
        """Store a value and return it; an optional ttl overrides the default."""
        lifetime = self.ttl if ttl is None else ttl
        if isinstance(lifetime, bool) or not isinstance(lifetime, (int, float)):
            raise TypeError("ttl must be a number")
        if not isfinite(lifetime) or lifetime < 0:
            raise ValueError("ttl must be finite and non-negative")
        with self._lock:
            self._data.pop(key, None)
            self._data[key] = (monotonic() + float(lifetime), value)
            while len(self._data) > self.maxsize:
                self._data.popitem(last=False)
        return value

    def get(self, key, default=None):
        """Return a cached value, or *default* if missing or expired."""
        with self._lock:
            item = self._data.get(key)
            if item is None:
                return default
            expires, value = item
            if expires <= monotonic():
                del self._data[key]
                return default
            self._data.move_to_end(key)
            return value

    def delete(self, key):
        """Delete *key* and report whether it existed."""
        with self._lock:
            return self._data.pop(key, _MISSING) is not _MISSING

    def clear(self):
        """Remove all cached entries."""
        with self._lock:
            self._data.clear()

    def __len__(self):
        """Return the number of unexpired entries."""
        with self._lock:
            now = monotonic()
            expired = [key for key, (deadline, _) in self._data.items() if deadline <= now]
            for key in expired:
                del self._data[key]
            return len(self._data)


_MISSING = object()


def cached(ttl=300, maxsize=256):
    """Memoize function results in a bounded TTL cache.

    Unhashable arguments bypass caching and call the wrapped function normally.
    """
    def decorate(function):
        store = TTLCache(ttl=ttl, maxsize=maxsize)

        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                key = (args, tuple(sorted(kwargs.items())))
                hash(key)
            except TypeError:
                return function(*args, **kwargs)
            missing = object()
            result = store.get(key, missing)
            if result is missing:
                result = function(*args, **kwargs)
                store.set(key, result)
            return result

        wrapper.cache = store
        wrapper.cache_clear = store.clear
        return wrapper
    return decorate
