"""A short DQN run on CartPole must finish, log to the database, stay finite, checkpoint and resume."""

import math
from dataclasses import replace

import pytest

pytest.importorskip("torch")

from sla.training.config import load_config  # noqa: E402
from sla.training.pipeline import resume_run, train_run  # noqa: E402

pytestmark = pytest.mark.smoke


def test_dqn_smoke_run_and_resume(tmp_path, db):
    cfg = replace(load_config("configs/smoke_cartpole_dqn.yaml"), run_root=str(tmp_path / "runs"))
    out = train_run(cfg, db, final_eval_episodes=3)
    episodes = db.query_episodes(out.run_id)
    assert len(episodes) == cfg.episodes
    losses = episodes["mean_loss"].dropna()
    assert not losses.empty and all(math.isfinite(v) for v in losses)
    assert (out.train.run_dir / "checkpoints" / "best" / "dqn.pt").exists()
    longer = replace(cfg, episodes=cfg.episodes + 10)
    (out.train.run_dir / "config.yaml").write_text(
        (out.train.run_dir / "config.yaml").read_text().replace(f"episodes: {cfg.episodes}",
                                                                 f"episodes: {longer.episodes}"))
    again = resume_run(out.train.run_dir, db, final_eval_episodes=3)
    assert again.train.episodes_completed == longer.episodes
    assert len(db.query_episodes(out.run_id)) == longer.episodes
