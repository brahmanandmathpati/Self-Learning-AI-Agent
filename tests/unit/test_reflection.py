import pytest

from sla.evaluation.evaluate import EvalResult
from sla.reflection.fallback import template_note
from sla.reflection.grounding import check_grounding, extract_numbers
from sla.reflection.reflect import reflect
from sla.reflection.stats import compute_facts
from sla.training.runner import EpisodeInfo
from sla.utils.errors import LLMError, StoreError


@pytest.fixture
def filled(db):
    db.start_run("r", "FrozenLake-v1", "q_learning", 0, {})
    for ep in range(100):
        reward = 1.0 if ep >= 50 else 0.0
        db.log_episode("r", EpisodeInfo(ep, reward, 6, 0.1, None, "goal" if reward else "hole", 0.0))
    db.log_evaluation("r", "validation", EvalResult(1.0, 0.0, 1.0, 20, [1.0] * 20, 1.0, 6.0), episode=99)
    db.log_evaluation("r", "initial", EvalResult(0.0, 0.0, 0.0, 20, [0.0] * 20, 0.0, 8.0))
    db.log_evaluation("r", "test", EvalResult(1.0, 0.0, 1.0, 20, [1.0] * 20, 1.0, 6.0), episode=99)
    return db


def test_extract_numbers():
    assert extract_numbers("mean 23.5 over 1,000 episodes, change -2") == [23.5, 1000.0, -2.0]


def test_facts(filled):
    facts = compute_facts(filled, "r", window=50)
    assert facts["first_window_mean"] == 0.0 and facts["last_window_mean"] == 1.0
    assert facts["windows"][1]["episodes"] == "51-100" and facts["best_validation_after_episode"] == 100
    assert facts["untrained_test_mean"] == 0.0 and facts["test_mean"] == 1.0


def test_facts_missing_run(db):
    with pytest.raises(StoreError):
        compute_facts(db, "nope")


def test_template_note_is_grounded(filled):
    facts = compute_facts(filled, "r")
    assert check_grounding(template_note(facts), facts).passed


def test_planted_wrong_number_rejected(filled):
    facts = compute_facts(filled, "r")
    report = check_grounding("The agent reached a mean reward of 87.3 after training.", facts)
    assert not report.passed and report.unsupported == [87.3]


class FakeClient:
    def __init__(self, text=None, fail=False):
        self.text, self.fail = text, fail

    def generate(self, prompt):
        if self.fail:
            raise LLMError("offline")
        return self.text


def test_reflect_falls_back_when_llm_offline(filled):
    result = reflect(filled, "r", use_llm=True, client=FakeClient(fail=True))
    assert result.shown.source == "template" and result.shown.report.passed and result.rejected is None


def test_reflect_rejects_hallucinated_llm_note(filled):
    result = reflect(filled, "r", use_llm=True, client=FakeClient("Reward rose to 999 points."))
    assert result.rejected is not None and result.rejected.source == "llm"
    assert result.shown.source == "template"
    assert len(filled.query_reflections("r")) == 2


def test_reflect_accepts_grounded_llm_note(filled):
    result = reflect(filled, "r", use_llm=True, client=FakeClient("Mean reward went from 0.0 to 1.0."))
    assert result.shown.source == "llm" and result.rejected is None
