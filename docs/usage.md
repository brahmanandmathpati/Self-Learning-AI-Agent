# Usage

All commands accept `--db <file>` (default `runs/sla.db`, or env `SLA_DB`). `python -m sla ...` is equivalent to `sla ...`.

| Command | Purpose |
|---|---|
| `sla init-db` | create or migrate the database |
| `sla train --config <yaml> [--seed N] [--episodes N] [--eval-episodes 100]` | train one run, then evaluate the best checkpoint on held-out test seeds |
| `sla train --resume runs/<run_id>` | continue a stopped run from its latest checkpoint (same run id) |
| `sla evaluate --run runs/<run_id> [--checkpoint best\|latest\|ep_000499] [--episodes 100] [--no-record]` | frozen-policy evaluation (ε = 0, no learning) |
| `sla pipeline --config <yaml> --seeds 0 1 2 3 4 [--no-baseline] [--reflect] [--llm]` | multi-seed experiment + random baseline + statistics |
| `sla ablation --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4 [--variants full no_replay no_target]` | ablation study; CSVs in `results/ablation/` |
| `sla baseline --config <yaml> --seeds 0 1 2 3 4` | random-action baseline only |
| `sla reflect --run runs/<run_id> [--llm]` | grounded explanation (template if Ollama is unavailable) |
| `sla runs` | list runs |
| `sla dashboard [--port 8501]` | open the Streamlit dashboard |
| `python scripts/make_tables.py` | regenerate `results/*.md` from the database |

## Quick demo (about 1 minute)

```bash
sla pipeline --config configs/frozenlake_qlearning.yaml --seeds 0 1 2 3 4 --reflect
sla train --config configs/smoke_cartpole_dqn.yaml
sla dashboard
```

## Demo flow in the dashboard

1. **Training** → choose FrozenLake + Q-learning (or CartPole + DQN) → *Start training*; watch reward, moving average, ε and loss update.
2. The run saves checkpoints every `checkpoint_every` episodes and the best validation checkpoint automatically.
3. **Run explorer** → select the run → *Evaluate frozen policy now* (held-out test seeds, ε = 0).
4. **Training** → *Multi-seed experiment* (or `sla pipeline`) to get 5 seeds plus the random baseline.
5. **Evaluation** → trained vs random, before vs after, Welch's t-test, bootstrap CI.
6. **Ablation** → full DQN vs no replay vs no target network (after `sla ablation`).
7. **Reflection** → *Generate note*; check the grounded facts and validation badge.
8. **Run explorer** → configuration, git SHA, checkpoints and logs for any run.
