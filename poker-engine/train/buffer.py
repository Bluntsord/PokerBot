from __future__ import annotations
import torch
import numpy as np
from collections import deque
from typing import List, Tuple, Optional
import random


class ReplayBuffer:
    def __init__(self, capacity: int, state_dim: int, device: str = "cpu"):
        self.capacity = capacity
        self.device = device

        self.states = torch.zeros(capacity, state_dim, dtype=torch.float32)
        self.target_values = torch.zeros(capacity, 6, dtype=torch.float32)
        self.action_masks = torch.zeros(capacity, 6, dtype=torch.bool)
        self.weights = torch.ones(capacity, dtype=torch.float32)

        self.head = 0
        self.size = 0
        self.full = False

    def add(
        self,
        state: torch.Tensor,
        target_values: torch.Tensor,
        action_mask: torch.Tensor,
        weight: float = 1.0,
    ):
        idx = self.head

        self.states[idx] = state.cpu()
        self.target_values[idx] = target_values.cpu()
        self.action_masks[idx] = action_mask.cpu()
        self.weights[idx] = weight

        self.head = (self.head + 1) % self.capacity
        if self.full:
            self.size = self.capacity
        else:
            self.size += 1
            if self.size >= self.capacity:
                self.full = True

    def sample(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        if self.size < batch_size:
            indices = list(range(self.size))
            indices = indices * (batch_size // self.size + 1)
            indices = indices[:batch_size]
        else:
            probs = self.weights[:self.size].numpy()
            probs = probs / probs.sum()
            indices = np.random.choice(self.size, size=batch_size, replace=False, p=probs)

        states = self.states[indices].to(self.device)
        targets = self.target_values[indices].to(self.device)
        masks = self.action_masks[indices].to(self.device)
        sample_weights = self.weights[indices].to(self.device)

        return states, targets, masks, sample_weights

    def sample_uniform(
        self, batch_size: int
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if self.size < batch_size:
            indices = list(range(self.size)) * (batch_size // self.size + 1)
            indices = indices[:batch_size]
        else:
            indices = random.sample(range(self.size), batch_size)

        states = self.states[indices].to(self.device)
        targets = self.target_values[indices].to(self.device)
        masks = self.action_masks[indices].to(self.device)

        return states, targets, masks

    def update_weights(self, indices: List[int], new_weights: List[float]):
        for idx, w in zip(indices, new_weights):
            if idx < self.size:
                self.weights[idx] = w

    def clear(self):
        self.head = 0
        self.size = 0
        self.full = False

    def __len__(self) -> int:
        return self.size


class RegretBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.states: deque = deque(maxlen=capacity)
        self.regrets: deque = deque(maxlen=capacity)
        self.masks: deque = deque(maxlen=capacity)

    def add(self, state: torch.Tensor, regrets: torch.Tensor, mask: torch.Tensor):
        self.states.append(state)
        self.regrets.append(regrets)
        self.masks.append(mask)

    def sample_all(self):
        if len(self.states) == 0:
            return None, None, None
        return (
            torch.stack(list(self.states)),
            torch.stack(list(self.regrets)),
            torch.stack(list(self.masks)),
        )

    def clear(self):
        self.states.clear()
        self.regrets.clear()
        self.masks.clear()

    def __len__(self) -> int:
        return len(self.states)
