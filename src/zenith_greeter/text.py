"""Small, predictable text-processing helpers."""

import re
import unicodedata


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
