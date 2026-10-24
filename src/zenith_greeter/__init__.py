"""Dependency-free utilities for everyday Python development.

The original :class:`Greeter` API remains available for backwards compatibility.
"""

from .dates import days_between, format_datetime, time_ago
from .environment import get_env, get_env_bool, get_env_int
from .files import ensure_directory, file_size, read_json, write_json
from .greeter import Greeter
from .numbers import clamp, in_range, is_even, is_odd, percentage
from .text import normalize_whitespace, slugify, truncate, word_count
from .validation import is_non_empty_string, is_valid_email, is_valid_url

__all__ = [
    "Greeter",
    "clamp",
    "days_between",
    "ensure_directory",
    "file_size",
    "format_datetime",
    "get_env",
    "get_env_bool",
    "get_env_int",
    "in_range",
    "is_even",
    "is_non_empty_string",
    "is_odd",
    "is_valid_email",
    "is_valid_url",
    "normalize_whitespace",
    "percentage",
    "read_json",
    "slugify",
    "time_ago",
    "truncate",
    "word_count",
    "write_json",
]

__version__ = "0.2.0"
