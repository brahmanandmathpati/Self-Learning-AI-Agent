"""the runner validates every transition through a callback."""

import math

import pytest

from sla.training.runner import Callback, run_training
from sla.utils.errors import ValidationError
from sla.utils.validation import TransitionValidationCallback


def test_every_transition_is_checked(fl_cfg):
    fl_cfg.episodes = 10
    cb = TransitionValidationCallback(fl_cfg.env_name)
    result = run_training(fl_cfg, [cb])
    assert cb.checked == sum(result.lengths)


class CorruptReward(Callback):
    """Pretends the environment returned a broken reward."""

    def on_step(self, ctx, transition):
        transition.reward = math.nan


def test_corrupted_transition_stops_training(fl_cfg):
    fl_cfg.episodes = 5
    with pytest.raises(ValidationError, match="NaN"):
        run_training(fl_cfg, [CorruptReward(), TransitionValidationCallback(fl_cfg.env_name)])
