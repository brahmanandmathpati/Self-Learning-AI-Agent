import numpy as np

from sla.training.runner import Callback, run_training


class Recorder(Callback):
    def __init__(self, stop_after=None):
        self.steps, self.episodes, self.stop_after = 0, [], stop_after

    def on_step(self, ctx, transition):
        self.steps += 1

    def on_episode_end(self, ctx, info):
        self.episodes.append(info)
        return self.stop_after is not None and len(self.episodes) >= self.stop_after


def test_q_learning_beats_random_on_frozenlake(fl_cfg, tmp_path):
    learned = run_training(fl_cfg, run_dir=tmp_path / "q")
    fl_cfg.agent = "random"
    random = run_training(fl_cfg, run_dir=tmp_path / "r")
    assert np.mean(learned.returns[-50:]) > np.mean(random.returns[-50:])


def test_callbacks_called_and_can_stop(fl_cfg):
    rec = Recorder(stop_after=5)
    result = run_training(fl_cfg, [rec])
    assert result.stopped_reason == "callback" and result.episodes_completed == 5
    assert rec.steps == sum(result.lengths)
    assert (result.run_dir / "config.yaml").exists()


def test_step_limit_truncates(fl_cfg):
    fl_cfg.max_steps_per_episode = 3
    fl_cfg.episodes = 20
    result = run_training(fl_cfg)
    assert max(result.lengths) <= 3


def test_same_seed_same_returns(fl_cfg, tmp_path):
    a = run_training(fl_cfg, run_dir=tmp_path / "a")
    b = run_training(fl_cfg, run_dir=tmp_path / "b")
    assert a.returns == b.returns
