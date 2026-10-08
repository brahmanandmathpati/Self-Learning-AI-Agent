import pytest

from sla.training.config import RunConfig, config_from_dict, load_config, save_config
from sla.utils.errors import ConfigError


def write(tmp_path, text):
    path = tmp_path / "cfg.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_loads_valid_file(tmp_path):
    cfg = load_config(write(tmp_path, "env_name: CartPole-v1\nagent: dqn\nepisodes: 10\n"))
    assert cfg.env_name == "CartPole-v1" and cfg.episodes == 10 and cfg.dqn.batch_size == 64


def test_repo_configs_are_valid():
    names = ["frozenlake_qlearning", "frozenlake_random", "cartpole_random", "cartpole_dqn",
             "ablation_no_replay", "ablation_no_target", "smoke_cartpole_dqn"]
    for name in names:
        assert isinstance(load_config(f"configs/{name}.yaml"), RunConfig)
    assert load_config("configs/ablation_no_replay.yaml").dqn.replay_enabled is False
    assert load_config("configs/ablation_no_target.yaml").dqn.target_net_enabled is False


def test_missing_file(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        load_config(tmp_path / "nope.yaml")


def test_invalid_yaml(tmp_path):
    with pytest.raises(ConfigError, match="not valid YAML"):
        load_config(write(tmp_path, "episodes: [1, 2\n"))


@pytest.mark.parametrize("key,value", [
    ("gamma", 1.5), ("gamma", 0), ("learning_rate", -0.1), ("episodes", 0),
    ("episodes", "many"), ("env_name", "Pong-v5"), ("agent", "ppo"), ("seed", -1),
])
def test_bad_values_name_the_key(key, value):
    with pytest.raises(ConfigError, match=key):
        config_from_dict({key: value})


def test_unknown_key_rejected():
    with pytest.raises(ConfigError, match="Unknown config key"):
        config_from_dict({"episodez": 10})


def test_bad_dqn_value():
    with pytest.raises(ConfigError, match="dqn.batch_size"):
        config_from_dict({"agent": "dqn", "env_name": "CartPole-v1", "dqn": {"batch_size": 0}})


def test_save_and_reload(tmp_path):
    cfg = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn", "dqn": {"hidden_size": 64}})
    again = load_config(save_config(cfg, tmp_path / "copy.yaml"))
    assert again == cfg
