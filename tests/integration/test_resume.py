from dataclasses import replace

from sla.checkpoints.manager import CheckpointCallback, latest_checkpoint, load_checkpoint, resume_training
from sla.training.callbacks import DatabaseCallback
from sla.training.pipeline import resume_run
from sla.training.runner import Callback, run_training


class StopAt(Callback):
    def __init__(self, episode):
        self.episode = episode

    def on_episode_end(self, ctx, info):
        return info.episode >= self.episode


def test_resume_continues_episode_count(fl_cfg, db):
    cfg = replace(fl_cfg, episodes=200)
    first = run_training(cfg, [DatabaseCallback(db), CheckpointCallback(50, db=db), StopAt(119)])
    assert first.episodes_completed == 120
    assert db.get_run(first.run_id)["status"] == "stopped"
    _, info = load_checkpoint(latest_checkpoint(first.run_dir))
    assert info["episode"] == 119
    resumed = resume_training(first.run_dir, [DatabaseCallback(db), CheckpointCallback(50, db=db)])
    assert resumed.episodes_completed == 200 and len(resumed.returns) == 80
    assert len(db.query_episodes(first.run_id)) == 200
    assert db.get_run(first.run_id)["status"] == "completed"


def test_resumed_run_matches_uninterrupted_run(fl_cfg, tmp_path):
    """Q-learning + per-episode reset seeds: stop/resume gives the same returns as one long run."""
    cfg = replace(fl_cfg, episodes=150)
    full = run_training(cfg, run_dir=tmp_path / "full")
    part = run_training(cfg, [CheckpointCallback(50), StopAt(99)], run_dir=tmp_path / "part")
    rest = resume_training(part.run_dir, [CheckpointCallback(50)])
    assert part.returns + rest.returns == full.returns


def test_resume_run_pipeline_adds_final_eval(fl_cfg, db):
    cfg = replace(fl_cfg, episodes=200)
    first = run_training(cfg, [DatabaseCallback(db), CheckpointCallback(50, db=db), StopAt(99)])
    out = resume_run(first.run_dir, db, final_eval_episodes=5)
    assert out.train.episodes_completed == 200
    assert len(db.query_evaluations(first.run_id, "test")) == 1
