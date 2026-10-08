# Training

## Configuration (YAML)

| Key | Meaning |
|---|---|
| `env_name`, `env_kwargs` | `FrozenLake-v1` (`map_name`, `is_slippery`) or `CartPole-v1` |
| `agent` | `random`, `q_learning` or `dqn` |
| `episodes`, `seed` | number of training episodes; training seed |
| `learning_rate`, `gamma` | α (Q-learning step size / optimiser learning rate) and discount γ |
| `epsilon_start`, `epsilon_end`, `epsilon_decay_steps` | linear ε schedule over environment steps |
| `max_steps_per_episode`, `max_wall_clock_s` | safety limits |
| `eval_every`, `eval_episodes` | validation evaluation frequency and size (selects the best checkpoint) |
| `checkpoint_every` | periodic checkpoint frequency |
| `dqn.hidden_size, batch_size, buffer_size, learning_starts, train_freq` | DQN network and replay settings |
| `dqn.target_update_every` | gradient steps between target-network syncs |
| `dqn.grad_clip`, `dqn.optimizer` (`adam`/`adamw`), `dqn.weight_decay` | optimisation |
| `dqn.replay_enabled`, `dqn.target_net_enabled` | ablation switches |

Unknown keys and invalid values are rejected with an error that names the key.

Provided configs: `frozenlake_qlearning.yaml`, `frozenlake_random.yaml`, `cartpole_dqn.yaml`, `cartpole_random.yaml`, `ablation_no_replay.yaml`, `ablation_no_target.yaml`, `smoke_cartpole_dqn.yaml` (seconds; for tests and demos, not for results).

## Run folder

```
runs/<env>_<agent>_s<seed>_<timestamp>/
  config.yaml          exact config used
  run.log              log with the run id on every line
  metrics.json         initial and final (test) evaluation, git SHA
  checkpoints/ep_000049/ ...  periodic checkpoints (last 3 kept)
  checkpoints/best/     best validation checkpoint (used for the final evaluation)
  checkpoints/latest.json
```

A checkpoint holds everything needed to resume: Q-table or online/target network weights, optimiser state, replay buffer, step counters and RNG states. Because every episode resets the environment with `seed×100000+episode`, a stopped and resumed Q-learning run produces exactly the same returns as an uninterrupted one (tested).

## Resume

```bash
sla train --resume runs/<run_id>
```

Runs interrupted from the dashboard or with Ctrl+C are marked `stopped` and can be resumed.
