# Experiments

## Plan

| # | Command | Purpose |
|---|---|---|
| 1 | `sla pipeline --config configs/frozenlake_qlearning.yaml --seeds 0 1 2 3 4` | Q-learning vs random on FrozenLake |
| 2 | `sla pipeline --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4` | DQN vs random on CartPole |
| 3 | `sla ablation --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4` | contribution of replay and the target network |
| 4 | `python scripts/make_tables.py` | regenerate `results/*.md` |

Experiments 2 and 3 take a while on a CPU (15 runs for the ablation); run them overnight if needed. Each experiment is stored with its git SHA, so commit your code before running.

## Recording results

- Never edit numbers in `results/` by hand; regenerate them.
- Report the held-out **test** numbers (not training reward) together with the random baseline and the number of seeds.
- Keep failed or weak seeds in the tables.

## Results log

See `results/comparison.md`, `results/experiments.md` and `results/ablation.md` (generated). Until experiments are run they contain NOT RUN.
