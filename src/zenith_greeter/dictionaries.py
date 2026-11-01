"""Helpers for nested dictionaries and mapping operations."""

def deep_get(mapping, path, default=None, separator="."):
    """Read a nested value using a dotted path; return default if absent."""
    if not isinstance(mapping, dict):
        raise TypeError("mapping must be a dictionary")
    if not isinstance(path, str) or not path:
        raise ValueError("path must be a non-empty string")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty string")
    current = mapping
    for key in path.split(separator):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current

def deep_set(mapping, path, value, separator="."):
    """Set a nested value, creating missing intermediate dictionaries."""
    if not isinstance(mapping, dict):
        raise TypeError("mapping must be a dictionary")
    if not isinstance(path, str) or not path or not isinstance(separator, str) or not separator:
        raise ValueError("path and separator must be non-empty strings")
    keys = path.split(separator)
    if any(not key for key in keys):
        raise ValueError("path must contain non-empty keys")
    current = mapping
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        if not isinstance(current[key], dict):
            raise TypeError("cannot traverse non-dictionary key: {}".format(key))
        current = current[key]
    current[keys[-1]] = value
    return mapping

def merge(*mappings):
    """Shallow-merge dictionaries from left to right."""
    result = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            raise TypeError("all values must be dictionaries")
        result.update(mapping)
    return result

def flatten(mapping, parent_key="", separator="."):
    """Flatten nested dictionaries into separator-delimited keys."""
    result = {}
    for key, value in mapping.items():
        name = "{}{}{}".format(parent_key, separator, key) if parent_key else str(key)
        if isinstance(value, dict) and value:
            result.update(flatten(value, name, separator))
        else:
            result[name] = value
    return result
