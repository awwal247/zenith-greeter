"""Small file and JSON helpers using the Python standard library."""

import json
from pathlib import Path
from typing import Any, Union

PathLike = Union[str, Path]


def ensure_directory(path: PathLike) -> Path:
    """Create a directory and its parents if needed; return the Path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def read_json(path: PathLike, encoding: str = "utf-8") -> Any:
    """Read and decode a JSON file. File and JSON errors are propagated."""
    with Path(path).open("r", encoding=encoding) as file:
        return json.load(file)


def write_json(
    path: PathLike,
    data: Any,
    indent: int = 2,
    encoding: str = "utf-8",
    create_parents: bool = True,
) -> Path:
    """Write JSON to a file and return its path.

    Parent directories are created by default. Existing files are overwritten.
    """
    target = Path(path)
    if create_parents:
        target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)
        file.write("\n")
    return target


def file_size(path: PathLike) -> int:
    """Return a file's size in bytes."""
    return Path(path).stat().st_size
