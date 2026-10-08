# Non-Functional Requirements & Evaluation Questions

## Non-Functional Requirements (Measurable NFRs)

| Category | Requirement | Measure | How Measured | Week Tested |
| :--- | :--- | :--- | :--- | :--- |
| **Reproducibility** | Same seed and configuration must produce identical episode returns | 100% bitwise/numerical match | `pytest tests/test_runner.py::test_same_seed_same_returns` | Week 4 |
| **Compute Budget** | Complete 600 CartPole-v1 DQN episodes on the weakest laptop CPU | < 60 minutes, CPU only | `python scripts/measure_performance.py` | Week 8 |
| **Memory Limit** | Peak RAM consumption during DQN training | ≤ 2.0 GB peak RAM | `psutil` peak memory logging script | Week 8 |
| **Offline Operation** | Full pipeline runs without an active internet connection | 100% functionality offline | Clean install test with network disabled (T-24) | Week 9 |
| **Zero Software Cost** | Total external software and API licensing cost | ₹0 software cost | `docs/feasibility.md` & `docs/licences.md` | Week 9 |
| **Transparency** | Every line of the learning algorithm can be explained by team members | Viva score ≥ 8/10 | Mock viva evaluation | Week 10 |
| **Data Integrity** | Every reported evaluation number is traceable to run folder and Git commit | 100% of reported results | `results/manifest.csv` hash verification | Week 8 |
| **Reliability** | Training resumes seamlessly after abrupt termination | Resumes from latest checkpoint | Integration test T-13 | Week 5 |

## Evaluation Questions (Week 6 Protocol)
1. Does the frozen trained policy achieve a statistically higher score than a random agent on unseen test seeds?
2. Does the agent score significantly higher than its own untrained state (checkpoint 0)?
3. Is performance improvement consistent across 5 independent training seeds (95% CI strictly positive)?
4. Does the learned policy retain its performance when loaded into a completely fresh Python process?
5. Does removing the replay buffer or the target network cause learning collapse or instability (ablation analysis)?

## Background & Literature Foundations
- **Experience Replay (Lin, 1992):** Replay buffers store consecutive experience tuples $(s, a, r, s', done)$. Uniform random sampling breaks temporal correlation and stabilizes training.
- **Deep Q-Networks (Mnih et al., 2015):** Combining neural network function approximation with experience replay and periodic target network updates prevents policy divergence.
- **Evaluation Standards (Henderson et al., 2018; Agarwal et al., 2021):** Reporting mean over multiple seeds with confidence intervals prevents cherry-picked reinforcement learning results.
