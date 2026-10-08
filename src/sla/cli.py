"""Command-line interface: ``sla <command>`` (also ``python -m sla <command>``)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from sla import __version__
from sla.utils.errors import SLAError


def _services(args: argparse.Namespace):
    from sla.services import get_services
    return get_services(args.db)


def _load_cfg(args: argparse.Namespace):
    from sla.training.config import load_config, validate_config
    cfg = load_config(args.config)
    if getattr(args, "episodes", None) is not None:
        cfg = replace(cfg, episodes=args.episodes)
    if getattr(args, "seed", None) is not None:
        cfg = replace(cfg, seed=args.seed)
    if getattr(args, "run_root", None):
        cfg = replace(cfg, run_root=args.run_root)
    return validate_config(cfg)


def _print_run(out) -> None:
    f = out.final_eval
    print(f"Run id: {out.run_id}  ({out.train.stopped_reason}, {out.train.episodes_completed} episodes)")
    if out.initial_eval is not None:
        print(f"Before training (untrained policy, test seeds): mean {out.initial_eval.mean_return:.2f}")
    print(f"After training  (best checkpoint, test seeds):  mean {f.mean_return:.2f} ± {f.std_return:.2f}, "
          f"median {f.median_return:.2f}, success {f.success_rate:.0%} over {f.n_episodes} episodes")
    print(f"Folder: {out.train.run_dir}")


def cmd_train(args: argparse.Namespace) -> int:
    svc = _services(args)
    if args.resume:
        out = svc.training.resume(args.resume, args.eval_episodes)
    else:
        if not args.config:
            raise SLAError("Give --config <yaml> (or --resume <run_dir>)")
        out = svc.training.train(_load_cfg(args), args.eval_episodes)
    _print_run(out)
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    svc = _services(args)
    res, folder = svc.evaluation.evaluate_run(args.run, args.checkpoint, args.episodes, record=not args.no_record)
    print(f"{folder}: mean {res.mean_return:.2f} ± {res.std_return:.2f}, median {res.median_return:.2f}, "
          f"success {res.success_rate:.0%}, mean length {res.mean_length:.1f} over {res.n_episodes} test "
          f"episodes (epsilon = 0, no learning)")
    return 0


def cmd_pipeline(args: argparse.Namespace) -> int:
    from sla.utils.validation import validate_seeds
    svc = _services(args)
    cfg = _load_cfg(args)
    out = svc.training.experiment(cfg, validate_seeds(args.seeds), args.eval_episodes, not args.no_baseline)
    for r in out.runs:
        print(f"[{r.run_id}] test mean {r.final_eval.mean_return:.2f} ± {r.final_eval.std_return:.2f}")
    s = out.summary
    if "trained_vs_random" in s:
        c = s["trained_vs_random"]
        print(f"Trained {c['mean_trained']:.2f} vs random {c['mean_random']:.2f}: diff {c['diff']:.2f} "
              f"(bootstrap 95% CI {c['diff_ci_low']:.2f} .. {c['diff_ci_high']:.2f}), Welch p = {c['p_value']:.4g}")
    if "trained_vs_untrained" in s:
        c = s["trained_vs_untrained"]
        print(f"Before/after: untrained {c['mean_untrained']:.2f} -> trained {c['mean_trained']:.2f} "
              f"(95% CI of gain {c['diff_ci_low']:.2f} .. {c['diff_ci_high']:.2f})")
    print(f"Experiment #{out.experiment_id} stored in the database.")
    if args.reflect:
        for r in out.runs:
            res = svc.reflection.generate(r.run_id, use_llm=args.llm)
            print(f"  note ({res.shown.source}) for {r.run_id}: {res.shown.text}")
    return 0


def cmd_ablation(args: argparse.Namespace) -> int:
    from sla.evaluation.ablation import run_ablation
    from sla.utils.validation import validate_seeds
    svc = _services(args)
    exp_id, df, stats = run_ablation(_load_cfg(args), validate_seeds(args.seeds), svc.db, args.variants,
                                     args.eval_episodes)
    print(df.to_string(index=False))
    print(stats.round(4).to_string(index=False) if not stats.empty else "Need >= 2 seeds per variant for statistics.")
    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        df.to_csv(out / "ablation.csv", index=False)
        stats.to_csv(out / "ablation_stats.csv", index=False)
        print(f"Saved CSV files to {out}")
    print(f"Ablation experiment #{exp_id} stored in the database.")
    return 0


def cmd_baseline(args: argparse.Namespace) -> int:
    from sla.utils.validation import validate_seeds
    svc = _services(args)
    results = svc.training.baseline(_load_cfg(args), validate_seeds(args.seeds), args.eval_episodes)
    for seed, r in zip(args.seeds, results):
        print(f"random seed {seed}: mean {r.mean_return:.2f} ± {r.std_return:.2f}")
    return 0


def cmd_reflect(args: argparse.Namespace) -> int:
    svc = _services(args)
    run_id = Path(args.run).name
    result = svc.reflection.generate(run_id, use_llm=args.llm)
    if result.rejected:
        print(f"Rejected LLM note (unsupported numbers {result.rejected.report.unsupported}):")
        print(f"  {result.rejected.text}")
    print(f"Note #{result.shown.note_id} ({result.shown.source}, grounded={result.shown.report.passed}):")
    print(result.shown.text)
    return 0


def cmd_runs(args: argparse.Namespace) -> int:
    runs = _services(args).experiments.runs()
    if runs.empty:
        print("No runs yet. Start one with: sla train --config configs/frozenlake_qlearning.yaml")
        return 0
    cols = ["run_id", "env", "algorithm", "seed", "variant", "status", "episodes_completed", "started_at"]
    print(runs[cols].to_string(index=False))
    return 0


def cmd_init_db(args: argparse.Namespace) -> int:
    svc = _services(args)
    print(f"Database ready at {svc.db.path} (schema version {svc.db.schema_version()})")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    from sla import settings
    app = Path(__file__).resolve().parent / "app" / "main.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(app), "--server.port", str(args.port)]
    root = settings.PROJECT_ROOT if (settings.PROJECT_ROOT / ".streamlit").is_dir() else None
    return subprocess.call(cmd, cwd=root)  # cwd with .streamlit/config.toml -> project theme


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--db", help="SQLite database (default: env SLA_DB or runs/sla.db)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sla", description="Self-Learning AI Agent")
    parser.add_argument("--version", action="version", version=f"sla {__version__}")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("train", help="train one run from a YAML config, or resume a run")
    p.add_argument("--config", help="e.g. configs/cartpole_dqn.yaml")
    p.add_argument("--resume", metavar="RUN_DIR", help="continue runs/<run_id> from its latest checkpoint")
    p.add_argument("--seed", type=int)
    p.add_argument("--episodes", type=int)
    p.add_argument("--run-root", help="folder for run directories (default from config)")
    p.add_argument("--eval-episodes", type=int, default=100, help="held-out test episodes after training")
    _add_common(p)
    p.set_defaults(func=cmd_train)

    p = sub.add_parser("evaluate", help="frozen-policy evaluation of a run (epsilon = 0, no learning)")
    p.add_argument("--run", required=True, help="run folder, e.g. runs/<run_id>")
    p.add_argument("--checkpoint", default="best", help="best | latest | ep_000499")
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--no-record", action="store_true", help="do not store the result in the database")
    _add_common(p)
    p.set_defaults(func=cmd_evaluate)

    p = sub.add_parser("pipeline", help="multi-seed training + test evaluation + random baseline + statistics")
    p.add_argument("--config", required=True)
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    p.add_argument("--episodes", type=int)
    p.add_argument("--run-root")
    p.add_argument("--eval-episodes", type=int, default=100)
    p.add_argument("--no-baseline", action="store_true")
    p.add_argument("--reflect", action="store_true", help="also write a grounded note per run")
    p.add_argument("--llm", action="store_true", help="try the local Ollama model for notes")
    _add_common(p)
    p.set_defaults(func=cmd_pipeline)

    p = sub.add_parser("ablation", help="full DQN vs no replay vs no target network")
    p.add_argument("--config", default="configs/cartpole_dqn.yaml")
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    p.add_argument("--variants", nargs="+", choices=["full", "no_replay", "no_target"])
    p.add_argument("--episodes", type=int)
    p.add_argument("--run-root")
    p.add_argument("--eval-episodes", type=int, default=100)
    p.add_argument("--out-dir", default="results/ablation")
    _add_common(p)
    p.set_defaults(func=cmd_ablation)

    p = sub.add_parser("baseline", help="random-action baseline on the held-out test seeds")
    p.add_argument("--config", required=True)
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    p.add_argument("--eval-episodes", type=int, default=100)
    _add_common(p)
    p.set_defaults(func=cmd_baseline)

    p = sub.add_parser("reflect", help="grounded plain-language note for a run")
    p.add_argument("--run", required=True, help="run folder or run id")
    p.add_argument("--llm", action="store_true", help="try the local Ollama model (template if unavailable)")
    _add_common(p)
    p.set_defaults(func=cmd_reflect)

    p = sub.add_parser("runs", help="list stored runs")
    _add_common(p)
    p.set_defaults(func=cmd_runs)

    p = sub.add_parser("init-db", help="create or migrate the SQLite database")
    _add_common(p)
    p.set_defaults(func=cmd_init_db)

    p = sub.add_parser("dashboard", help="open the Streamlit dashboard")
    p.add_argument("--port", type=int, default=8501)
    p.set_defaults(func=cmd_dashboard)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        return int(args.func(args) or 0)
    except (SLAError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
