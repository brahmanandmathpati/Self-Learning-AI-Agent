# Q-learning by hand

Update rule:  `Q(s,a) ← Q(s,a) + α [ r + γ · max_a' Q(s',a') − Q(s,a) ]`; at a terminal step the target is just `r`.

## Worked example (checked by `tests/unit/test_q_learning.py::test_update_matches_hand_calculation`)

α = 0.5, γ = 0.9. Two states, two actions; Q starts at 0 except `Q(s'=1, a=1) = 1.0`.

| Step | s | a | r | s' | terminal | max Q(s',·) | target r + γ·max | Q(s,a) before | Q(s,a) after |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1 | no | 1.0 | 0 + 0.9 × 1.0 = 0.9 | 0 | 0 + 0.5 × (0.9 − 0) = **0.45** |

## Terminal step

If the episode terminates (goal or hole), there is no next state: target = r, even if Q(s',·) is large. With r = 1, α = 1.0, Q(s,a) = 0 and Q(s',·) = 5: Q ← 0 + 1.0 × (1 − 0) = 1.0, not 1 + 0.9 × 5 (`test_terminal_does_not_bootstrap`).

## Practice

1. α = 0.1, γ = 0.99, r = 0, max Q(s') = 0.5, Q(s,a) = 0.2 → Q becomes 0.2 + 0.1 × (0.495 − 0.2) = 0.2295.
2. Why does a truncated (time-limit) step still bootstrap while a terminal step does not?
