"""Bounded, thread-safe, in-process TTL cache."""
from collections import OrderedDict
from threading import RLock
from time import monotonic
from functools import wraps

class TTLCache:
    """A small least-recently-used cache with per-item expiry."""
    def __init__(self, ttl=300, maxsize=256):
        if ttl < 0:
            raise ValueError("ttl must be non-negative")
        if not isinstance(maxsize, int) or isinstance(maxsize, bool) or maxsize < 1:
            raise ValueError("maxsize must be a positive integer")
        self.ttl, self.maxsize = float(ttl), maxsize
        self._data, self._lock = OrderedDict(), RLock()

    def set(self, key, value, ttl=None):
        lifetime = self.ttl if ttl is None else float(ttl)
        if lifetime < 0:
            raise ValueError("ttl must be non-negative")
        with self._lock:
            self._data.pop(key, None)
            self._data[key] = (monotonic() + lifetime, value)
            while len(self._data) > self.maxsize:
                self._data.popitem(last=False)
        return value

    def get(self, key, default=None):
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
        with self._lock:
            return self._data.pop(key, None) is not None

    def clear(self):
        with self._lock:
            self._data.clear()

    def __len__(self):
        with self._lock:
            now = monotonic()
            expired = [key for key, (deadline, _) in self._data.items() if deadline <= now]
            for key in expired:
                del self._data[key]
            return len(self._data)

def cached(ttl=300, maxsize=256):
    """Cache function results in process memory for a limited time."""
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
