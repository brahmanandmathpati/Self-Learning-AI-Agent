import math

from sla.training.guards import detect_regression, is_diverging


def test_divergence():
    assert is_diverging(math.nan, None)
    assert is_diverging(None, math.inf)
    assert is_diverging(1e9, 0.1)
    assert not is_diverging(50.0, 0.1)
    assert not is_diverging(None, None)


def test_regression_detected_after_three_drops():
    assert detect_regression([100, 200, 150, 150, 150], drop_fraction=0.2, patience=3)


def test_no_regression_when_recovering():
    assert not detect_regression([100, 200, 150, 150, 190], 0.2, 3)
    assert not detect_regression([100, 200], 0.2, 3)
