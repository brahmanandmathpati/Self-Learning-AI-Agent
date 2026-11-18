"""The pure helpers and the content behind the website's 'How it works' page."""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pytest

from sla.agents.q_learning import q_learning_update
from sla.app import how_content as hc
from sla.explain import (
    LAKE_MAP,
    describe_update,
    dqn_parameter_count,
    epsilon_at,
    epsilon_curve,
    greedy_walk,
    lake_step,
    moving_average,
    policy_arrows,
    practice_questions,
    q_update,
    random_success_rate,
    run_lake_demo,
)

FL = dict(alpha=0.1, gamma=0.99, eps_start=1.0, eps_end=0.05, eps_steps=10_000)


# ----------------------------------------------------------------------------- the Q-update calculator
def test_q_update_goal_example_is_point_one():
    u = q_update(0.0, 1.0, 0.0, True, 0.1, 0.99)
    assert u.target == 1.0 and u.td_error == pytest.approx(1.0) and u.new_q == pytest.approx(0.1)


def test_q_update_matches_the_agent_function():
    u = q_update(0.5, 0.0, 0.8, False, 0.1, 0.99)
    q = np.array([[0.5], [0.8]])
    q_learning_update(q, 0, 0, 0.0, 1, False, 0.1, 0.99)
    assert u.new_q == pytest.approx(float(q[0, 0])) == pytest.approx(0.5292)


def test_describe_update_shows_three_lines_of_arithmetic():
    lines = describe_update(q_update(0.0, 1.0, 0.0, True, 0.1, 0.99))
    assert len(lines) == 3 and lines[0].startswith("target") and "= 0.1" in lines[2]
    assert "best next Q" in describe_update(q_update(0.5, 0.0, 0.8, False, 0.1, 0.99))[0]


# ----------------------------------------------------------------------------- epsilon
def test_epsilon_curve_uses_the_real_schedule():
    steps, values = epsilon_curve(1.0, 0.05, 10_000)
    assert steps[0] == 0 and values[0] == 1.0
    assert min(values) == pytest.approx(0.05) and values[-1] == pytest.approx(0.05)
    assert all(a >= b for a, b in zip(values, values[1:]))
    assert epsilon_at(1.0, 0.05, 10_000, 2_000) == pytest.approx(0.81)


# ----------------------------------------------------------------------------- the FrozenLake demo
def test_lake_rules():
    assert lake_step(0, 2) == (1, 0.0, False)           # right from the start
    assert lake_step(14, 2) == (15, 1.0, True)           # the goal
    assert lake_step(4, 1)[2] is False and lake_step(5, 0)[2] is False
    assert lake_step(0, 0)[0] == 0                       # walls keep you in place
    assert LAKE_MAP[1][1] == "H"


def test_lake_demo_is_deterministic():
    a, b = run_lake_demo(150, seed=0, **FL), run_lake_demo(150, seed=0, **FL)
    assert np.array_equal(a.q_by_episode, b.q_by_episode) and np.array_equal(a.success, b.success)
    assert not np.array_equal(a.q_by_episode, run_lake_demo(150, seed=1, **FL).q_by_episode)


def test_lake_demo_learns_and_is_fast():
    t0 = time.perf_counter()
    demo = run_lake_demo(2000, seed=0, **FL)
    assert time.perf_counter() - t0 < 2.0
    assert demo.q_by_episode.shape == (2001, 16, 4) and not demo.q_by_episode[0].any()
    reached, path = greedy_walk(demo.q_by_episode[-1])
    assert reached and path[0] == 0 and path[-1] == 15
    assert moving_average(demo.success)[-1] > moving_average(demo.success)[:100].mean()


def test_before_training_is_random_and_after_is_not():
    assert not greedy_walk(np.zeros((16, 4)))[0]
    assert 0.0 <= random_success_rate(games=300, seed=0) < 0.1
    assert policy_arrows(np.zeros((16, 4))) == ["·"] * 16


def test_moving_average_is_trailing():
    out = moving_average(np.array([1.0, 1.0, 0.0, 0.0]), window=2)
    assert out.tolist() == [1.0, 1.0, 0.5, 0.0] and len(moving_average(np.zeros(0))) == 0


def test_dqn_parameter_count():
    assert dqn_parameter_count(128) == 17_410


# ----------------------------------------------------------------------------- practice questions
def test_practice_answers_are_computed():
    qs = practice_questions(0.1, 0.99, 1.0, 0.05, 10_000, 500, 20_000_000)
    assert len(qs) == 6
    answers = "\n".join(a for _, a in qs)
    for needle in ("0.28", "0.5292", "0.81", "**4**", "20,000,007", "**64**"):
        assert needle in answers


# ----------------------------------------------------------------------------- page content
def test_every_chip_path_exists():
    for key, paths in hc.FILE_CHIPS.items():
        for path in paths:
            assert hc.resolve(path).exists(), f"{key}: {path} does not exist"


def test_start_training_step_files_exist():
    assert len(hc.START_TRAINING_STEPS) == 8
    for _title, _desc, path in hc.START_TRAINING_STEPS:
        assert hc.resolve(path).exists(), path


def test_every_section_has_chips_and_both_languages():
    assert set(hc.FILE_CHIPS) == set(hc.SECTIONS) == set(hc.TEXT["en"]) == set(hc.TEXT["mr"])
    for key in hc.SECTIONS:
        assert hc.TEXT["mr"][key].strip() and hc.TEXT["mr"][key] != hc.TEXT["en"][key]


def test_glossary_has_the_twelve_terms():
    terms = [t for t, _ in hc.GLOSSARY]
    assert len(terms) == len(set(terms)) == 12 and "Replay memory" in terms and "p-value" in terms


def test_table_notes_cover_the_seven_tables():
    assert [t for t, _ in hc.TABLE_NOTES] == ["experiments", "runs", "episodes", "metrics", "evaluations",
                                              "ablation_results", "reflections"]


def test_limits_are_quoted_from_the_documentation(tmp_path: Path):
    doc = tmp_path / "d.md"
    doc.write_text("## 28\n\n**Limitations (honest):**\n\n- First point\n- Second point\n  continues here\n\n"
                   "**Future work:** x\n", encoding="utf-8")
    assert hc.limits_from_docs(doc) == ["First point", "Second point continues here"]
    assert hc.limits_from_docs(tmp_path / "missing.md") == list(hc.LIMITS_FALLBACK)
    real = hc.REPO_ROOT / "docs" / "PROJECT_DOCUMENTATION.md"
    if real.exists():
        bullets = hc.limits_from_docs()
        assert bullets and any("Vision Lab" in b for b in bullets)
        text = real.read_text(encoding="utf-8")
        assert all(b[:25] in text for b in bullets)


def test_the_page_does_not_hard_code_result_numbers():
    view = hc.SRC_SLA / "app" / "views" / "how_it_works.py"
    source = view.read_text(encoding="utf-8") + (hc.SRC_SLA / "app" / "how_content.py").read_text(encoding="utf-8")
    for number in ("425.92", "22.58", "0.0018", "403.34", "86.79", "9.36", "291.22", "474.74"):
        assert number not in source, number
