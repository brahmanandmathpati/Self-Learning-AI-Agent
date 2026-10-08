"""Statistics for comparing agents across seeds.

With only 5 seeds, report a mean, a 95% bootstrap confidence interval and a
Welch t-test (it does not assume equal variances) — never a single run.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy import stats as sps


def bootstrap_ci(values: Sequence[float], n_boot: int = 10_000, ci: float = 0.95,
                 seed: int = 0) -> tuple[float, float]:
    """Confidence interval for the mean, by resampling with replacement."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.size < 2:
        raise ValueError("Need at least 2 values for a confidence interval")
    rng = np.random.default_rng(seed)
    means = rng.choice(arr, size=(n_boot, arr.size), replace=True).mean(axis=1)
    alpha = (1.0 - ci) / 2.0
    return float(np.quantile(means, alpha)), float(np.quantile(means, 1.0 - alpha))


def bootstrap_diff_ci(a: Sequence[float], b: Sequence[float], n_boot: int = 10_000, ci: float = 0.95,
                      seed: int = 0) -> tuple[float, float]:
    """Confidence interval for mean(a) - mean(b)."""
    x, y = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    if x.size < 2 or y.size < 2:
        raise ValueError("Each group needs at least 2 values")
    rng = np.random.default_rng(seed)
    diffs = (rng.choice(x, size=(n_boot, x.size)).mean(axis=1)
             - rng.choice(y, size=(n_boot, y.size)).mean(axis=1))
    alpha = (1.0 - ci) / 2.0
    return float(np.quantile(diffs, alpha)), float(np.quantile(diffs, 1.0 - alpha))


def welch_t_test(a: Sequence[float], b: Sequence[float]) -> tuple[float, float]:
    """Return (t statistic, two-sided p-value) for mean(a) vs mean(b).

    When both groups have zero variance the test is undefined; we then return t = +/-inf and p = 0
    if the means differ (the groups are perfectly separated) or t = 0 and p = 1 if they are equal.
    """
    x, y = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    if x.size < 2 or y.size < 2:
        raise ValueError("Each group needs at least 2 values for Welch's t-test")
    if np.var(x, ddof=1) == 0 and np.var(y, ddof=1) == 0:
        diff = float(x.mean() - y.mean())
        return (float(np.sign(diff)) * float("inf"), 0.0) if diff != 0 else (0.0, 1.0)
    result = sps.ttest_ind(x, y, equal_var=False)
    return float(result.statistic), float(result.pvalue)


def compare_groups(a: Sequence[float], b: Sequence[float], name_a: str = "A", name_b: str = "B") -> dict:
    """Everything needed for one row of the results table."""
    t, p = welch_t_test(a, b)
    low, high = bootstrap_diff_ci(a, b)
    return {f"mean_{name_a}": float(np.mean(a)), f"mean_{name_b}": float(np.mean(b)),
            "diff": float(np.mean(a) - np.mean(b)), "diff_ci_low": low, "diff_ci_high": high,
            "t": t, "p_value": p, "n_a": len(a), "n_b": len(b),
            "significant_0_05": bool(p < 0.05 and (low > 0 or high < 0))}
