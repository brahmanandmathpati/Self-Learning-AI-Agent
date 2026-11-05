"""Save the learned grid policies (greedy move + value per square) for the hosted website.

Checkpoints are not committed, so the hosted app cannot read them. This script reads the best checkpoint of
the seed-0 run of the newest completed experiment for each table-based agent on FrozenLake and CliffWalking
and writes data/demo/policies.json. Every number in the file comes from a real trained Q-table.

Run:  python scripts/export_policies.py [--db data/demo/sla_demo.db]
"""

from __future__ import annotations

import argparse
import json

from sla import settings
from sla.catalog import TABULAR_AGENTS
from sla.database.store import Database
from sla.evaluation.policies import GRID_ENVS, POLICIES_FILE, from_checkpoint


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(settings.db_path()))
    parser.add_argument("--out", default=str(POLICIES_FILE))
    args = parser.parse_args()
    db = Database(args.db)
    exps = db.list_experiments("pipeline")
    out = []
    for env in GRID_ENVS:
        for algo in TABULAR_AGENTS:
            sel = exps[(exps["env"] == env) & (exps["algorithm"] == algo) & (exps["status"] == "completed")]
            if sel.empty:
                continue
            exp_id = int(sel.iloc[0]["experiment_id"])
            runs = db.list_runs(exp_id)
            runs = runs[(runs["algorithm"] == algo) & (runs["status"] == "completed")].sort_values("seed")
            for _, r in runs.iterrows():
                try:
                    actions, values = from_checkpoint(r["run_dir"])
                except Exception as exc:  # noqa: BLE001
                    print(f"skip {r['run_id']}: {exc}")
                    continue
                out.append({"env": env, "algorithm": algo, "run_id": r["run_id"], "experiment_id": exp_id,
                            "seed": int(r["seed"]), "actions": actions, "values": [round(v, 4) for v in values]})
                print(f"{env} {algo}: run {r['run_id']}")
                break
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {len(out)} policies to {args.out}")


if __name__ == "__main__":
    main()
