"""Convenient JSON encoding, decoding, formatting and validation."""
import json

def loads(value, **kwargs):
    """Decode JSON text."""
    return json.loads(value, **kwargs)

def dumps(value, *, indent=None, sort_keys=False, ensure_ascii=False, **kwargs):
    """Encode a Python object as JSON."""
    return json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii, **kwargs)

def pretty(value, indent=2, sort_keys=False):
    """Pretty-print JSON text or a Python object."""
    data = loads(value) if isinstance(value, (str, bytes, bytearray)) else value
    return dumps(data, indent=indent, sort_keys=sort_keys)

def minify(value):
    """Return compact JSON from JSON text or a Python object."""
    data = loads(value) if isinstance(value, (str, bytes, bytearray)) else value
    return dumps(data, separators=(",", ":"))

def is_json(value):
    """Return whether value contains valid JSON."""
    try:
        loads(value)
        return True
    except (TypeError, ValueError, UnicodeDecodeError):
        return False

def json_lines(values):
    """Encode each iterable item as one newline-delimited JSON value."""
    return "\n".join(dumps(item) for item in values)
