from sla.friendly import (
    before_after_sentence,
    best_score_event,
    epsilon_in_words,
    phase_change_event,
    phase_for,
    verdict_why,
    winner_sentence,
)


def test_epsilon_in_words():
    assert epsilon_in_words(0.3) == "30% random moves, 70% best-known moves"
    assert epsilon_in_words(1.0).startswith("100% random")
    assert epsilon_in_words(0.0).startswith("0% random")
    assert epsilon_in_words(None) == "not available"
    assert epsilon_in_words(7) .startswith("100%") and epsilon_in_words(-1).startswith("0%")


def test_phase_follows_epsilon_decay():
    assert phase_for(1.0, 1.0, 0.05)[0] == "exploring"
    assert phase_for(0.5, 1.0, 0.05)[0] == "learning"
    assert phase_for(0.05, 1.0, 0.05)[0] == "exploiting"
    assert phase_for(0.1, 0.1, 0.1)[0] == "exploiting"  # fixed exploration rate (CliffWalking)
    assert phase_for(0.8, 0.8, 0.8)[0] == "exploring"


def test_phase_and_best_events():
    assert phase_change_event(None, "learning", 5) is None
    assert phase_change_event("learning", "learning", 5) is None
    assert "learning" in phase_change_event("exploring", "learning", 1200)
    assert best_score_event(1, 3.0, None) == (None, 3.0)
    line, best = best_score_event(7, 5.0, 3.0)
    assert best == 5.0 and "Episode 7" in line and "5" in line
    assert best_score_event(8, 4.0, 5.0) == (None, 5.0)


def test_winner_sentence():
    s = winner_sentence("CartPole-v1", [("DQN", 400.0), ("Random", 20.0)])
    assert "DQN scores best" in s and "20.0 times" in s
    tie = winner_sentence("FrozenLake-v1", [("Q-learning", 1.0), ("SARSA", 1.0), ("Random", 0.01)])
    assert "tie for first" in tie and "Q-learning and SARSA" in tie
    assert winner_sentence("X", [("A", 2.0)]).endswith("2.00.")
    assert "compared with" in winner_sentence("X", [("A", 2.0), ("Random", 0.0)])
    assert winner_sentence("X", []) is None
    assert winner_sentence("X", [("A", float("nan"))]) is None


def test_before_after_and_verdict_lines():
    assert "improved" in before_after_sentence(10.0, 20.0)
    assert "got worse" in before_after_sentence(10.0, 5.0)
    assert before_after_sentence(None, 1.0).startswith("Not available")
    lines = verdict_why(0.0018, 291.2, 474.7)
    assert "1.8 times in 1,000" in lines[0] and "[291.20, 474.70]" in lines[1]
    assert verdict_why(None, None, None)[0].startswith("Not available")


def test_guide_content_covers_every_page_title_in_three_parts():
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[2] / "src" / "sla" / "app" / "guide_content.py"
    if not src.exists():
        return
    ns: dict = {}
    exec(compile(src.read_text(encoding="utf-8"), str(src), "exec"), ns)  # noqa: S102 - pure data module
    guide = ns["GUIDE"]
    assert {"Training", "Agent comparison", "Evaluation", "Overview"} <= set(guide)
    assert all(len(v) == 3 and all(x.strip() for x in v) for v in guide.values())
