import pytest

from sla.evaluation.ablation import make_variant_config
from sla.training.config import config_from_dict


def test_variants_change_only_their_flag():
    base = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn"})
    no_replay = make_variant_config(base, "no_replay", seed=3)
    assert no_replay.dqn.replay_enabled is False and no_replay.dqn.target_net_enabled is True
    assert no_replay.seed == 3 and base.dqn.replay_enabled is True  # base untouched


def test_full_variant_restores_components_from_an_ablation_config():
    base = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn", "dqn": {"replay_enabled": False}})
    full = make_variant_config(base, "full", seed=0)
    assert full.dqn.replay_enabled is True and full.dqn.target_net_enabled is True


def test_statistics_need_two_seeds_per_group():
    import pandas as pd

    from sla.evaluation.ablation import ablation_statistics
    df = pd.DataFrame({"variant": ["full", "full", "no_replay", "no_replay"], "final_mean": [200, 210, 50, 60]})
    stats = ablation_statistics(df)
    assert stats.iloc[0]["comparison"] == "full vs no_replay" and stats.iloc[0]["diff"] == 150
    assert ablation_statistics(df.iloc[[0, 2]]).empty


def test_unknown_variant_and_wrong_agent():
    base = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn"})
    with pytest.raises(ValueError):
        make_variant_config(base, "no_brain", 0)
    with pytest.raises(ValueError):
        make_variant_config(config_from_dict({}), "full", 0)
