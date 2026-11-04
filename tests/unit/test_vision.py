"""Vision Lab maths: landmark features, online learners, honest evaluation, video sampling, human-feedback RL."""

import numpy as np
import pytest

from sla.vision.features import N_FEATURES, normalise
from sla.vision.learners import KNNLearner, bootstrap_ci, evaluate, load_learner, stratified_split
from sla.vision.video import sample_times


def _hand(seed=0):
    return np.random.default_rng(seed).uniform(0.2, 0.8, size=(21, 3))


def test_features_ignore_position_and_size():
    h = _hand()
    moved = h.copy()
    moved[:, :2] = moved[:, :2] * 0.5 + 0.3  # same hand, smaller and somewhere else in the picture
    a, b = normalise(h), normalise(moved)
    assert a.shape == (N_FEATURES,)
    assert np.allclose(a, b, atol=1e-5)
    assert np.allclose(a[:2], 0)  # the wrist is the origin


def test_left_hand_is_mirrored_to_match_right():
    h = _hand()
    mirrored = h.copy()
    mirrored[:, 0] = 1 - mirrored[:, 0]
    assert np.allclose(normalise(h, "Right"), normalise(mirrored, "Left"), atol=1e-5)


def test_bad_landmarks_are_rejected():
    with pytest.raises(ValueError):
        normalise(np.zeros((5, 2)))
    with pytest.raises(ValueError):
        normalise(np.zeros((21, 2)))


def _toy(n=20, classes=("A", "B", "C"), noise=0.01, seed=0):
    rng = np.random.default_rng(seed)
    base = {c: rng.uniform(0.2, 0.8, size=(21, 2)) for c in classes}
    X = np.array([normalise(base[c] + rng.normal(0, noise, (21, 2))) for c in classes for _ in range(n)])
    y = [c for c in classes for _ in range(n)]
    return X, y


def test_knn_learns_online():
    X, y = _toy()
    k = KNNLearner()
    assert k.predict(X[0]) is None  # knows nothing yet
    for x, label in zip(X, y):
        k.add(x, label)
    assert k.predict(X[0]) == "A" and k.predict(X[-1]) == "C"
    assert abs(sum(k.predict_proba(X[0]).values()) - 1) < 1e-6
    assert load_learner(k.to_dict()).predict(X[30]) == y[30]


def test_split_is_stratified_and_disjoint():
    _, y = _toy(n=10)
    tr, te = stratified_split(y)
    assert set(tr).isdisjoint(te) and len(tr) + len(te) == len(y)
    assert {y[i] for i in te} == {"A", "B", "C"}


@pytest.mark.parametrize("kind", ["knn", "mlp"])
def test_evaluate_on_held_out_beats_chance(kind):
    X, y = _toy()
    ev = evaluate(X, y, kind=kind)
    assert ev.n_test == 12 and ev.n_train == 48
    assert ev.accuracy > ev.chance + 0.3
    assert ev.ci95[0] <= ev.accuracy <= ev.ci95[1]
    assert sum(map(sum, ev.confusion)) == ev.n_test
    assert ev.curve and ev.curve[-1][0] == ev.n_train


def test_random_labels_score_near_chance():
    X, _ = _toy(n=30)
    y = list(np.random.default_rng(1).choice(["A", "B", "C"], size=len(X)))
    ev = evaluate(X, y)
    assert ev.accuracy < 0.7  # no real pattern → no fake high score


def test_evaluate_needs_enough_samples():
    X, y = _toy(n=1)
    with pytest.raises(ValueError):
        evaluate(X, y)


def test_bootstrap_ci_bounds():
    lo, hi = bootstrap_ci(np.array([1, 1, 1, 0]))
    assert 0 <= lo <= 0.75 <= hi <= 1


def test_video_sample_times():
    assert sample_times(2.0, fps=5) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    assert len(sample_times(120, fps=5)) == 150  # capped at 30 seconds
    assert sample_times(0) == []


def test_video_frames_from_a_real_file(tmp_path):
    cv2 = pytest.importorskip("cv2")
    from sla.vision.video import frames
    path = tmp_path / "clip.avi"
    out = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), 10, (64, 48))
    for i in range(20):  # 2 seconds at 10 fps
        out.write(np.full((48, 64, 3), i * 10, np.uint8))
    out.release()
    got = list(frames(path, fps=5))
    assert len(got) == 10 and got[0][1].shape == (48, 64, 3)


def test_human_feedback_agent_learns_from_rewards(tmp_path):
    from sla.database.store import Database
    from sla.vision.human_rl import HumanFeedbackAgent
    agent = HumanFeedbackAgent(epsilon=0.0)
    s, a = agent.state, agent.proposal
    agent.feedback(-1.0)
    assert agent.q[s, a] < 0  # a 👎 makes that move less attractive
    agent.reset_episode()
    s, a = agent.state, agent.proposal
    agent.feedback(1.0)
    assert agent.q[s, a] > 0
    agent.reset_episode()
    db = Database(tmp_path / "hf.db")
    run_id = agent.save(db)
    run = db.get_run(run_id)
    assert run["variant"] == "human_feedback" and run["status"] == "completed"
    assert len(db.query_episodes(run_id)) == len(agent.history) == 2
