"""Retry decorators for operations that may fail temporarily."""
import random
import time
from functools import wraps
from typing import Callable, Optional, Tuple, Type


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    on_retry: Optional[Callable[[BaseException, int], None]] = None,
    jitter: bool = False,
):
    """Retry selected exceptions; attempts include the initial function call.

    Args:
        max_attempts: Total attempts, including the first call.
        delay: Initial wait in seconds between attempts.
        backoff: Multiplier applied to the wait after each retry.
        exceptions: Exception classes that should trigger a retry.
        on_retry: Optional callback called with (exception, failed_attempt).
        jitter: If true, randomize each wait between zero and the current delay.

    Only use this decorator for operations safe to repeat, or protect side
    effects with an idempotency strategy.
    """
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    for name, value in (("delay", delay), ("backoff", backoff)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("{} must be a number".format(name))
        if value < 0 or value == float("inf") or value != value:
            raise ValueError("{} must be finite and non-negative".format(name))
    if not isinstance(jitter, bool):
        raise TypeError("jitter must be a boolean")
    if not isinstance(exceptions, tuple) or not all(
        isinstance(exc, type) and issubclass(exc, BaseException) for exc in exceptions
    ):
        raise TypeError("exceptions must be a tuple of exception classes")
    if on_retry is not None and not callable(on_retry):
        raise TypeError("on_retry must be callable or None")

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
                    wait *= float(backoff)
            raise RuntimeError("retry loop exited unexpectedly")
        return wrapper
    return decorate
