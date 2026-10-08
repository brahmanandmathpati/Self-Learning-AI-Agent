"""Global random seeding.

Seeding makes runs reproducible: the same seed gives the same results.
"""

from __future__ import annotations

import os
import random

import numpy as np


def set_global_seed(seed: int) -> None:
    """Seed Python, NumPy and (if installed) PyTorch."""
    if not isinstance(seed, int) or seed < 0:
        raise ValueError(f"seed must be a non-negative int, got {seed!r}")
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
    except ImportError:  # PyTorch is only needed for the DQN
        return
    torch.manual_seed(seed)


def episode_seed(base_seed: int, episode: int) -> int:
    """Seed used for env.reset() in a given episode.

    Using base_seed * 100_000 + episode means every episode starts from a known
    state, so a resumed run continues exactly where it stopped.
    """
    return base_seed * 100_000 + episode
