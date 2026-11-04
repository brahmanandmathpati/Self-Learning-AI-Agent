"""Gesture learners and honest evaluation.

* ``KNNLearner`` learns online: every new sample is used immediately (no training step).
* ``MLPLearner`` is a tiny PyTorch network (42 → 64 → classes) trained on demand.
* ``evaluate`` holds out 20% of the samples (stratified, fixed seed), so the reported accuracy is measured on
  samples the learner never saw. ``learning_curve`` shows accuracy on that same held-out set as more training
  samples are added; ``bootstrap_ci`` gives a 95% interval; the chance baseline is 1 / number of classes.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


class KNNLearner:
    """k-nearest-neighbours on normalised landmarks. ``add`` is the online learning step."""

    kind = "knn"

    def __init__(self, k: int = 5) -> None:
        self.k = k
        self.X = np.zeros((0, 0), dtype=np.float32)
        self.y: list[str] = []

    @property
    def classes(self) -> list[str]:
        return sorted(set(self.y))

    def add(self, x: np.ndarray, label: str) -> None:
        x = np.asarray(x, dtype=np.float32).reshape(1, -1)
        self.X = x if self.X.size == 0 else np.vstack([self.X, x])
        self.y.append(label)

    def fit(self, X: np.ndarray, y: list[str]) -> KNNLearner:
        self.X, self.y = np.asarray(X, dtype=np.float32), list(y)
        return self

    def predict_proba(self, x: np.ndarray) -> dict[str, float]:
        """Share of the k nearest samples per class (distance-weighted)."""
        if not self.y:
            return {}
        d = np.linalg.norm(self.X - np.asarray(x, dtype=np.float32).reshape(1, -1), axis=1)
        idx = np.argsort(d)[: min(self.k, len(self.y))]
        w = 1.0 / (d[idx] + 1e-6)
        scores: dict[str, float] = {}
        for i, wi in zip(idx, w):
            scores[self.y[i]] = scores.get(self.y[i], 0.0) + float(wi)
        total = sum(scores.values())
        return dict(sorted(((c, s / total) for c, s in scores.items()), key=lambda t: -t[1]))

    def predict(self, x: np.ndarray) -> str | None:
        p = self.predict_proba(x)
        return next(iter(p)) if p else None

    def to_dict(self) -> dict:
        return {"kind": self.kind, "k": self.k, "X": self.X.tolist(), "y": self.y}

    @classmethod
    def from_dict(cls, d: dict) -> KNNLearner:
        return cls(int(d.get("k", 5))).fit(np.asarray(d["X"], dtype=np.float32), list(d["y"]))


class MLPLearner:
    """A tiny neural network (42 → 64 → n_classes) trained with Adam; deterministic for a given seed."""

    kind = "mlp"

    def __init__(self, hidden: int = 64, epochs: int = 200, lr: float = 0.01, seed: int = 0) -> None:
        self.hidden, self.epochs, self.lr, self.seed = hidden, epochs, lr, seed
        self.classes: list[str] = []
        self.model = None

    def fit(self, X: np.ndarray, y: list[str]) -> MLPLearner:
        import torch
        from torch import nn
        torch.manual_seed(self.seed)
        self.classes = sorted(set(y))
        idx = {c: i for i, c in enumerate(self.classes)}
        xt = torch.tensor(np.asarray(X, dtype=np.float32))
        yt = torch.tensor([idx[c] for c in y], dtype=torch.long)
        self.model = nn.Sequential(nn.Linear(xt.shape[1], self.hidden), nn.ReLU(), nn.Linear(self.hidden, len(idx)))
        opt = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        loss_fn = nn.CrossEntropyLoss()
        self.model.train()
        for _ in range(self.epochs):
            opt.zero_grad()
            loss = loss_fn(self.model(xt), yt)
            loss.backward()
            opt.step()
        self.model.eval()
        return self

    def predict_proba(self, x: np.ndarray) -> dict[str, float]:
        if self.model is None:
            return {}
        import torch
        with torch.no_grad():
            p = torch.softmax(self.model(torch.tensor(np.asarray(x, dtype=np.float32).reshape(1, -1))), dim=1)[0]
        return dict(sorted(((c, float(v)) for c, v in zip(self.classes, p)), key=lambda t: -t[1]))

    def predict(self, x: np.ndarray) -> str | None:
        p = self.predict_proba(x)
        return next(iter(p)) if p else None

    def to_dict(self) -> dict:
        state = {k: v.tolist() for k, v in self.model.state_dict().items()} if self.model is not None else {}
        return {"kind": self.kind, "hidden": self.hidden, "classes": self.classes, "state": state}

    @classmethod
    def from_dict(cls, d: dict) -> MLPLearner:
        import torch
        from torch import nn
        m = cls(hidden=int(d["hidden"]))
        m.classes = list(d["classes"])
        state = {k: torch.tensor(v) for k, v in d["state"].items()}
        m.model = nn.Sequential(nn.Linear(state["0.weight"].shape[1], m.hidden), nn.ReLU(),
                                nn.Linear(m.hidden, len(m.classes)))
        m.model.load_state_dict(state)
        m.model.eval()
        return m


def make_learner(kind: str):
    return MLPLearner() if kind == "mlp" else KNNLearner()


def load_learner(d: dict):
    return MLPLearner.from_dict(d) if d.get("kind") == "mlp" else KNNLearner.from_dict(d)


# ---------------------------------------------------------------------------------------------- evaluation
def stratified_split(y: list[str], test_frac: float = 0.2, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Indices for train / held-out test; every class keeps at least one sample on each side when it can."""
    rng = np.random.default_rng(seed)
    y_arr = np.asarray(y)
    train, test = [], []
    for c in sorted(set(y)):
        idx = np.flatnonzero(y_arr == c)
        rng.shuffle(idx)
        n_test = int(round(len(idx) * test_frac))
        if len(idx) >= 2:
            n_test = min(max(n_test, 1), len(idx) - 1)
        test.extend(idx[:n_test])
        train.extend(idx[n_test:])
    return np.asarray(sorted(train), dtype=int), np.asarray(sorted(test), dtype=int)


def bootstrap_ci(correct: np.ndarray, n_boot: int = 2000, seed: int = 0) -> tuple[float, float]:
    correct = np.asarray(correct, dtype=float)
    if correct.size == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = rng.choice(correct, size=(n_boot, correct.size), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


@dataclass
class Evaluation:
    classes: list[str]
    n_train: int
    n_test: int
    accuracy: float
    ci95: tuple[float, float]
    chance: float
    per_class: dict[str, float]
    confusion: list[list[int]]  # rows = true class, columns = predicted class
    curve: list[tuple[int, float]] = field(default_factory=list)  # (training samples used, held-out accuracy)


def evaluate(X: np.ndarray, y: list[str], kind: str = "knn", seed: int = 0, curve_points: int = 8) -> Evaluation:
    """Train on 80%, measure on the held-out 20%. Needs at least 2 classes with 2+ samples each."""
    X = np.asarray(X, dtype=np.float32)
    classes = sorted(set(y))
    if len(classes) < 2 or min(y.count(c) for c in classes) < 2:
        raise ValueError("need at least 2 classes with 2 or more samples each")
    tr, te = stratified_split(y, seed=seed)
    ytr, yte = [y[i] for i in tr], [y[i] for i in te]
    model = make_learner(kind).fit(X[tr], ytr)
    pred = [model.predict(X[i]) for i in te]
    correct = np.asarray([p == t for p, t in zip(pred, yte)], dtype=float)
    pos = {c: i for i, c in enumerate(classes)}
    conf = [[0] * len(classes) for _ in classes]
    for t, p in zip(yte, pred):
        if p in pos:
            conf[pos[t]][pos[p]] += 1
    per_class = {c: (conf[pos[c]][pos[c]] / max(1, sum(conf[pos[c]]))) for c in classes}
    curve = learning_curve(X[tr], ytr, X[te], yte, kind=kind, points=curve_points, seed=seed)
    return Evaluation(classes, len(tr), len(te), float(correct.mean()), bootstrap_ci(correct, seed=seed),
                      1.0 / len(classes), per_class, conf, curve)


def learning_curve(Xtr: np.ndarray, ytr: list[str], Xte: np.ndarray, yte: list[str], kind: str = "knn",
                   points: int = 8, seed: int = 0) -> list[tuple[int, float]]:
    """Held-out accuracy after training on growing, class-balanced subsets of the training samples."""
    rng = np.random.default_rng(seed)
    order = np.arange(len(ytr))
    rng.shuffle(order)
    classes = sorted(set(ytr))
    # interleave classes so every prefix contains every class as early as possible
    by_class = {c: [i for i in order if ytr[i] == c] for c in classes}
    inter = [i for group in zip(*[by_class[c] + [None] * (len(order) - len(by_class[c])) for c in classes])
             for i in group if i is not None]
    sizes = sorted({int(s) for s in np.linspace(len(classes), len(inter), num=min(points, len(inter))) if s >= 1})
    out = []
    for n in sizes:
        sub = inter[:n]
        sub_y = [ytr[i] for i in sub]
        if kind == "mlp" and len(set(sub_y)) < 2:
            continue
        m = make_learner(kind).fit(Xtr[sub], sub_y)
        acc = float(np.mean([m.predict(Xte[i]) == yte[i] for i in range(len(yte))]))
        out.append((n, acc))
    return out
