"""Dependency-free utilities for everyday Python development.

The original :class:`Greeter` API remains available for backwards compatibility.
"""

from .dates import days_between, format_datetime, time_ago
from .environment import get_env, get_env_bool, get_env_int, setup_logger
from .files import ensure_directory, file_size, read_json, write_json
from .greeter import Greeter
from .numbers import clamp, in_range, is_even, is_odd, percentage
from .text import (
    build_query_string,
    md5,
    parse_query_string,
    random_password,
    random_string,
    sha256,
    normalize_whitespace,
    slugify,
    truncate,
    word_count,
)
from .utils import is_bool, is_datetime, is_float, is_int, memoize

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
    "is_bool",
    "is_even",
    "is_float",
    "is_int",
    "is_non_empty_string",
    "is_odd",
    "is_valid_email",
    "is_valid_url",
    "md5",
    "normalize_whitespace",
    "percentage",
    "parse_query_string",
    "read_json",
    "random_password",
    "random_string",
    "setup_logger",
    "slugify",
    "time_ago",
    "truncate",
    "word_count",
    "write_json",
]

__version__ = "0.3.0"