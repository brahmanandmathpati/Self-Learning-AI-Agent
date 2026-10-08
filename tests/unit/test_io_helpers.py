import pytest

from sla.utils.io_helpers import ensure_dir, read_json, write_json


def test_write_then_read_roundtrip(tmp_path):
    path = write_json(tmp_path / "a" / "data.json", {"x": 1, "name": "Somesh"})
    assert read_json(path) == {"x": 1, "name": "Somesh"}


def test_read_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_json(tmp_path / "missing.json")


def test_read_invalid_json_raises_value_error(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="bad.json"):
        read_json(bad)


def test_ensure_dir_creates_nested_folders(tmp_path):
    folder = ensure_dir(tmp_path / "x" / "y")
    assert folder.is_dir()


def test_ensure_dir_rejects_existing_file(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hi")
    with pytest.raises(NotADirectoryError):
        ensure_dir(f)
