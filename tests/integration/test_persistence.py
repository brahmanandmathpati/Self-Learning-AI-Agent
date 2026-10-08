"""learning survives saving, exiting and reloading in a new process."""

import subprocess
import sys

import numpy as np

from sla.checkpoints.manager import CheckpointCallback, latest_checkpoint, load_checkpoint
from sla.evaluation.evaluate import evaluate_agent
from sla.training.runner import run_training


def test_reloaded_agent_has_same_q_table_and_score(fl_cfg):
    result = run_training(fl_cfg, [CheckpointCallback(100)])
    agent, _ = load_checkpoint(latest_checkpoint(result.run_dir))
    again, _ = load_checkpoint(latest_checkpoint(result.run_dir))
    assert np.array_equal(agent.q, again.q)
    a = evaluate_agent(agent, fl_cfg.env_name, fl_cfg.env_kwargs, 20)
    b = evaluate_agent(again, fl_cfg.env_name, fl_cfg.env_kwargs, 20)
    assert a.mean_return == b.mean_return


def test_new_process_gets_same_score(fl_cfg):
    result = run_training(fl_cfg, [CheckpointCallback(100)])
    folder = latest_checkpoint(result.run_dir)
    agent, _ = load_checkpoint(folder)
    here = evaluate_agent(agent, fl_cfg.env_name, fl_cfg.env_kwargs, 20).mean_return
    code = (
        "from sla.checkpoints.manager import load_checkpoint;"
        "from sla.evaluation.evaluate import evaluate_agent;"
        f"a,_=load_checkpoint(r'{folder}');"
        f"print(evaluate_agent(a,'{fl_cfg.env_name}',{fl_cfg.env_kwargs!r},20).mean_return)"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert float(out.stdout.strip()) == here
