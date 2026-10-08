"""Deep Q-Network agent.

Key ideas (Mnih et al., 2015):
  * a neural network replaces the Q-table,
  * experience replay: learn from random mini-batches of past transitions,
  * a target network, copied every C steps, gives stable learning targets.
"""

from __future__ import annotations

import copy
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F

from sla.agents.base import Agent, Transition
from sla.agents.networks import QNetwork
from sla.agents.schedules import LinearSchedule
from sla.memory.replay_buffer import Batch, ReplayBuffer
from sla.training.config import DQNConfig
from sla.utils.io_helpers import ensure_dir, read_json, write_json


def compute_td_target(rewards, next_q_max, terminated, gamma: float):
    """y = r + gamma * (1 - terminated) * max_a' Q_target(s', a').

    Works with NumPy arrays and PyTorch tensors. Only *terminated* stops
    bootstrapping; a time-limit truncation still uses the next state's value.
    """
    return rewards + gamma * (1.0 - terminated) * next_q_max


class DQNAgent(Agent):
    name = "dqn"

    def __init__(self, obs_dim: int, n_actions: int, cfg: DQNConfig | None = None, gamma: float = 0.99,
                 learning_rate: float = 1e-3, epsilon_schedule: LinearSchedule | None = None,
                 seed: int = 0) -> None:
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        self.cfg = cfg or DQNConfig()
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.schedule = epsilon_schedule or LinearSchedule(1.0, 0.05, 10_000)
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        torch.manual_seed(seed)

        self.online = QNetwork(obs_dim, n_actions, self.cfg.hidden_size)
        self.target = copy.deepcopy(self.online)
        self.target.eval()
        if self.cfg.optimizer == "adamw":
            self.optimizer = torch.optim.AdamW(self.online.parameters(), lr=learning_rate,
                                               weight_decay=self.cfg.weight_decay)
        else:
            self.optimizer = torch.optim.Adam(self.online.parameters(), lr=learning_rate)
        capacity = self.cfg.buffer_size if self.cfg.replay_enabled else 1
        self.buffer = ReplayBuffer(capacity, obs_dim, seed)

        self.steps = 0          # environment steps seen
        self.updates = 0        # gradient steps taken
        self.last_loss: float | None = None
        self.last_max_q: float | None = None

    # ----- acting ---------------------------------------------------------
    @property
    def epsilon(self) -> float:
        return self.schedule.value(self.steps)

    def q_values(self, obs: Any) -> np.ndarray:
        with torch.no_grad():
            x = torch.as_tensor(np.asarray(obs, dtype=np.float32).reshape(1, -1))
            return self.online(x).squeeze(0).numpy()

    def act(self, obs: Any, explore: bool = True) -> int:
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return int(np.argmax(self.q_values(obs)))

    # ----- learning -------------------------------------------------------
    def update(self, transition: Transition) -> dict[str, float]:
        self.buffer.push(transition.state, transition.action, transition.reward,
                         transition.next_state, transition.terminated)
        self.steps += 1
        stats: dict[str, float] = {}
        if self.steps >= self.cfg.learning_starts and self.steps % self.cfg.train_freq == 0:
            if self.cfg.replay_enabled:
                if len(self.buffer) >= self.cfg.batch_size:
                    stats["loss"] = self.train_step(self.buffer.sample(self.cfg.batch_size))
            else:
                stats["loss"] = self.train_step(self.buffer.latest())
        if self.cfg.target_net_enabled and self.steps % self.cfg.target_update_every == 0:
            self.sync_target()
        return stats

    def train_step(self, batch: Batch) -> float:
        states = torch.as_tensor(batch.states)
        actions = torch.as_tensor(batch.actions).long()
        rewards = torch.as_tensor(batch.rewards)
        next_states = torch.as_tensor(batch.next_states)
        terminated = torch.as_tensor(batch.terminated)

        q = self.online(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            bootstrap_net = self.target if self.cfg.target_net_enabled else self.online
            next_q_max = bootstrap_net(next_states).max(dim=1).values
            target = compute_td_target(rewards, next_q_max, terminated, self.gamma)
        loss = F.smooth_l1_loss(q, target)  # Huber loss

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.online.parameters(), self.cfg.grad_clip)
        self.optimizer.step()

        self.updates += 1
        self.last_loss = float(loss.item())
        self.last_max_q = float(q.detach().abs().max().item())
        return self.last_loss

    def sync_target(self) -> None:
        self.target.load_state_dict(self.online.state_dict())

    # ----- saving ---------------------------------------------------------
    def save(self, path: Path, include_buffer: bool = True) -> None:
        folder = ensure_dir(path)
        torch.save({"online": self.online.state_dict(), "target": self.target.state_dict(),
                    "optimizer": self.optimizer.state_dict()}, folder / "dqn.pt")
        write_json(folder / "meta.json", {
            "agent": self.name, "obs_dim": self.obs_dim, "n_actions": self.n_actions,
            "cfg": asdict(self.cfg), "gamma": self.gamma, "learning_rate": self.learning_rate,
            "schedule": {"start": self.schedule.start, "end": self.schedule.end, "duration": self.schedule.duration},
            "seed": self.seed, "steps": self.steps, "updates": self.updates,
            "rng_state": self.rng.bit_generator.state,
            "buffer_rng_state": self.buffer.rng.bit_generator.state,
        })
        if include_buffer and len(self.buffer) > 0:
            self.buffer.save(folder / "replay.npz")

    @classmethod
    def load(cls, path: Path) -> DQNAgent:
        folder = Path(path)
        meta = read_json(folder / "meta.json")
        agent = cls(meta["obs_dim"], meta["n_actions"], DQNConfig(**meta["cfg"]), meta["gamma"],
                    meta["learning_rate"], LinearSchedule(**meta["schedule"]), meta["seed"])
        state = torch.load(folder / "dqn.pt", map_location="cpu", weights_only=True)
        agent.online.load_state_dict(state["online"])
        agent.target.load_state_dict(state["target"])
        agent.optimizer.load_state_dict(state["optimizer"])
        agent.steps, agent.updates = meta["steps"], meta["updates"]
        agent.rng.bit_generator.state = meta["rng_state"]
        agent.buffer.rng.bit_generator.state = meta["buffer_rng_state"]
        if (folder / "replay.npz").exists():
            agent.buffer.load_from(folder / "replay.npz")
        return agent
