"""Vision Lab: teach the agent hand gestures live (webcam), from photos and videos; gestures can reward the RL agent.

Everything shown is measured on the samples the visitor actually gave: accuracy is always on a held-out 20% split,
compared with chance, with a bootstrap 95% interval. Only hand-landmark numbers are kept.
"""

from __future__ import annotations

import hashlib
import html
import json
import tempfile
import time
from pathlib import Path

import numpy as np
import streamlit as st

from sla.app import auth, routes
from sla.app import vision_live as vl
from sla.app.charts.figures import accuracy_curve, confusion_heatmap, prediction_timeline, reward_bars
from sla.app.components.chart_card import chart_card
from sla.app.components.metric_card import card_grid, metric_card
from sla.app.components.section_header import hero, section
from sla.app.components.states import empty_state, error_state
from sla.app.state import services
from sla.vision.learners import evaluate, load_learner

PRIVACY = ("Your camera is used only while this page is open. Frames are processed in memory on this server to find "
           "21 hand points; only those numbers are kept (never your face or the picture), unless you tick “save "
           "images”. Nothing is sent to any outside service. “Delete my data” removes everything.")


def render() -> None:
    hero("Vision Lab", "Teach the agent hand gestures live — from your webcam, photos or videos. It learns from 21 "
         "hand points, never raw pixels, and every score is measured on samples it has not seen.",
         eyebrow="Live learning · vision")
    if not vl.available():
        empty_state("The Vision Lab needs two extra packages on this server.", 'pip install -e ".[vision]"',
                    "Install MediaPipe and OpenCV, then reload this page.", glyph="eye")
        return
    live = vl.state()
    _privacy(live)
    t1, t2, t3, t4 = st.tabs(["① Teach with gestures", "② Photos & videos", "③ Gestures teach the agent",
                              "④ Results & model card"])
    with t1:
        _teach(live)
    with t2:
        _uploads(live)
    with t3:
        _human_rl(live)
    with t4:
        _results(live)


# ---------------------------------------------------------------------------------------------- privacy & classes
def _privacy(live: vl.LiveState) -> None:
    with st.container(key="card_privacy"):
        a, b = st.columns([3, 1], vertical_alignment="center")
        a.markdown(f'<div class="sla-share"><b>Privacy first</b><span>{html.escape(PRIVACY)}</span></div>',
                   unsafe_allow_html=True)
        if b.button("Delete my data", key="vl_delete", icon=":material/delete:", width="stretch"):
            live.clear()
            user = auth.current_user()
            removed = services().db.delete_vision_models(user["email"]) if auth.can_act() and user["email"] else 0
            st.toast(f"Deleted all samples on this page{f' and {removed} saved model(s)' if removed else ''}.")
        live.save_images = a.checkbox("Save images of my samples (off by default; kept on this server only)",
                                      value=live.save_images, key="vl_save_images")


def _consented() -> bool:
    return st.checkbox("I agree to turn on my camera for this page. I understand only hand-point numbers are kept.",
                       key="vl_consent")


def _class_editor(live: vl.LiveState) -> None:
    with st.expander("Gesture classes", expanded=False):
        text = st.text_area("One class per line (2–8 classes)", "\n".join(live.classes), key="vl_classes_text",
                            height=130)
        names = [n.strip() for n in text.splitlines() if n.strip()][:8]
        if len(names) >= 2 and names != live.classes:
            live.classes = list(dict.fromkeys(names))
            st.caption("Classes updated.")


def _counts_html(live: vl.LiveState) -> str:
    counts = live.counts()
    chips = "".join(
        f'<div class="sla-chip"><span class="ck">{html.escape(c)}</span><span class="cv">{n} '
        f'<small>{"✓" if n >= vl.MIN_PER_CLASS else f"/ {vl.MIN_PER_CLASS}"}</small></span></div>'
        for c, n in counts.items())
    return f'<div class="sla-chips">{chips}</div>'


def _prediction_html(pred) -> str:
    if pred is None or not pred.hand:
        return '<div class="sla-pred empty">Show your hand to the camera…</div>'
    if not pred.label:
        return '<div class="sla-pred empty">Hand found ✓ — record some samples so the agent can learn.</div>'
    rows = "".join(f'<div class="row"><span>{html.escape(c)}</span><div class="bar"><i style="width:{p * 100:.0f}%">'
                   f'</i></div><b>{p:.0%}</b></div>' for c, p in list(pred.proba.items())[:3])
    return f'<div class="sla-pred"><div class="top">{html.escape(pred.label)}</div>{rows}</div>'


# ---------------------------------------------------------------------------------------------- tab 1: live webcam
def _teach(live: vl.LiveState) -> None:
    section("Teach with gestures", "Pick a class, press Record and hold the gesture. Add 10+ samples for each class "
            "— move your hand around a little so it learns the shape, not one position.", kicker="Live")
    _class_editor(live)
    if not _consented():
        empty_state("The camera is off.", next_step="Tick the consent box above to start.", glyph="eye",
                    tag="CAMERA OFF")
        return
    if not _load_detector(live):
        return
    modes = (["Live video", "Snapshots"] if vl.webrtc_available() else ["Snapshots"])
    mode = st.segmented_control("Camera mode", modes, default=modes[0], key="vl_mode")
    rec_class = st.selectbox("Class to record", live.classes, key="vl_rec_class")
    left, right = st.columns([1.4, 1], gap="large")
    with left:
        if mode == "Live video":
            from streamlit_webrtc import WebRtcMode, webrtc_streamer
            recording = st.toggle(f"Record samples of “{rec_class}”", key="vl_recording")
            live.recording = rec_class if recording else None
            webrtc_streamer(key="vl_cam", mode=WebRtcMode.SENDRECV, video_frame_callback=vl.frame_callback(live),
                            media_stream_constraints={"video": {"width": {"ideal": 640}, "facingMode": "user"},
                                                      "audio": False},
                            rtc_configuration={"iceServers": vl.ice_servers()}, async_processing=True)
            st.caption("Live video: the hand skeleton and the prediction are drawn on each frame. If the video does "
                       "not connect (some networks block it), switch to Snapshots.")
        else:
            live.recording = None
            shot = st.camera_input("Take a photo of your gesture", key="vl_snap")
            if shot is not None:
                rgb = _decode(shot.getvalue())
                out, pred = live.process(rgb, "snapshot", record=False)
                st.image(out, caption="Detected hand points", width="stretch")
                if not pred.hand:
                    st.warning("No hand found. Try more light and keep the whole hand in the picture.")
                elif st.button(f"Add as a sample of “{rec_class}”", key="vl_add_snap", type="primary"):
                    _add_snapshot(live, rgb, rec_class)
    with right:
        _live_panel(live)
    _train_controls(live)


def _load_detector(live: vl.LiveState) -> bool:
    """Start the MediaPipe hand model; on failure show a clear card (not the generic database error)."""
    try:
        live.det = vl.detector()
        return True
    except (OSError, ImportError, RuntimeError) as exc:
        error_state("The hand-tracking model could not start on this server.",
                    "a system library that MediaPipe needs is missing (for example libEGL / libGLES on Linux).",
                    "the app owner should check packages.txt (libegl1, libgles2) and reboot the app. "
                    "Charts, results and the other pages still work.", exc)
        return False


def _decode(data: bytes) -> np.ndarray:
    import cv2
    bgr = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("could not read the image")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def _add_snapshot(live: vl.LiveState, rgb: np.ndarray, label: str) -> None:
    from sla.vision.features import normalise
    hands = live.det.detect(rgb)
    if not hands:
        st.warning("No hand found in this photo.")
        return
    live.add(normalise(hands[0].landmarks, hands[0].handedness), label, "snapshot")
    if live.save_images:
        live._save_image(rgb, label)
    st.toast(f"Added a sample of {label}.")


@st.fragment(run_every=1.0)
def _live_panel(live: vl.LiveState) -> None:
    st.markdown('<p class="sla-chart-title">Live prediction</p>', unsafe_allow_html=True)
    st.markdown(_prediction_html(live.last), unsafe_allow_html=True)
    fps, ms = live.fps(), live.mean_ms()
    st.caption(f"{fps:.0f} FPS · {ms:.0f} ms per frame" if ms else "Waiting for camera frames…")
    st.markdown('<p class="sla-chart-title" style="margin-top:.8rem">Samples per class</p>', unsafe_allow_html=True)
    st.markdown(_counts_html(live), unsafe_allow_html=True)


def _train_controls(live: vl.LiveState) -> None:
    section("Learner", "k-NN learns instantly from every sample. The neural network learns a smoother rule when you "
            "press Train.", kicker="Learning")
    a, b = st.columns([2, 1], vertical_alignment="center")
    choice = a.radio("Predict with", ["k-NN (online)", "Neural network"], horizontal=True, key="vl_learner")
    live.use_mlp = choice == "Neural network"
    if b.button("Train neural network", key="vl_train", type="primary", width="stretch", disabled=not live.ready()):
        with st.spinner("Training the 42 → 64 → classes network…"):
            live.train_mlp()
        st.toast("Neural network trained on all current samples.")
    if live.use_mlp and live.mlp is None:
        st.caption("The neural network is not trained on the current samples yet — k-NN is used until you train it.")
    if not live.ready():
        st.caption(f"Add at least {vl.MIN_PER_CLASS} samples for two or more classes to train and measure accuracy.")


# ---------------------------------------------------------------------------------------------- tab 2: uploads
def _guess_label(name: str, classes: list[str]) -> str:
    low = name.lower().replace("_", " ").replace("-", " ")
    for c in classes:
        words = [w for w in c.lower().split() if w.isalpha()]
        if words and all(w in low for w in words):
            return c
    return classes[0]


def _uploads(live: vl.LiveState) -> None:
    section("Learn from photos and videos", "Upload photos (jpg/png) or short videos (mp4, up to 30 seconds — sampled "
            "at 5 frames per second). Name files like “thumbs_up_1.jpg” and the class is picked for you.",
            kicker="Upload")
    files = st.file_uploader("Training photos or videos", type=["jpg", "jpeg", "png", "mp4", "mov"],
                             accept_multiple_files=True, key="vl_up_train")
    if files:
        labels = {}
        with st.container(key="card_labels"):
            for i, f in enumerate(files):
                default = _guess_label(f.name, live.classes)
                labels[f.name] = st.selectbox(f.name, live.classes, index=live.classes.index(default),
                                              key=f"vl_lab_{i}_{f.name}")
        if st.button("Add to training data", key="vl_add_up", type="primary") and _load_detector(live):
            added, frames, misses = 0, 0, 0
            with st.spinner("Finding hands…"):
                for f in files:
                    for _, rgb in _media_frames(f):
                        frames += 1
                        hands = live.det.detect(rgb)
                        if not hands:
                            misses += 1
                            continue
                        from sla.vision.features import normalise
                        live.add(normalise(hands[0].landmarks, hands[0].handedness), labels[f.name], "upload")
                        added += 1
                        if live.save_images:
                            live._save_image(rgb, labels[f.name])
            st.success(f"Added {added} samples from {frames} frames ({misses} without a visible hand were skipped).")

    section("Test on something new", "Upload a photo or video the learner has never seen and check each frame.",
            kicker="Test mode")
    test = st.file_uploader("Test photo or video", type=["jpg", "jpeg", "png", "mp4", "mov"], key="vl_up_test")
    if test is None:
        return
    if not live.y:
        empty_state("The learner has no samples yet.", next_step="Add training samples first (webcam or upload).",
                    glyph="inbox")
        return
    if not _load_detector(live):
        return
    times, labels, conf, last_img = [], [], [], None
    for t, rgb in _media_frames(test):
        out, pred = live.process(rgb, "test", record=False)
        times.append(t)
        labels.append(pred.label)
        conf.append(pred.proba.get(pred.label, 0.0) if pred.label else 0.0)
        last_img = out
    if len(times) <= 1:
        st.image(last_img, caption=f"Prediction: {labels[0] or 'no hand found'}", width="stretch")
    else:
        chart_card(prediction_timeline(times, labels, conf), "Prediction per frame",
                   f"{len(times)} frames · marker size = confidence", key="vl_timeline")


def _media_frames(f):
    """Yield (time, RGB) for an uploaded image (one frame) or video (sampled frames)."""
    name = f.name.lower()
    if name.endswith((".mp4", ".mov")):
        from sla.vision.video import frames
        with tempfile.NamedTemporaryFile(suffix=Path(name).suffix, delete=False) as tmp:
            tmp.write(f.getvalue())
            path = tmp.name
        try:
            yield from frames(path)
        finally:
            Path(path).unlink(missing_ok=True)
    else:
        yield 0.0, _decode(f.getvalue())


# ---------------------------------------------------------------------------------------------- tab 3: human RL
REWARD_KEYS = {"+1 (good move)": 1.0, "−1 (bad move)": -1.0, "pause": "pause", "reset": "reset"}


def _default_class(live: vl.LiveState, words: tuple[str, ...]) -> int:
    for i, c in enumerate(live.classes):
        if any(w in c.lower() for w in words):
            return i
    return 0


def _agent():
    from sla.vision.human_rl import HumanFeedbackAgent
    if "vl_agent" not in st.session_state:
        st.session_state["vl_agent"] = HumanFeedbackAgent()
    return st.session_state["vl_agent"]


def _human_rl(live: vl.LiveState) -> None:
    section("Gestures teach the agent", "The agent proposes a move on FrozenLake. Your 👍 gives +1, your 👎 gives −1. "
            "It updates its Q-table with YOUR reward, so it learns what you approve of.", kicker="Human in the loop")
    agent = _agent()
    with st.expander("Gesture → action mapping", expanded=False):
        m = {
            "good": st.selectbox("+1 (good move)", live.classes, index=_default_class(live, ("thumbs up", "👍")),
                                 key="vl_map_good"),
            "bad": st.selectbox("−1 (bad move)", live.classes, index=_default_class(live, ("thumbs down", "👎")),
                                key="vl_map_bad"),
            "pause": st.selectbox("Pause", live.classes, index=_default_class(live, ("palm", "✋")),
                                  key="vl_map_pause"),
            "reset": st.selectbox("Reset episode", live.classes, index=_default_class(live, ("fist", "✊")),
                                  key="vl_map_reset"),
        }
    use_gestures = st.toggle("React to my live gestures (needs a trained gesture learner and the live camera in tab ①)",
                             key="vl_use_gestures", disabled=not live.ready())
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("👍 Good move (+1)", key="vl_good", width="stretch"):
        agent.feedback(1.0)
    if c2.button("👎 Bad move (−1)", key="vl_bad", width="stretch"):
        agent.feedback(-1.0)
    c3.toggle("✋ Pause", key="vl_paused")
    if c4.button("✊ Reset episode", key="vl_reset", width="stretch"):
        agent.reset_episode()
    _agent_live(live, m, use_gestures)

    if agent.history:
        chart_card(reward_bars(agent.history), "Human reward per episode",
                   "gold = the agent reached the goal", key="vl_rewards")
        goals = sum(h["end_reason"] == "goal" for h in agent.history)
        st.caption(f"{len(agent.history)} episodes · reached the goal {goals} time(s).")
    allowed = auth.member_gate("save this session to the experiment database", "vl_save_rl")
    if allowed and agent.history and st.button("Save session to the database", key="vl_save_rl_btn", type="primary"):
        run_id = agent.save(services().db)
        st.success(f"Saved as run {run_id}.")
        routes.link("runs", "Open it in the Run explorer →", "outline", "vl_run")


@st.fragment(run_every=1.0)
def _agent_live(live: vl.LiveState, mapping: dict, use_gestures: bool) -> None:
    agent = _agent()
    paused = st.session_state.get("vl_paused") or st.session_state.get("vl_gesture_pause")
    if use_gestures:
        g = live.stable_gesture()
        now = time.time()
        if g and now - st.session_state.get("vl_last_gesture_at", 0) > 2.0:  # cool-down: one action per gesture
            st.session_state["vl_last_gesture_at"] = now
            if g == mapping["pause"]:  # the pause gesture toggles pause / resume
                st.session_state["vl_gesture_pause"] = not st.session_state.get("vl_gesture_pause")
            elif paused:
                pass
            elif g == mapping["good"]:
                agent.feedback(1.0)
            elif g == mapping["bad"]:
                agent.feedback(-1.0)
            elif g == mapping["reset"]:
                agent.reset_episode()
    st.markdown(_grid_html(agent), unsafe_allow_html=True)
    from sla.vision.human_rl import ACTIONS
    state = " · ⏸ paused" if (st.session_state.get("vl_paused") or st.session_state.get("vl_gesture_pause")) else ""
    st.caption(f"Episode {agent.episode + 1} · step {agent.steps} · reward so far {agent.total:+.0f} · "
               f"proposed move: **{ACTIONS[agent.proposal]}**{state}")


def _grid_html(agent) -> str:
    from sla.vision.human_rl import ARROWS, MAP
    policy = agent.greedy_policy()
    cells = []
    for s in range(16):
        kind = MAP[s // 4][s % 4]
        cls = {"H": "hole", "G": "goal", "S": "start"}.get(kind, "ice")
        here = s == agent.state
        txt = "🤖" if here else {"H": "HOLE", "G": "GOAL"}.get(kind, policy[s])
        prop = f'<span class="prop">{ARROWS[agent.proposal]}</span>' if here and agent.proposal is not None else ""
        cells.append(f'<div class="cell {cls}{" here" if here else ""}">{txt}{prop}</div>')
    return f'<div class="sla-lake" role="img" aria-label="FrozenLake board">{"".join(cells)}</div>'


# ---------------------------------------------------------------------------------------------- tab 4: results
@st.cache_data(show_spinner="Measuring on held-out samples…", max_entries=8)
def _evaluate(digest: str, X: np.ndarray, y: tuple[str, ...], kind: str):
    return evaluate(X, list(y), kind=kind)


def _results(live: vl.LiveState) -> None:
    section("Results", "Measured on a held-out 20% of YOUR samples (never used for learning), compared with guessing.",
            kicker="Proof")
    X, y = live.arrays()
    counts = live.counts()
    if not live.ready():
        card_grid([metric_card(f"{c}", n, "samples", "{:,}", icon="layers", count=False) for c, n in counts.items()],
                  min_width=150)
        empty_state("Not enough samples to measure yet.",
                    next_step=f"Add at least {vl.MIN_PER_CLASS} samples for two or more classes (tab ① or ②).",
                    glyph="flask")
        _model_store(live, None)
        return
    keep = [i for i, c in enumerate(y) if counts.get(c, 0) >= 2]
    Xk, yk = X[keep], tuple(y[i] for i in keep)
    digest = hashlib.sha1(Xk.tobytes() + json.dumps(yk).encode()).hexdigest()
    knn = _evaluate(digest, Xk, yk, "knn")
    mlp = _evaluate(digest, Xk, yk, "mlp")
    card_grid([
        metric_card("k-NN accuracy", knn.accuracy * 100, f"95% CI {knn.ci95[0]:.0%}–{knn.ci95[1]:.0%} · "
                    f"{knn.n_test} held-out samples", "{:.0f}%", icon="check", accent="#C9A24B", count=False),
        metric_card("Neural network accuracy", mlp.accuracy * 100, f"95% CI {mlp.ci95[0]:.0%}–{mlp.ci95[1]:.0%}",
                    "{:.0f}%", icon="cpu", count=False),
        metric_card("Chance level", knn.chance * 100, f"guessing among {len(knn.classes)} classes", "{:.0f}%",
                    icon="dice", count=False),
        metric_card("Samples", len(yk), f"{knn.n_train} to learn · {knn.n_test} to test", "{:,}", icon="layers"),
        metric_card("Speed", live.mean_ms() or None, "ms per frame (hand detection + prediction)", "{:.0f}",
                    icon="clock", count=False),
    ], min_width=170)
    a, b = st.columns(2, gap="medium")
    with a:
        chart_card(accuracy_curve({"k-NN": knn.curve, "Neural network": mlp.curve}, knn.chance),
                   "Learning curve", "held-out accuracy as more samples are learned", key="vl_curve")
    with b:
        chart_card(confusion_heatmap(knn.classes, knn.confusion), "Confusion matrix (k-NN)",
                   "rows = true gesture · columns = predicted", key="vl_conf")
    st.caption("Per-class accuracy (k-NN): " + " · ".join(f"{c} {v:.0%}" for c, v in knn.per_class.items()))
    _model_card(knn, mlp, counts)
    _model_store(live, knn)


def _model_card(knn, mlp, counts: dict) -> None:
    section("Model card", kicker="Transparency")
    st.markdown(
        f"- **What it learns:** to tell {len(knn.classes)} hand gestures apart from 21 hand points (42 numbers per "
        "sample, centred on the wrist and scaled by hand size).\n"
        f"- **Data:** {sum(counts.values())} samples you recorded or uploaded in this session "
        f"({', '.join(f'{c}: {n}' for c, n in counts.items())}).\n"
        f"- **Measured:** k-NN {knn.accuracy:.0%} and neural network {mlp.accuracy:.0%} on {knn.n_test} held-out "
        f"samples, versus {knn.chance:.0%} for guessing.\n"
        "- **Limits:** one hand at a time; trained on one person's hands unless you add others; poor light, motion "
        "blur and very close-ups (where the palm fills the picture) make detection fail. Accuracy on new people, "
        "skin tones and cameras is unknown until you test it — record samples from different people to check "
        "for bias.\n"
        "- **Privacy:** only hand-point numbers are stored; no faces or pictures unless “save images” is ticked; "
        "nothing leaves this server.")


def _model_store(live: vl.LiveState, ev) -> None:
    section("Save, load and export", kicker="Models")
    db, user = services().db, auth.current_user()
    X, y = live.arrays()
    if ev is not None:
        export = {"kind": "knn", "classes": live.classes, "features": "wrist-centred, scale-normalised 21x2",
                  "accuracy_heldout": ev.accuracy, "model": live.knn.to_dict()}
        st.download_button("Export model (.json)", json.dumps(export), file_name="gesture_model.json",
                           mime="application/json", key="vl_export")
    if not auth.member_gate("save and load gesture models", "vl_models"):
        return
    owner = user["email"]
    if ev is not None:
        name = st.text_input("Model name", f"Gestures · {time.strftime('%d %b %H:%M')}", key="vl_model_name")
        if st.button("Save model", key="vl_save_model", type="primary"):
            model = live.knn.to_dict()
            if live.mlp is not None:
                model["mlp"] = live.mlp.to_dict()
            mid = db.save_vision_model(name, "knn", live.classes, len(y), ev.accuracy,
                                       {"ci95": ev.ci95, "chance": ev.chance, "per_class": ev.per_class}, model, owner)
            st.success(f"Saved model #{mid}.")
    saved = db.list_vision_models(owner)
    if saved.empty:
        st.caption("No saved models yet.")
        return
    labels = {int(r.model_id): f"#{r.model_id} · {r.name} · {r.n_samples} samples · "
              f"{(r.accuracy or 0):.0%} held-out" for r in saved.itertuples()}
    pick = st.selectbox("Your saved models", list(labels), format_func=labels.get, key="vl_pick_model")
    c1, c2 = st.columns(2)
    if c1.button("Load model", key="vl_load", width="stretch"):
        rec = db.get_vision_model(int(pick))
        knn = load_learner(rec["model"])
        live.load(knn.X, knn.y, rec["classes"])
        st.success(f"Loaded model #{pick} ({len(knn.y)} samples).")
    if c2.button("Delete model", key="vl_del_model", width="stretch"):
        db.delete_vision_models(owner, int(pick))
        st.rerun()
