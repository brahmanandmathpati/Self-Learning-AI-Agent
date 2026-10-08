"""Project-wide paths. Override with environment variables (see .env.example)."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _path(var: str, default: Path) -> Path:
    value = os.environ.get(var)
    return Path(value) if value else default


def db_path() -> Path:
    """SQLite database file (env SLA_DB, default runs/sla.db in the project)."""
    return _path("SLA_DB", PROJECT_ROOT / "runs" / "sla.db")


def config_dir() -> Path:
    """Folder with the YAML experiment configs (env SLA_CONFIG_DIR)."""
    return _path("SLA_CONFIG_DIR", PROJECT_ROOT / "configs")


def run_root() -> Path:
    """Folder where run directories are created (env SLA_RUN_ROOT)."""
    return _path("SLA_RUN_ROOT", PROJECT_ROOT / "runs")
