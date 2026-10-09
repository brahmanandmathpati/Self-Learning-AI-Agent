# Non-Functional Requirements — Self-Learning AI Agent
**Owner:** Vedant Biradar · **Task:** SLA-01-VB-1 · **Week:** 1  

Every NFR has a number, a way to measure it, the week it is tested, and the requirement (REQ ID) it is connected to.

---

## Measurable Non-Functional Requirements Table

| ID | Category | Requirement | Measure | How measured | Week | Related REQ |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **NFR-01** | Reproducibility | Same seed and same config give identical episode returns | 100% identical | `test_runner.py::test_same_seed_same_returns` | 4 | REQ-01 |
| **NFR-02** | Compute | 600 CartPole DQN episodes on the weakest laptop | < 60 min, CPU only | `scripts/measure_performance.py` | 8 | REQ-08 |
| **NFR-03** | Memory | Peak RAM during DQN training | < 2 GB | `scripts/measure_performance.py` | 8 | REQ-08 |
| **NFR-04** | Offline | Train, evaluate, UI and template note work with internet off | All work | T-24 (clean install test) | 9 | REQ-21 |
| **NFR-05** | Cost | Software cost | ₹0 | `docs/licences.md` | 9 | REQ-21 |
| **NFR-06** | Transparency | Every algorithm line can be explained by its owner | Mock viva ≥ 8/10 | Week-10 mock viva | 10 | REQ-05, REQ-08 |
| **NFR-07** | Honesty | Every reported number is traceable to a run folder and git commit | 100% of table rows | `results/manifest.csv` | 8 | REQ-13 |
| **NFR-08** | Reliability | Training resumes after a forced stop | Resumes at the next episode | T-13 | 5 | REQ-11 |
| **NFR-09** | Data durability | Stored runs and episodes survive a restart | 0 rows lost | T-10, T-11 | 5 | REQ-10 |
| **NFR-10** | Usability | A new user can start a training run from the UI without help | ≤ 3 clicks and ≤ 2 minutes | Demo test with a teammate | 9 | REQ-17 |

---

## Evaluation Questions (Vedant owns the answers in Week 6)
1. Does the frozen trained policy score higher than the random agent on unseen test seeds?
2. Does it score higher than its own untrained version (checkpoint 0)?
3. Is the improvement consistent across 5 training seeds (does the confidence interval exclude 0)?
4. Does the improvement survive saving, closing the program and reloading?
5. Does removing the replay buffer or the target network change the result (ablation)?

---

## Background: Experience Replay & DQN Foundations
*Notes from Lin (1992) and Mnih et al. (2015):*

- **Experience Replay Origin:** Lin (1992) introduced experience replay: the agent stores past experiences $(s, a, r, s')$ and trains on them repeatedly, instead of discarding each transition after one update.
- **Data Efficiency:** Replaying past experiences makes learning significantly more data-efficient, because one environmental step can contribute to multiple gradient updates.
- **Deep Q-Networks (DQN):** Mnih et al. (2015) successfully combined deep neural networks with experience replay to master Atari games directly from raw visual observations.
- **Breaking Correlation:** Sampling uniform random mini-batches from the replay buffer breaks the strong temporal autocorrelation of consecutive states, stabilizing neural network convergence.
- **Target Network & Ablation:** The DQN utilizes a separate, periodically updated target network so that target value estimates remain stationary during gradient descent. The ablation study (REQ-20) rigorously tests the impact of isolating or removing replay memory and target networks.