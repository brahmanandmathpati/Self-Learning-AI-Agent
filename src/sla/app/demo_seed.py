"""Seed the hosted dashboard with the committed results snapshot (data/demo/sla_demo.db).

The hosted app (Streamlit Community Cloud) starts with no database, and its disk is wiped on every reboot.
When running there, and only if no database exists yet, the read-only snapshot of real local runs is copied to
the database path, so Evaluation, Agent comparison and Ablation show real results. Runs started on the hosted
app are added on top. Locally (and in tests) nothing happens unless SLA_SEED_DEMO=1 is set.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from sla import settings

SNAPSHOT_DIR = settings.PROJECT_ROOT / "data" / "demo"
SNAPSHOT_DB = SNAPSHOT_DIR / "sla_demo.db"
SNAPSHOT_META = SNAPSHOT_DIR / "snapshot.json"


def _hosted() -> bool:
    """True on Streamlit Community Cloud (the repository is mounted under /mount/src) or when forced."""
    return os.environ.get("SLA_SEED_DEMO") == "1" or str(Path(__file__).resolve()).startswith("/mount/src/")


def seed_if_needed() -> bool:
    """Copy the snapshot to the database path when hosted and no database exists. Returns True if seeded."""
    if os.environ.get("SLA_SEED_DEMO") == "0" or not _hosted() or not SNAPSHOT_DB.is_file():
        return False
    target = Path(settings.db_path())
    if target.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SNAPSHOT_DB, target)
    return True


def snapshot_info() -> dict[str, Any] | None:
    """Metadata of the committed snapshot, shown in the sidebar when the hosted app uses it."""
    if not (_hosted() and SNAPSHOT_META.is_file()):
        return None
    try:
        return json.loads(SNAPSHOT_META.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
