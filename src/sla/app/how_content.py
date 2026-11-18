"""Text and file lists for the "How it works" page (pure data, no Streamlit).

Keeping every sentence here makes the page easy to proofread and edit. ``TEXT["mr"]`` holds one Roman-Marathi helper
line per section (technical words stay in English); the page shows it only when the visitor switches it on.
"""

from __future__ import annotations

import re
from pathlib import Path

SRC_SLA = Path(__file__).resolve().parents[1]
REPO_ROOT = SRC_SLA.parents[1]

# Sections in the order they appear on the page.
SECTIONS = ("big_picture", "one_step", "watch", "explore", "dqn", "prove", "data", "start_training", "ablation",
            "beyond", "limits", "glossary", "try_it")

TEXT: dict[str, dict[str, str]] = {
    "en": {
        "big_picture": "From a config file to a verified result, in one line.",
        "one_step": "Observe, choose, act, learn: one step, with the real arithmetic.",
        "watch": "Run the same Q-learning algorithm in your browser and watch the table fill with numbers.",
        "explore": "Why the agent starts by trying random moves, and when it stops.",
        "dqn": "When there are too many states for a table, a small neural network takes its place.",
        "prove": "Training scores are not proof. This is how the project shows that learning really happened.",
        "data": "Everything the website shows is read from these tables.",
        "start_training": "What happens, file by file, when you press Start training.",
        "ablation": "Take one trick away at a time and measure the damage.",
        "beyond": "Two more layers built on top of the same learner.",
        "limits": "Quoted from Section 28 of the project documentation.",
        "glossary": "Short answers for the words you will hear in the review.",
        "try_it": "Run everything yourself on your own computer.",
    },
    "mr": {
        "big_picture": "Config file pasun training suru hote, runner agent la shikavto, result database madhe jato "
                       "ani website fakt te vachte.",
        "one_step": "Agent observe karto, move choose karto, reward milavto ani ek Q number thoda badalto.",
        "watch": "Suruvatila Q-table madhe sagle 0 aste; episodes vadhle ki goal javalche numbers vadhtat ani "
                 "arrows changlya rastyakade point kartat.",
        "explore": "Epsilon mhanje random move cha chance; suruvatila 1.0, nantar kami, ani test madhe 0.",
        "dqn": "Jithe table shakya nahi tithe neural network vaparto; replay memory ani target network learning "
               "steady thevtat.",
        "prove": "Agent la learning band karun navya seeds var test karto, mag statistics ne siddha karto ki he "
                 "luck nahi.",
        "data": "Sagla data SQLite database madhe aahe; website to fakt vachte, kadhich badlat nahi.",
        "start_training": "Start training dabavla ki config banto, runner game khelto, best checkpoint save hoto "
                          "ani shevti held-out test hote.",
        "ablation": "Ek ek trick kadhun pahila ani score kiti kami zala te dakhavle.",
        "beyond": "Reflection layer numbers database shi tapaste; Vision Lab madhe agent hat chya gestures pasun "
                  "shikto.",
        "limits": "Aamhi kharech sangto: chote games, kami seeds, ani Vision Lab accuracy ajun mojli nahi.",
        "glossary": "Review madhe yenare shabd sope bhashet.",
        "try_it": "Ya commands ne tumhi swatah training ani website chalvu shakta.",
    },
}

# Files shown as chips under each section. Paths are relative to src/sla/, or to the repository root
# (configs/..., docs/...). A unit test checks that every one of them exists.
FILE_CHIPS: dict[str, tuple[str, ...]] = {
    "big_picture": ("cli.py", "services/training_service.py", "training/pipeline.py", "training/runner.py",
                    "agents/q_learning.py", "agents/dqn.py", "envs/factory.py", "checkpoints/manager.py",
                    "database/store.py", "evaluation/evaluate.py", "evaluation/stats.py", "app/main.py"),
    "one_step": ("agents/q_learning.py", "training/runner.py", "explain.py"),
    "watch": ("agents/q_learning.py", "agents/schedules.py", "envs/factory.py", "explain.py",
              "configs/frozenlake_qlearning.yaml"),
    "explore": ("agents/schedules.py", "configs/frozenlake_qlearning.yaml"),
    "dqn": ("agents/dqn.py", "agents/networks.py", "memory/replay_buffer.py", "configs/cartpole_dqn.yaml"),
    "prove": ("evaluation/evaluate.py", "evaluation/stats.py", "utils/seeding.py", "app/views/evaluation.py"),
    "data": ("database/store.py", "app/data.py"),
    "start_training": ("training/config.py", "services/training_service.py", "training/pipeline.py",
                       "training/runner.py", "agents/", "checkpoints/manager.py", "database/store.py",
                       "evaluation/evaluate.py", "training/safety.py", "training/guards.py"),
    "ablation": ("evaluation/ablation.py", "configs/ablation_no_replay.yaml", "configs/ablation_no_target.yaml"),
    "beyond": ("reflection/grounding.py", "vision/hands.py", "vision/features.py", "vision/learners.py"),
    "limits": ("docs/PROJECT_DOCUMENTATION.md",),
    "glossary": ("explain.py", "app/how_content.py"),
    "try_it": ("cli.py", "app/main.py"),
}


def resolve(path: str) -> Path:
    """Where a chip's path lives on disk (under src/sla/ first, then the repository root)."""
    inside = SRC_SLA / path
    return inside if inside.exists() else REPO_ROOT / path



# --------------------------------------------------------------------------- the 8 steps of "Start training"


START_TRAINING_STEPS = (
    ("The form becomes a config", "Your choices (game, algorithm, seed, episodes) are turned into a checked "
                                  "run configuration.", "training/config.py"),
    ("A service starts the run", "The training service creates the run and tells the pipeline what to do.",
     "services/training_service.py"),
    ("The pipeline picks the mode", "Single run, multi-seed experiment, baseline or ablation.",
     "training/pipeline.py"),
    ("The runner plays episodes", "It resets the game, asks the agent for a move, and steps the game.",
     "training/runner.py"),
    ("The agent learns after every step", "Q-learning updates one table number; the DQN trains its network.",
     "agents/"),
    ("Validation and checkpoints", "Every few episodes the agent plays held-out validation games and the best "
                                   "checkpoint is saved.", "checkpoints/manager.py"),
    ("Every episode is stored", "Reward, length, epsilon and loss go into the SQLite database.",
     "database/store.py"),
    ("Final test on unseen seeds", "The best checkpoint is tested with learning switched off; the Evaluation "
                                   "page then updates.", "evaluation/evaluate.py"),
)

SAFETY_TEXT = ("Safety stops: training/safety.py ends runaway runs (too many steps, too much time, broken numbers) "
               "and training/guards.py stops training if Q-values or the loss explode.")

# --------------------------------------------------------------------------- the SQLite tables

TABLE_NOTES = (
    ("experiments", "One row per experiment: single run, multi-seed experiment, baseline or ablation."),
    ("runs", "One row per training run: seed, configuration, git commit, status and best checkpoint."),
    ("episodes", "Every training episode: reward, length, epsilon and loss."),
    ("metrics", "Extra named numbers logged while a run is going."),
    ("evaluations", "Frozen-policy tests: initial (untrained), validation and final test results."),
    ("ablation_results", "Per-seed test scores of the full DQN and the two ablated variants."),
    ("reflections", "Plain-language notes and whether their number check passed."),
)

# --------------------------------------------------------------------------- glossary

GLOSSARY = (
    ("Agent", "The learner: our program, which picks moves and changes its own numbers."),
    ("Environment", "The game the agent plays, for example FrozenLake or CartPole."),
    ("State", "What the agent sees right now, such as 'I am on square 5'."),
    ("Action", "A move the agent can make, such as left, right, up or down."),
    ("Reward", "The points the game gives after a move; they are the only teacher."),
    ("Episode", "One whole game, from the start to the end."),
    ("Seed", "A number that fixes the randomness, so anyone can repeat the same game exactly."),
    ("Epsilon", "The chance of making a random move to explore; it falls during training and is 0 when we test."),
    ("Q-table", "A table with one number per (state, action): how good that move looks from that state."),
    ("Replay memory", "A store of old moves; the DQN learns from random samples of it so learning stays steady."),
    ("Target network", "A frozen copy of the network, refreshed now and then, that gives steady learning targets."),
    ("p-value", "The chance of seeing a gap this big if nothing had really been learned; below 0.05 is called "
                "significant."),
)

# --------------------------------------------------------------------------- limits (quoted from the docs)

LIMITS_FALLBACK = (
    "Four small benchmark games. This is bounded, single-task learning — not general intelligence.",
    "Five seeds give wide confidence intervals; the CartPole DQN is sensitive to hyper-parameters, and results can "
    "vary across hardware.",
    "Vision Lab accuracy on real users is **not measured yet**.",
)


def limits_from_docs(path: Path | None = None) -> list[str]:
    """The bullets under 'Limitations (honest)' in Section 28 of the project documentation (quoted, not rewritten)."""
    doc = path or REPO_ROOT / "docs" / "PROJECT_DOCUMENTATION.md"
    try:
        text = doc.read_text(encoding="utf-8")
    except OSError:
        return list(LIMITS_FALLBACK)
    m = re.search(r"\*\*Limitations \(honest\):\*\*\s*\n(.*?)\n\*\*Future work", text, flags=re.S)
    if not m:
        return list(LIMITS_FALLBACK)
    bullets: list[str] = []
    for line in m.group(1).splitlines():
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif line.strip() and bullets:
            bullets[-1] += " " + line.strip()
    return bullets or list(LIMITS_FALLBACK)
