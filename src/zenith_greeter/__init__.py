"""Dependency-free utilities for everyday Python development.

The original Greeter API and existing imports remain backwards compatible.
"""
from . import cache, decorators, dictionaries, identifiers, json_tools, lists, logger, pagination, retry, timer
from .dates import days_between, format_datetime, time_ago
from .environment import get_env, get_env_bool, get_env_int, setup_logger
from .files import ensure_directory, file_size, read_json, write_json
from .greeter import Greeter
from .numbers import avg, clamp, in_range, is_even, is_odd, median, percentage, round_to
from .text import (
    build_query_string, md5, normalize_whitespace, parse_query_string,
    random_password, random_string, sha256, slugify, truncate, word_count,
)
from .utils import is_bool, is_datetime, is_float, is_int, memoize
from .validation import is_non_empty_string, is_valid_email, is_valid_url

__all__ = [
    "Greeter", "cache", "decorators", "dictionaries", "identifiers",
    "json_tools", "lists", "logger", "pagination", "retry", "timer",
    "avg", "build_query_string", "clamp", "days_between", "ensure_directory",
    "file_size", "format_datetime", "get_env", "get_env_bool", "get_env_int",
    "in_range", "is_bool", "is_datetime", "is_even", "is_float", "is_int",
    "is_non_empty_string", "is_odd", "is_valid_email", "is_valid_url",
    "md5", "median", "memoize", "normalize_whitespace", "parse_query_string",
    "percentage", "random_password", "random_string", "read_json", "round_to",
    "setup_logger", "sha256", "slugify", "time_ago", "truncate", "word_count",
    "write_json",
]
__version__ = "0.4.0"
