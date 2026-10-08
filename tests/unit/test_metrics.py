import pytest

from sla.evaluation.metrics import (
    area_under_curve,
    episodes_to_threshold,
    first_last_fraction,
    success_rate,
    summarize,
)


def test_summarize():
    s = summarize([1, 2, 3])
    assert s["mean"] == 2 and s["median"] == 2 and s["n"] == 3


def test_success_rate():
    assert success_rate([500, 200, 500, 500], 500) == 0.75


def test_episodes_to_threshold_known_answer():
    returns = [0] * 10 + [10] * 10
    assert episodes_to_threshold(returns, threshold=10, window=5) == 14
    assert episodes_to_threshold([1, 1, 1], threshold=5, window=2) is None


def test_first_last_fraction():
    first, last = first_last_fraction(list(range(100)), 0.05)
    assert first == pytest.approx(2.0) and last == pytest.approx(97.0)


def test_auc():
    assert area_under_curve([0, 10]) == 5


def test_empty_raises():
    with pytest.raises(ValueError):
        summarize([])
