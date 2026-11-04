# Multi-seed experiments: trained vs random

| experiment | env | algorithm | seeds | git_sha | trained_mean | random_mean | diff_ci95 | welch_p |
|---|---|---|---|---|---|---|---|---|
| 2 | CartPole-v1 | dqn | 5 | 0719247 | 425.916 | 22.578 | [291.22, 474.74] | 0.002 |
| 1 | FrozenLake-v1 | q_learning | 5 | 0719247 | 1.000 | 0.012 | [0.98, 1.00] | 0.000 |
