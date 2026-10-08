import pandas as pd
import pytest

from sla.evaluation.plots import plot_eval_curve, plot_learning_curve, plot_seed_band


@pytest.fixture
def df():
    return pd.DataFrame({"episode": range(100), "total_reward": [i % 10 for i in range(100)]})


def test_learning_curve_saved_with_labels(df, tmp_path):
    out = tmp_path / "plots" / "curve.png"
    fig = plot_learning_curve(df, window=10, title="test", out_path=out)
    ax = fig.axes[0]
    assert out.exists() and out.stat().st_size > 0
    assert ax.get_xlabel() == "Episode" and ax.get_ylabel() == "Total reward" and ax.get_title() == "test"


def test_learning_curve_rejects_bad_df():
    with pytest.raises(ValueError):
        plot_learning_curve(pd.DataFrame({"x": [1]}))


def test_seed_band(df, tmp_path):
    fig = plot_seed_band({0: df, 1: df}, window=5, out_path=tmp_path / "band.png")
    assert (tmp_path / "band.png").exists() and len(fig.axes) == 1


def test_eval_curve(tmp_path):
    evals = pd.DataFrame({"checkpoint_episode": [49, 99], "mean_return": [10.0, 50.0], "std_return": [2.0, 5.0]})
    plot_eval_curve(evals, out_path=tmp_path / "eval.png")
    assert (tmp_path / "eval.png").exists()
