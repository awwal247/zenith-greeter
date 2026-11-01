# Zenith Greeter

A lightweight, dependency-free Python toolkit for common development tasks. It began with the `Greeter` class and now includes practical helpers for text, numbers, dates, validation, files, JSON, collections, nested dictionaries, identifiers, retries, timing, caching, logging, decorators and pagination.

- **Distribution:** `zenith-greeter`
- **Import:** `zenith_greeter`
- **Python:** 3.9+
- **Runtime dependencies:** none
- **License:** MIT

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

## Utilities at a glance

| Module | What it helps with |
|---|---|
| `greeter` | Original configurable greeting class |
| `text` | Slugs, whitespace, truncation, URL query encoding, hashes and random strings |
| `numbers` | Clamping, ranges, parity, averages, median and percentages |
| `dates` | Date differences, formatting and relative time |
| `validation` | Lightweight email, URL and non-empty string checks |
| `files` | Directory creation, file size and JSON file read/write |
| `environment` | Typed environment-variable access |
| `json_tools` | JSON encode/decode, pretty-print, minify and JSON Lines |
| `lists` | Chunking, deduplication, flattening, filtering and partitioning |
| `dictionaries` | Nested lookup/update, shallow merge and flattening |
| `identifiers` | UUIDs and cryptographically secure short IDs/tokens |
| `retry` | Retry decorator with backoff, selected exceptions and optional jitter |
| `timer` | Context-manager and direct function timing |
| `decorators` | Deprecation warnings, call counts and memoization |
| `cache` | Bounded, thread-safe, process-local TTL cache |
| `logger` | Console and optional file logger setup |
| `pagination` | In-memory pagination for finite iterables |

## Common examples

### Split data into batches

```python
from zenith_greeter.lists import chunk

for batch in chunk(range(1, 11), 3):
    print(batch)
# [1, 2, 3]
# [4, 5, 6]
# [7, 8, 9]
# [10]
```

### Read a nested setting

```python
from zenith_greeter.dictionaries import deep_get, deep_set

config = {"database": {"connection": {"port": 5432}}}
port = deep_get(config, "database.connection.port", default=3306)
deep_set(config, "database.connection.ssl", True)
```

### Encode query parameters safely

```python
from zenith_greeter.text import build_query_string, parse_query_string

query = build_query_string({"search": "python utilities", "tag": ["tools", "tips"]})
print(query)
print(parse_query_string(query))
```

### Retry a temporary operation

```python
from zenith_greeter.retry import retry

@retry(max_attempts=3, delay=0.5, backoff=2, jitter=True)
def fetch_status():
    return call_service()
```

Retries include the first attempt. Only retry operations that are safe to repeat, or protect side effects with an idempotency strategy.

### Cache a frequently used result

```python
from zenith_greeter.cache import cached

@cached(ttl=60, maxsize=128)
def load_profile(user_id):
    return fetch_profile(user_id)

profile = load_profile(42)
load_profile.cache_clear()  # clear cached results
```

The cache is local to one Python process. It is not a replacement for Redis or a shared cache in multi-worker deployments.

### Measure execution time

```python
from zenith_greeter.timer import measure

with measure("report") as timer:
    generate_report()

print(timer.elapsed)  # seconds
```

### Paginate a finite collection

```python
from zenith_greeter.pagination import paginate

page = paginate(records, page=2, per_page=20)
print(page.items, page.total_pages, page.has_next)
```

Pagination materializes the iterable in memory. Use database-level pagination for large querysets or datasets.

## Important behaviour and limitations

- The package uses only the Python standard library at runtime.
- Validators are convenience checks, not authoritative domain validation.
- `random_string` is for ordinary non-secret strings. Use `identifiers.random_token` for security-sensitive tokens.
- `random_password` uses Python's system-backed `secrets` generator.
- MD5 is provided for compatibility/checksum use only; never use it for password storage.
- Retry may repeat side effects. Use it only for safe/idempotent operations.
- The TTL cache is process-local and is not shared between workers.
- Pagination is intended for finite, reasonably sized in-memory collections.
- `write_json` overwrites an existing target file.

## Development

Clone the repository, then run:

```bash
python -m venv .venv
# Linux / macOS / Termux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e .
python -m unittest discover -s tests -v
```

Build and validate distribution files:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

The project CI runs the unit tests on supported Python versions and checks the built distribution.

## Backwards compatibility

The original `Greeter` class and established top-level imports remain supported. New utility modules are additive.

## License

MIT. See [LICENSE](LICENSE).
