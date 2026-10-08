import numpy as np
import pytest
from scipy import stats

from sla.evaluation.stats import bootstrap_ci, bootstrap_diff_ci, compare_groups, welch_t_test


def test_welch_matches_scipy():
    a, b = [10, 12, 11, 13, 12], [5, 6, 7, 5, 6]
    t, p = welch_t_test(a, b)
    ref = stats.ttest_ind(a, b, equal_var=False)
    assert t == pytest.approx(ref.statistic) and p == pytest.approx(ref.pvalue)


def test_bootstrap_ci_contains_mean():
    values = [10, 12, 11, 13, 12]
    low, high = bootstrap_ci(values, n_boot=2000)
    assert low <= np.mean(values) <= high


def test_diff_ci_excludes_zero_for_clear_gap():
    low, high = bootstrap_diff_ci([100, 101, 102, 103], [1, 2, 3, 4], n_boot=2000)
    assert low > 0


def test_compare_groups_keys():
    out = compare_groups([1, 2, 3], [1, 2, 4], "dqn", "random")
    assert {"mean_dqn", "mean_random", "p_value", "diff_ci_low"} <= set(out)


def test_too_few_values():
    with pytest.raises(ValueError):
        bootstrap_ci([1])
