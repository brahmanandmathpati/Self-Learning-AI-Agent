# Multi-seed experiments: trained vs random

| experiment | env | algorithm | seeds | git_sha | trained_mean | random_mean | diff_ci95 | welch_p |
|---|---|---|---|---|---|---|---|---|
| 12 | Taxi-v4 | sarsa | 5 | bf3c273 | 5.902 | -768.860 | [771.23, 779.46] | 0.000 |
| 11 | Taxi-v4 | expected_sarsa | 5 | bf3c273 | 7.182 | -768.860 | [772.82, 780.73] | 0.000 |
| 9 | Taxi-v4 | q_learning | 5 | bf3c273 | 5.964 | -768.860 | [771.31, 779.52] | 0.000 |
| 8 | FrozenLake-v1 | expected_sarsa | 5 | bf3c273 | 1.000 | 0.012 | [0.98, 1.00] | 0.000 |
| 7 | FrozenLake-v1 | sarsa | 5 | bf3c273 | 1.000 | 0.012 | [0.98, 1.00] | 0.000 |
| 6 | CliffWalking-v1 | expected_sarsa | 5 | bf3c273 | -15.000 | -2021.874 | [1993.81, 2017.81] | 0.000 |
| 5 | CliffWalking-v1 | sarsa | 5 | bf3c273 | -17.000 | -2021.874 | [1991.81, 2015.81] | 0.000 |
| 4 | CliffWalking-v1 | q_learning | 5 | bf3c273 | -13.000 | -2021.874 | [1995.81, 2019.81] | 0.000 |
| 2 | CartPole-v1 | dqn | 5 | 0719247 | 425.916 | 22.578 | [291.22, 474.74] | 0.002 |
| 1 | FrozenLake-v1 | q_learning | 5 | 0719247 | 1.000 | 0.012 | [0.98, 1.00] | 0.000 |
