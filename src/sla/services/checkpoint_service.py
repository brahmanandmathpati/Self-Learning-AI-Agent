"""Inspect checkpoints stored on disk for a run."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from sla.utils.io_helpers import read_json


class CheckpointService:
    @staticmethod
    def list(run_dir: str | Path) -> pd.DataFrame:
        folder = Path(run_dir) / "checkpoints"
        rows = []
        if folder.is_dir():
            for ck in sorted(p for p in folder.iterdir() if (p / "checkpoint.json").is_file()):
                info = read_json(ck / "checkpoint.json")
                size = sum(f.stat().st_size for f in ck.iterdir() if f.is_file())
                rows.append({"name": ck.name, "episode": info.get("episode"), "agent": info.get("agent"),
                             "eval_mean": info.get("eval_mean"), "size_kb": round(size / 1024, 1),
                             "path": str(ck)})
        return pd.DataFrame(rows)
