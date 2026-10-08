# Evaluation methodology

1. **Separate seeds.** Training resets use `seed×100000+episode`. Validation uses `10 000 000+i`; test uses `20 000 000+i`. The ranges never overlap (tested).
2. **Frozen policy.** `evaluate_agent()` plays a deep copy of the agent with `explore=False` (ε = 0) and never calls `update()`: no gradient steps, no replay pushes, no target syncs; even the training agent's RNG state is untouched (tested).
3. **Model selection on validation only.** The best checkpoint is chosen by validation score; the final number is that checkpoint on the test seeds.
4. **Before vs after.** The untrained agent is evaluated on the same test seeds before training (`kind = initial`).
5. **Baseline.** A random-action agent is evaluated on the same test seeds for every training seed.
6. **Metrics.** Mean, standard deviation, median, success rate (FrozenLake: goal reached; CartPole: return 500), mean episode length.
7. **Statistics over seeds** (`evaluation/stats.py`): Welch's t-test (unequal variances) and a bootstrap 95% CI for the difference of means (10 000 resamples, fixed seed). If both groups have zero variance the t-test is undefined: it is reported as p = 0 when the means differ and p = 1 when they are equal.
8. **Deterministic environments.** On the non-slippery FrozenLake map the start state and transitions are fixed, so
   every evaluation episode of a greedy policy is identical and its standard deviation is 0; seeds only matter on the
   slippery map. The variation that the statistics measure there comes from the 5 *training* seeds. On CartPole the
   seed sets the start state, so held-out test seeds matter for every policy.
9. **No invented numbers.** All tables and dashboard values are read from the database; missing data is shown as NOT RUN.
