import math
import time

import pytest

from sla.training.safety import SafetyLimits, check_finite
from sla.utils.errors import TrainingError


def test_check_finite():
    assert check_finite(1.5, "reward") == 1.5
    with pytest.raises(TrainingError, match="reward"):
        check_finite(math.nan, "reward")


def test_limits():
    limits = SafetyLimits(max_steps_per_episode=50, max_episodes=10, max_wall_clock_s=0.01)
    assert limits.step_limit_reached(50) and not limits.step_limit_reached(49)
    start = time.monotonic()
    time.sleep(0.02)
    assert limits.wall_clock_exceeded(start)
