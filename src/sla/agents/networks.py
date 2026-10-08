"""Neural network that estimates Q-values."""

from __future__ import annotations

import torch
from torch import nn


class QNetwork(nn.Module):
    """Small MLP: state (obs_dim numbers) -> one Q-value per action.

    For CartPole: 4 -> 128 -> 128 -> 2.
    """

    def __init__(self, obs_dim: int, n_actions: int, hidden_size: int = 128) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)
