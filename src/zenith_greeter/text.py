"""Small, predictable text-processing helpers."""

import re
import string
import unicodedata
from urllib.parse import parse_qs, urlparse


def normalize_whitespace(value: str) -> str:
    """Collapse runs of whitespace to one space and trim the ends."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return " ".join(value.split())


def word_count(value: str) -> int:
    """Count whitespace-separated words after normalizing whitespace."""
    return len(normalize_whitespace(value).split())


def slugify(value: str, separator: str = "-") -> str:
    """Convert text to a simple lowercase ASCII slug."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", separator, ascii_text.lower())
    return slug.strip(separator)


def truncate(value: str, max_length: int, suffix: str = "…") -> str:
    """Limit a string to max_length characters, including any suffix."""
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


def random_string(length: int = 12, alphabet: str = None) -> str:
    """Generate a random string of the specified length.

    Args:
        length: Number of characters in the result.
        alphabet: Custom character set. Uses letters+digits by default.

    Returns:
        A randomly generated string.

    Example:
        >>> random_string(8)
        'aB3dE5fG'
    """
    import random

    if alphabet is None:
        alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def random_password(length: int = 12) -> str:
    """Generate a random password meeting common requirements.

    Includes letters, digits, and at least two special characters from
    !@#$%^&*().

    Args:
        length: Total password length (must be >= 4).

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If length is less than 4.

    Example:
        >>> random_password(10)
        'K9$mP2@qL1'
    """
    if length < 4:
        raise ValueError("password length must be at least 4")

    import random

    specials = "!@#$%^&*()"
    # Reserve 2 spots for special characters
    result = [
        random.choice(specials),
        random.choice(specials),
    ]
    # Fill remainder from full alphabet
    alphabet = string.ascii_letters + string.digits + specials
    result += [
        random.choice(alphabet) for _ in range(length - 2)
    ]
    # Shuffle to randomize special positions
    random.shuffle(result)
    return "".join(result)[:length]


def md5(value: str) -> str:
    """Return the MD5 hex digest of a string.

    Args:
        value: The string to hash.

    Returns:
        A 32-character hexadecimal string.

    Example:
        >>> md5("hello")
        '5d41402abc4b2a76b9719d911017c592'
    """
    import hashlib

    return hashlib.md5(value.encode("utf-8")).hexdigest()


def sha256(value: str) -> str:
    """Return the SHA-256 hex digest of a string.

    Args:
        value: The string to hash.

    Returns:
        A 64-character hexadecimal string.

    Example:
        >>> sha256("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_query_string(params: dict, separator: str = "&") -> str:
    """Encode a dictionary as a URL query string.

    Args:
        params: Mapping of key/value pairs. Values are converted to strings.
        separator: Separator between parameters (default "&").

    Returns:
        A query string starting with "?" if params is non-empty, otherwise "".

    Example:
        >>> build_query_string({"page": 2, "q": "hello"})
        'page=2&q=hello'
    """
    if not isinstance(params, dict):
        raise TypeError("params must be a dict")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")

    if not params:
        return ""

    parts = []
    for key, value in params.items():
        parts.append(f"{key}={value}")
    return separator.join(parts)


def parse_query_string(url: str) -> dict:
    """Parse a URL query string into a dictionary.

    Args:
        url: A full URL or just the query portion (e.g. "?key=val").

    Returns:
        A dict mapping keys to lists of values (as returned by parse_qs).

    Example:
        >>> parse_query_string("?page=2&page=3&q=hello")
        {'page': ['2', '3'], 'q': ['hello']}
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")
    parsed = urlparse(url)
    return parse_qs(parsed.query)