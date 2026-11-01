# Zenith Greeter

A lightweight, dependency-free Python utility toolkit for everyday development. The original `Greeter` class remains supported; the package now also includes practical helpers for JSON, collections, nested dictionaries, identifiers, retries and timing.

- Distribution: `zenith-greeter`
- Import package: `zenith_greeter`
- Python: 3.9+
- Runtime dependencies: none

## Install

```bash
python -m pip install --upgrade zenith-greeter
```

## Quick start

```python
from zenith_greeter import Greeter, clamp, slugify
from zenith_greeter import dictionaries, json_tools, lists

print(Greeter("Awwal").greet())
print(slugify("Zenith Greeter Toolkit"))
print(clamp(120, 0, 100))

settings = {"account": {"profile": {"name": "Awwal"}}}
print(dictionaries.deep_get(settings, "account.profile.name"))
print(lists.chunk([1, 2, 3, 4, 5], 2))
print(json_tools.pretty({"active": True, "name": "Zenith"}))
```

## Modules

| Module | Purpose |
|---|---|
| `greeter` | Original configurable greeting class |
| `text` | Slugs, whitespace, truncation, query strings and hashes |
| `validation` | Lightweight email, URL and string checks |
| `numbers` | Clamp, ranges, parity, averages, median and percentages |
| `dates` | Date differences, formatting and relative time |
| `files` | Directory creation and JSON/file helpers |
| `environment` | Typed environment-variable access and logger setup |
| `json_tools` | JSON encode/decode, pretty-print, minify and JSON Lines |
| `lists` | Chunking, deduplication, flattening and partitioning |
| `dictionaries` | Nested lookup/update, merge and flatten |
| `identifiers` | UUIDs and secure short IDs/tokens |
| `retry` | Configurable retry decorator with backoff and jitter |
| `timer` | Context-manager and direct function timing |
| `decorators` | Deprecation warnings, call counts and memoization |
| `cache` | Bounded, process-local TTL cache |
| `logger` | Console and optional file logger setup |
| `pagination` | In-memory pagination for finite iterables |

## Examples

### Chunk a list

```python
from zenith_greeter.lists import chunk
print(chunk([1, 2, 3, 4, 5], 2))
# [[1, 2], [3, 4], [5]]
```

### Read nested configuration

```python
from zenith_greeter.dictionaries import deep_get
config = {"database": {"connection": {"port": 5432}}}
print(deep_get(config, "database.connection.port", default=3306))
```

### Retry a temporary operation

```python
from zenith_greeter.retry import retry

@retry(max_attempts=3, delay=0.5, backoff=2, jitter=True)
def fetch_status():
    return call_service()
```

Retries include the first attempt. Only retry operations that are safe to repeat, or protect side effects with an idempotency strategy.

### Measure execution time

```python
from zenith_greeter.timer import measure

with measure("report") as timer:
    generate_report()

print(timer.elapsed)
```

### Paginate a finite collection

```python
from zenith_greeter.pagination import paginate
page = paginate(records, page=2, per_page=20)
print(page.items, page.total_pages, page.has_next)
```

This helper materializes its iterable in memory. Use database-level pagination for large querysets or datasets.

## Behaviour and limitations

- The package uses only the Python standard library.
- Validators are convenience checks, not authoritative domain validation.
- Retry only idempotent or safely repeatable operations; retries may repeat side effects.
- The TTL cache is process-local and is not shared across multiple workers.
- Pagination is intended for finite in-memory collections.
- File-writing functions may overwrite an existing target file.
- Use `identifiers.random_token` for security-sensitive tokens; ordinary pseudo-random strings are not security tokens.
- MD5 is for compatibility/checksum use only, never password storage.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m build
python -m twine check dist/*
```

New helpers are additive. Existing `Greeter` and earlier top-level imports remain available.
