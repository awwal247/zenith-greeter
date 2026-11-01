"""Small, predictable text-processing helpers.

The random string helpers are intended for ordinary identifiers and examples.
Use :func:`zenith_greeter.identifiers.random_token` for security-sensitive tokens.
"""
import hashlib
import random
import re
import secrets
import string
import unicodedata
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlencode, urlparse


def normalize_whitespace(value: str) -> str:
    """Collapse runs of whitespace to one space and trim the ends."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return " ".join(value.split())


def word_count(value: str) -> int:
    """Count whitespace-separated words after normalizing whitespace."""
    return len(normalize_whitespace(value).split())


def slugify(value: str, separator: str = "-") -> str:
    """Convert text to a lowercase ASCII slug using *separator*."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", separator, ascii_text.lower())
    return slug.strip(separator)


def truncate(value: str, max_length: int, suffix: str = "…") -> str:
    """Limit a string to *max_length* characters, including the suffix."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if not isinstance(max_length, int) or isinstance(max_length, bool):
        raise TypeError("max_length must be an integer")
    if max_length < 0:
        raise ValueError("max_length cannot be negative")
    if not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if len(value) <= max_length:
        return value
    if max_length == 0:
        return ""
    if len(suffix) >= max_length:
        return suffix[:max_length]
    return value[: max_length - len(suffix)] + suffix


def random_string(length: int = 12, alphabet: Optional[str] = None) -> str:
    """Generate a non-cryptographic random string.

    For API keys, reset links, session secrets, or other security-sensitive
    values, use :func:`zenith_greeter.identifiers.random_token` instead.
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer")
    if length < 0:
        raise ValueError("length cannot be negative")
    if alphabet is None:
        alphabet = string.ascii_letters + string.digits
    if not isinstance(alphabet, str):
        raise TypeError("alphabet must be a string")
    if length and not alphabet:
        raise ValueError("alphabet cannot be empty when length is positive")
    return "".join(random.choice(alphabet) for _ in range(length))


def random_password(length: int = 12) -> str:
    """Generate a password containing at least two special characters.

    Uses the system-backed :mod:`secrets` generator. This is a convenience
    generator, not a substitute for an application's password policy.
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer")
    if length < 4:
        raise ValueError("password length must be at least 4")
    specials = "!@#$%^&*()"
    alphabet = string.ascii_letters + string.digits + specials
    result = [secrets.choice(specials), secrets.choice(specials)]
    result.extend(secrets.choice(alphabet) for _ in range(length - 2))
    secrets.SystemRandom().shuffle(result)
    return "".join(result)


def md5(value: str) -> str:
    """Return an MD5 hex digest for compatibility/checksum use, not passwords."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return hashlib.md5(value.encode("utf-8")).hexdigest()


def sha256(value: str) -> str:
    """Return the SHA-256 hex digest of a string."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_query_string(params: Dict[str, Any], separator: str = "&") -> str:
    """URL-encode mapping values into a query string without a leading '?'."""
    if not isinstance(params, dict):
        raise TypeError("params must be a dict")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")
    return urlencode(params, doseq=True, safe="") .replace("&", separator)


def parse_query_string(url: str) -> Dict[str, list]:
    """Parse a URL or query string into a mapping of keys to value lists."""
    if not isinstance(url, str):
        raise TypeError("url must be a string")
    parsed = urlparse(url)
    query = parsed.query if parsed.scheme or parsed.netloc or parsed.path else url.lstrip("?")
    return parse_qs(query)
