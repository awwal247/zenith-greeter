"""Lightweight validation helpers.

These checks are convenience checks, not substitutes for authoritative validation
by an email provider, URL fetch policy, or application-specific rules.
"""

import re
from urllib.parse import urlsplit


_EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def is_non_empty_string(value: object) -> bool:
    """Return True when value is a string containing non-whitespace text."""
    return isinstance(value, str) and bool(value.strip())


def is_valid_email(value: object) -> bool:
    """Perform a pragmatic email-shape check; does not prove deliverability."""
    return isinstance(value, str) and bool(_EMAIL_PATTERN.fullmatch(value.strip()))


def is_valid_url(value: object) -> bool:
    """Return True for an absolute HTTP(S) URL with a hostname."""
    if not isinstance(value, str):
        return False
    try:
        parts = urlsplit(value.strip())
        return parts.scheme.lower() in {"http", "https"} and bool(parts.hostname)
    except ValueError:
        return False
