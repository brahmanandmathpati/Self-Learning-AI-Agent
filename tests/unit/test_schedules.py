import numpy as np
import pytest

from sla.agents.schedules import LinearSchedule


def test_linear_schedule():
    s = LinearSchedule(1.0, 0.1, 100)
    assert s.value(0) == 1.0
    assert np.isclose(s.value(50), 0.55)
    assert np.isclose(s.value(100), 0.1) and np.isclose(s.value(10_000), 0.1)


def test_negative_step_treated_as_zero():
    assert LinearSchedule(1.0, 0.0, 10).value(-5) == 1.0


def test_duration_must_be_positive():
    with pytest.raises(ValueError):
        LinearSchedule(1.0, 0.0, 0)
