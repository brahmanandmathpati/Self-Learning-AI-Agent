import yaml

from sla.cli import main


def small_config(tmp_path, episodes=100):
    cfg = {"env_name": "FrozenLake-v1", "env_kwargs": {"is_slippery": False}, "agent": "q_learning",
           "episodes": episodes, "learning_rate": 0.5, "epsilon_decay_steps": 800, "max_steps_per_episode": 100,
           "eval_every": 50, "eval_episodes": 5, "checkpoint_every": 50, "run_root": str(tmp_path / "runs")}
    path = tmp_path / "cfg.yaml"
    path.write_text(yaml.safe_dump(cfg))
    return path


def test_train_evaluate_reflect_runs(tmp_path, capsys):
    cfg = small_config(tmp_path)
    db = str(tmp_path / "c.db")
    assert main(["train", "--config", str(cfg), "--db", db, "--eval-episodes", "5"]) == 0
    out = capsys.readouterr().out
    assert "After training" in out and "Before training" in out
    run_dir = next((tmp_path / "runs").iterdir())
    assert main(["evaluate", "--run", str(run_dir), "--episodes", "5", "--db", db]) == 0
    assert "epsilon = 0" in capsys.readouterr().out
    assert main(["reflect", "--run", str(run_dir), "--db", db]) == 0
    assert "template" in capsys.readouterr().out
    assert main(["runs", "--db", db]) == 0
    assert run_dir.name in capsys.readouterr().out


def test_pipeline_two_seeds_with_statistics(tmp_path, capsys):
    cfg = small_config(tmp_path, episodes=150)
    db = str(tmp_path / "p.db")
    assert main(["pipeline", "--config", str(cfg), "--seeds", "0", "1", "--eval-episodes", "5", "--db", db]) == 0
    out = capsys.readouterr().out
    assert "Welch p" in out and "Experiment #1" in out


def test_bad_config_gives_clear_error(tmp_path, capsys):
    bad = tmp_path / "bad.yaml"
    bad.write_text("gamma: 5\n")
    assert main(["train", "--config", str(bad), "--db", str(tmp_path / "x.db")]) == 1
    assert "gamma" in capsys.readouterr().err


def test_evaluate_non_run_folder_error(tmp_path, capsys):
    assert main(["evaluate", "--run", str(tmp_path), "--db", str(tmp_path / "x.db")]) == 1
    assert "not a run folder" in capsys.readouterr().err


def test_init_db(tmp_path, capsys):
    assert main(["init-db", "--db", str(tmp_path / "n.db")]) == 0
    assert "schema version 1" in capsys.readouterr().out
