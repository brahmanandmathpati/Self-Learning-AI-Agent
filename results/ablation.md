# Ablation results

## Ablation #3 (git 8ef389b)

| variant | mean | std | count |
|---|---|---|---|
| full | 425.916 | 122.592 | 5 |
| no_replay | 86.794 | 56.199 | 5 |
| no_target | 9.364 | 0.022 | 5 |

| comparison | mean_full | mean_no_replay | diff | diff_ci_low | diff_ci_high | t | p_value | n_a | n_b | significant_0_05 | mean_no_target |
|---|---|---|---|---|---|---|---|---|---|---|---|
| full vs no_replay | 425.916 | 86.794 | 339.122 | 221.263 | 427.772 | 5.623 | 0.002 | 5 | 5 | True | nan |
| full vs no_target | 425.916 | nan | 416.552 | 304.276 | 488.080 | 7.598 | 0.002 | 5 | 5 | True | 9.364 |
