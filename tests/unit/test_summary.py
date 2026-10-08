import pytest

from sla.utils.summary import format_episode_summary, rolling_mean


def test_rolling_mean():
    assert rolling_mean([1, 2, 3, 4], 2) == [1.0, 1.5, 2.5, 3.5]


def test_rolling_mean_bad_window():
    with pytest.raises(ValueError):
        rolling_mean([1], 0)


def test_summary_line():
    line = format_episode_summary(9, [1.0] * 10, window=5, epsilon=0.5)
    assert "Episode     9" in line and "eps 0.50" in line and "1.00" in line
