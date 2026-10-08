"""Regenerate the results tables in results/ from the SQLite database (never type numbers by hand).

Run:  python scripts/make_tables.py [--db runs/sla.db] [--out results]
Writes results/comparison.md, results/experiments.md and results/ablation.md. If nothing has been
run yet, each file says NOT RUN.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from sla import settings
from sla.services import get_services


def _md(df: pd.DataFrame) -> str:
    if df.empty:
        return "NOT RUN - no experiment data available.\n"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in row) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(settings.db_path()))
    parser.add_argument("--out", default="results")
    args = parser.parse_args()
    svc = get_services(args.db)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    comp = svc.experiments.comparison_table()
    (out / "comparison.md").write_text("# Held-out test results by agent (mean over seeds)\n\n" + _md(comp))

    rows = []
    for _, e in svc.experiments.experiments("pipeline").iterrows():
        exp = svc.experiments.experiment(int(e["experiment_id"]))
        s = exp.get("summary") or {}
        c = s.get("trained_vs_random") or {}
        rows.append({"experiment": int(e["experiment_id"]), "env": e["env"], "algorithm": e["algorithm"],
                     "seeds": s.get("n_seeds"), "git_sha": e["git_sha"],
                     "trained_mean": c.get("mean_trained"), "random_mean": c.get("mean_random"),
                     "diff_ci95": f"[{c['diff_ci_low']:.2f}, {c['diff_ci_high']:.2f}]" if c else "NOT RUN",
                     "welch_p": c.get("p_value")})
    (out / "experiments.md").write_text("# Multi-seed experiments: trained vs random\n\n" + _md(pd.DataFrame(rows)))

    parts = ["# Ablation results\n"]
    abl = svc.experiments.experiments("ablation")
    if abl.empty:
        parts.append("NOT RUN - no ablation data available.\n")
    for _, e in abl.iterrows():
        df, stats = svc.experiments.ablation(int(e["experiment_id"]))
        parts.append(f"\n## Ablation #{int(e['experiment_id'])} (git {e['git_sha']})\n\n")
        parts.append(_md(df.groupby("variant")["final_mean"].agg(["mean", "std", "count"]).reset_index()))
        parts.append("\n" + _md(stats))
    (out / "ablation.md").write_text("".join(parts))
    print(f"Wrote tables to {out}/")


if __name__ == "__main__":
    main()
