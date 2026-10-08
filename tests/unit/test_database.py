import pytest

from sla.database.store import SCHEMA_VERSION, Database
from sla.evaluation.evaluate import EvalResult
from sla.training.runner import EpisodeInfo
from sla.utils.errors import StoreError


def info(ep, reward=1.0):
    return EpisodeInfo(ep, reward, 10, 0.5, None, "hole", 0.01)


def ev(mean=20.0):
    return EvalResult(mean, 3.0, 0.0, 3, [mean - 1, mean, mean + 1], mean, 15.0, [14, 15, 16])


def test_schema_created_and_versioned(tmp_path):
    db = Database(tmp_path / "x.db")
    assert db.schema_version() == SCHEMA_VERSION
    assert Database(tmp_path / "x.db").migrate() == SCHEMA_VERSION  # re-opening does not re-apply
    assert set(db.counts()) >= {"experiments", "runs", "episodes", "evaluations", "ablation_results", "reflections"}


def test_run_and_episodes_persist_after_reopen(tmp_path):
    path = tmp_path / "e.db"
    db = Database(path)
    db.start_run("r1", "FrozenLake-v1", "q_learning", 0, {"a": 1}, "runs/r1", "abc123")
    for ep in range(10):
        db.log_episode("r1", info(ep, float(ep)))
    db.finish_run("r1", "completed", 10, "completed")
    again = Database(path)  # like restarting the program
    df = again.query_episodes("r1")
    run = again.get_run("r1")
    assert df["total_reward"].tolist() == [float(i) for i in range(10)]
    assert run["status"] == "completed" and run["git_sha"] == "abc123" and run["config"] == {"a": 1}
    assert run["episodes_completed"] == 10 and run["ended_at"]


def test_retrieval_accuracy_1000_rows(db):
    db.start_run("r", "CartPole-v1", "dqn", 1, {})
    for ep in range(1000):
        db.log_episode("r", info(ep, ep * 0.5))
    df = db.query_episodes("r")
    assert (df["total_reward"] == df["episode"] * 0.5).all() and len(df) == 1000


def test_foreign_key_enforced(db):
    with pytest.raises(StoreError):
        db.log_episode("no_such_run", info(0))


def test_evaluations_metrics_checkpoints(db):
    db.start_run("r", "CartPole-v1", "dqn", 0, {})
    db.log_evaluation("r", "validation", ev(20.0), episode=49)
    db.log_evaluation("r", "test", ev(30.0), episode=49, seed_base=20_000_000, checkpoint="runs/r/checkpoints/best")
    db.log_metric("r", "test_mean_return", 30.0)
    db.set_checkpoints("r", latest="runs/r/checkpoints/ep_000049", best="runs/r/checkpoints/best")
    tests = db.query_evaluations("r", "test")
    assert len(db.query_evaluations("r")) == 2 and tests.iloc[0]["mean_return"] == 30.0
    assert tests.iloc[0]["algorithm"] == "dqn"
    assert db.query_metrics("r")["name"].tolist() == ["test_mean_return"]
    assert db.get_run("r")["best_checkpoint"].endswith("best")


def test_experiments_ablation_reflections_feedback(db):
    exp = db.create_experiment("abl", "ablation", "CartPole-v1", "dqn", {"x": 1}, [0, 1])
    db.start_run("r", "CartPole-v1", "dqn", 0, {}, experiment_id=exp, variant="full")
    db.log_ablation(exp, "full", 0, "r", 100.0, 5.0, 0.0)
    db.finish_experiment(exp, "completed", {"ok": True})
    note = db.add_reflection("r", {"x": 1}, "text", "template", True)
    db.add_feedback(note, True, 4, "nice")
    assert db.get_experiment(exp)["summary"] == {"ok": True}
    assert db.get_experiment(exp)["seeds"] == [0, 1]
    assert db.query_ablation(exp)["final_mean"].tolist() == [100.0]
    assert db.list_runs(exp)["variant"].tolist() == ["full"]
    assert db.get_reflection(note)["note_text"] == "text"
    assert db.query_feedback(note)["usefulness"].tolist() == [4]


def test_delete_cascades(db):
    db.start_run("r", "CartPole-v1", "dqn", 0, {})
    db.log_episode("r", info(0))
    db.log_evaluation("r", "test", ev())
    db.delete_run("r")
    assert db.query_episodes("r").empty and db.query_evaluations("r").empty


def test_failed_run_records_error(db):
    db.start_run("r", "CartPole-v1", "dqn", 0, {})
    db.finish_run("r", "failed", error="TrainingError: boom")
    assert db.get_run("r")["status"] == "failed" and "boom" in db.get_run("r")["error"]
