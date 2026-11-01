"""Retry decorators for operations that may fail temporarily."""
import random
import time
from functools import wraps

def retry(max_attempts=3, delay=1.0, backoff=1.0, exceptions=(Exception,), on_retry=None, jitter=False):
    """Retry selected exceptions; max_attempts includes the initial call.

    Only use with operations safe to repeat, or with an idempotency strategy.
    """
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    if delay < 0 or backoff < 0:
        raise ValueError("delay and backoff must be non-negative")
    if not isinstance(exceptions, tuple) or not all(
        isinstance(exc, type) and issubclass(exc, BaseException) for exc in exceptions
    ):
        raise TypeError("exceptions must be a tuple of exception classes")
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            wait = float(delay)
            for attempt in range(1, max_attempts + 1):
                try:
                    return function(*args, **kwargs)
                except exceptions as error:
                    if attempt == max_attempts:
                        raise
                    if on_retry is not None:
                        on_retry(error, attempt)
                    pause = random.uniform(0, wait) if jitter and wait else wait
                    if pause:
                        time.sleep(pause)
                    wait *= backoff
        return wrapper
    return decorate
