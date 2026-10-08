"""Small file helpers.

These wrap reading/writing JSON so every module handles errors the same way.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    """Create a folder (and its parents) if it does not exist; return it as a Path."""
    folder = Path(path)
    if folder.exists() and not folder.is_dir():
        raise NotADirectoryError(f"{folder} exists and is not a folder")
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def write_json(path: str | Path, data: Any) -> Path:
    """Write ``data`` to ``path`` as pretty JSON. Creates parent folders."""
    file_path = Path(path)
    ensure_dir(file_path.parent)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return file_path


def read_json(path: str | Path) -> Any:
    """Read JSON from ``path``.

    Raises:
        FileNotFoundError: the file does not exist.
        ValueError: the file is not valid JSON (message includes the file name).
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {file_path}: {exc}") from exc
