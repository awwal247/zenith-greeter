# Zenith Greeter

**Zenith Greeter** is a dependency-free Python utility toolkit for everyday tasks. The package keeps its original `Greeter` API and adds helpers for text, numbers, dates and times, validation, JSON/files, and environment variables.

- **Distribution name:** `zenith-greeter`
- **Import name:** `zenith_greeter`
- **Python:** 3.9+
- **Runtime dependencies:** none

## Installation

When published to PyPI:

```bash
python -m pip install --upgrade zenith-greeter
```

For local development:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Quick start

Import only what you need:

```python
from datetime import date, datetime
from pathlib import Path

from zenith_greeter import (
    Greeter,
    clamp,
    days_between,
    get_env_bool,
    is_valid_email,
    read_json,
    slugify,
    time_ago,
    write_json,
)

print(Greeter("Awwal").greet())
# Hello, Awwal! Welcome to Python packages.

print(slugify("Zenith Greeter: Python Utilities"))
# zenith-greeter-python-utilities

print(clamp(120, 0, 100))
# 100

print(days_between(date(2026, 1, 1), date(2026, 1, 8)))
# 7

print(time_ago(datetime(2026, 1, 1, 11, 55), now=datetime(2026, 1, 1, 12, 0)))
# 5 minutes ago

print(is_valid_email("developer@example.com"))
# True

settings = read_json("settings.json")
debug = get_env_bool("APP_DEBUG", default=False)
write_json(Path("output") / "result.json", {"debug": debug})
```

## Modules and functions

### Greetings

- `Greeter(name="there", greeting="Hello", welcome_message="Welcome to Python packages.")`
- `Greeter.greet()`

The original `from zenith_greeter import Greeter` import and greeting output are retained.

### Text — `zenith_greeter.text`

- `normalize_whitespace(value)`: collapse repeated whitespace.
- `word_count(value)`: count whitespace-separated words.
- `slugify(value, separator="-")`: create a lowercase ASCII slug.
- `truncate(value, max_length, suffix="…")`: limit text length including the suffix.

### Numbers — `zenith_greeter.numbers`

- `clamp(value, minimum, maximum)`
- `percentage(part, whole, decimals=2)`
- `in_range(value, minimum, maximum)`: inclusive bounds.
- `is_even(value)` and `is_odd(value)`

Boolean values are rejected by numeric helpers that expect numbers or integers. Invalid bounds and zero percentage denominators raise clear errors.

### Dates and times — `zenith_greeter.dates`

- `format_datetime(value, fmt="%Y-%m-%d %H:%M:%S")`
- `days_between(start, end)`: absolute calendar-day difference between `date` objects.
- `time_ago(value, now=None)`: human-readable relative time.

For predictable output in tests and applications, pass `now` to `time_ago`. When using timezone-aware datetimes, pass a compatible timezone-aware `now`.

### Validation — `zenith_greeter.validation`

- `is_non_empty_string(value)`
- `is_valid_email(value)`: pragmatic format check, not proof that an address exists.
- `is_valid_url(value)`: accepts absolute HTTP(S) URLs with a hostname.

These helpers are intentionally lightweight; use application-specific rules where stronger validation is required.

### Files and JSON — `zenith_greeter.files`

- `ensure_directory(path)`: create a directory and parent directories.
- `read_json(path, encoding="utf-8")`
- `write_json(path, data, indent=2, encoding="utf-8", create_parents=True)`
- `file_size(path)`: return bytes.

**Caution:** `write_json` overwrites an existing target file. `read_json` and file helpers propagate filesystem and JSON parsing errors so callers can handle them explicitly. Do not load untrusted JSON into sensitive workflows without application-level checks.

### Environment variables — `zenith_greeter.environment`

- `get_env(name, default=None)`
- `get_env_bool(name, default=False)`: recognizes `1/0`, `true/false`, `yes/no`, and `on/off`.
- `get_env_int(name, default=None)`

Invalid boolean or integer values raise `ValueError`. The package reads the process environment only; it does not automatically read `.env` files.

## Error handling

Functions validate common invalid inputs and raise `TypeError` or `ValueError` where appropriate. File operations may raise standard exceptions such as `FileNotFoundError`, `PermissionError`, or `json.JSONDecodeError`; catch these at the application boundary when needed.

## Development and tests

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m build
python -m twine check dist/*
```

The test suite uses Python's built-in `unittest`. No runtime third-party dependencies are required.

## Versioning

This toolkit upgrade is version **0.2.0**. Existing greeting users can continue importing `Greeter` from `zenith_greeter`; new modules are additive.
