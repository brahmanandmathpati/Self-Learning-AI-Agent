import json
from dataclasses import replace

from sla.training.pipeline import run_experiment, train_run


def test_train_run_stores_everything(fl_cfg, db):
    out = train_run(fl_cfg, db, final_eval_episodes=10)
    metrics = json.loads((out.train.run_dir / "metrics.json").read_text())
    run = db.get_run(out.run_id)
    assert metrics["final_eval"]["n_episodes"] == 10 and metrics["final_eval"]["seed_base"] == 20_000_000
    assert (out.train.run_dir / "checkpoints" / "best" / "checkpoint.json").exists()
    assert (out.train.run_dir / "run.log").exists()
    assert run["status"] == "completed" and run["best_checkpoint"] and run["latest_checkpoint"]
    assert len(db.query_episodes(out.run_id)) == fl_cfg.episodes
    assert len(db.query_evaluations(out.run_id, "validation")) == fl_cfg.episodes // fl_cfg.eval_every
    assert len(db.query_evaluations(out.run_id, "initial")) == 1
    assert len(db.query_evaluations(out.run_id, "test")) == 1


def test_experiment_with_baseline_and_statistics(fl_cfg, db):
    out = run_experiment(replace(fl_cfg, episodes=200), [0, 1], db, final_eval_episodes=5)
    exp = db.get_experiment(out.experiment_id)
    assert exp["status"] == "completed" and len(out.runs) == 2 and len(out.baseline) == 2
    s = exp["summary"]
    assert len(s["trained_test_means"]) == 2 and len(s["baseline_test_means"]) == 2
    assert {"p_value", "diff_ci_low", "diff_ci_high"} <= set(s["trained_vs_random"])
    runs = db.list_runs(out.experiment_id)
    assert sorted(runs["algorithm"].tolist()) == ["q_learning", "q_learning", "random", "random"]


def test_failed_run_is_marked_failed(fl_cfg, db, monkeypatch):
    import pytest

    from sla.training import pipeline

    def boom(*args, **kwargs):
        raise RuntimeError("disk full")
    monkeypatch.setattr(pipeline, "final_evaluation", boom)
    with pytest.raises(RuntimeError):
        train_run(replace(fl_cfg, episodes=100), db, final_eval_episodes=5)
    runs = db.list_runs()
    assert runs.iloc[0]["status"] == "failed" and "disk full" in runs.iloc[0]["error"]
