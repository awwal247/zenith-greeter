"""Date and time formatting helpers."""

from datetime import date, datetime
from typing import Optional, Union

DateLike = Union[date, datetime]


def format_datetime(value: DateLike, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a date or datetime using Python's strftime format codes."""
    if not isinstance(value, (date, datetime)):
        raise TypeError("value must be a date or datetime")
    if not isinstance(fmt, str):
        raise TypeError("fmt must be a string")
    return value.strftime(fmt)


def days_between(start: DateLike, end: DateLike) -> int:
    """Return whole calendar days between two dates (absolute difference)."""
    if isinstance(start, datetime) or isinstance(end, datetime):
        raise TypeError("start and end must be date objects, not datetime objects")
    if not isinstance(start, date) or not isinstance(end, date):
        raise TypeError("start and end must be date objects")
    return abs((end - start).days)


def time_ago(value: datetime, now: Optional[datetime] = None) -> str:
    """Describe a datetime relative to now, such as '5 minutes ago' or 'in 2 days'.

    Naive datetimes must be compared with other naive datetimes; timezone-aware
    datetimes must be compared with timezone-aware datetimes in compatible zones.
    """
    if not isinstance(value, datetime):
        raise TypeError("value must be a datetime")
    if now is None:
        now = datetime.now(value.tzinfo)
    elif not isinstance(now, datetime):
        raise TypeError("now must be a datetime")
    delta = now - value
    total_seconds = delta.total_seconds()
    seconds = int(abs(total_seconds))
    future = total_seconds < 0

    if seconds < 5:
        return "just now"
    units = (
        (60, "second"),
        (60, "minute"),
        (24, "hour"),
        (float("inf"), "day"),
    )
    amount = seconds
    unit = "second"
    for divisor, label in units:
        unit = label
        if amount < divisor:
            break
        amount = amount // divisor
    amount = int(amount)
    phrase = "{} {}{}".format(amount, unit, "" if amount == 1 else "s")
    return "in " + phrase if future else phrase + " ago"
