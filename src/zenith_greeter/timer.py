"""Execution timing context manager and function helper."""
from time import perf_counter

class Timer:
    """Measure elapsed wall-clock time with a context manager."""
    def __init__(self, name=None):
        self.name = name
        self.elapsed = None
        self.started_at = None

    def __enter__(self):
        self.started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = perf_counter() - self.started_at
        return False

def measure(name=None):
    """Create a timer for use in a with statement."""
    return Timer(name=name)

def time_call(function, *args, **kwargs):
    """Run function and return (result, elapsed_seconds)."""
    started = perf_counter()
    result = function(*args, **kwargs)
    return result, perf_counter() - started
