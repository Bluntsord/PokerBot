from __future__ import annotations
import torch
import torch.nn as nn
from typing import List, Tuple

from engine.types import Card, Street, Action, ActionType
from train.config import (
    NUM_CARDS, NUM_RANKS, NUM_SUITS, NUM_STREETS,
    NUM_ACTIONS, MAX_PLAYERS,
    ACTION_FOLD, ACTION_CHECK_CALL, ACTION_BET_05,
    ACTION_BET_075, ACTION_BET_10, ACTION_BET_15,
    ACTION_ALL_IN, AVAILABLE_ACTIONS,
)


def encode_cards(card_ids: List[int]) -> torch.Tensor:
    vec = torch.zeros(NUM_CARDS, dtype=torch.float32)
    for cid in card_ids:
        if 0 <= cid < NUM_CARDS:
            vec[cid] = 1.0
    return vec


def encode_hand_rank_features(card_ids: List[int]) -> torch.Tensor:
    vec = torch.zeros(NUM_RANKS, dtype=torch.float32)
    for cid in card_ids:
        rank = cid % 13
        vec[rank] += 1.0
    return vec


def encode_hand_suit_features(card_ids: List[int]) -> torch.Tensor:
    vec = torch.zeros(NUM_SUITS, dtype=torch.float32)
    for cid in card_ids:
        suit = cid // 13
        vec[suit] += 1.0
    return vec


def encode_betting_features(state_dict: dict, player_id: int) -> torch.Tensor:
    features = []

    pot = state_dict["pot"] + sum(
        state_dict.get("_current_bets", [0] * MAX_PLAYERS)[:state_dict.get("num_players", 2)]
    ) if "_current_bets" in state_dict else state_dict["pot"]
    stack = state_dict["stack"]
    starting_stack = state_dict.get("starting_stack", state_dict["stack"])
    effective_stack = min(stack, state_dict.get("opp_stack", stack))

    pot_frac = pot / max(starting_stack, 1)
    stack_frac = effective_stack / max(starting_stack, 1)
    to_call_frac = state_dict.get("to_call", 0) / max(pot + 1, 1)

    features.extend([pot_frac, stack_frac, to_call_frac])

    street = state_dict.get("street", "PREFLOP")
    street_idx = {"PREFLOP": 0, "FLOP": 1, "TURN": 2, "RIVER": 3}.get(street, 0)
    street_onehot = [0.0] * NUM_STREETS
    street_onehot[street_idx] = 1.0
    features.extend(street_onehot)

    position = state_dict.get("position", 0)
    num_players = state_dict.get("num_players", 2)
    pos_onehot = [0.0] * MAX_PLAYERS
    pos_onehot[max(0, min(position, MAX_PLAYERS - 1))] = 1.0
    features.extend(pos_onehot)

    num_active = state_dict.get("num_active", 2)
    active_frac = (num_active - 1) / max(num_players - 1, 1)
    features.append(active_frac)

    return torch.tensor(features, dtype=torch.float32)


def encode_action_history(
    action_history: List[dict], max_len: int = 8
) -> torch.Tensor:
    encoded = torch.zeros(max_len * 3, dtype=torch.float32)
    history = action_history[-max_len:] if len(action_history) > max_len else action_history

    for i, act in enumerate(history):
        action_type = act.get("action", "FOLD")
        is_aggressive = float(action_type in ("BET", "RAISE", "ALL_IN"))
        is_passive = float(action_type in ("CHECK", "CALL"))
        relative_amount = min(act.get("amount", 0) / max(act.get("amount", 0) + 1, 1), 1.0)
        base = i * 3
        encoded[base] = is_aggressive
        encoded[base + 1] = is_passive
        encoded[base + 2] = relative_amount

    return encoded


def compute_action_mask(state_dict: dict) -> torch.Tensor:
    mask = torch.zeros(NUM_ACTIONS, dtype=torch.bool)

    to_call = state_dict.get("to_call", 0)
    stack = state_dict["stack"]
    pot = state_dict.get("pot", 0)

    if to_call > 0:
        mask[ACTION_FOLD] = True
        if to_call < stack:
            mask[ACTION_CHECK_CALL] = True
        else:
            mask[ACTION_BET_15] = True
    else:
        mask[ACTION_CHECK_CALL] = True

    for idx, frac in zip(
        [ACTION_BET_05, ACTION_BET_075, ACTION_BET_10, ACTION_BET_15],
        [0.5, 0.75, 1.0, 1.5],
    ):
        bet_size = int(pot * frac) if pot > 0 else state_dict.get("big_blind", 2) * 2
        bet_size = max(bet_size, state_dict.get("big_blind", 2))
        if to_call + bet_size < stack:
            mask[idx] = True

    mask[ACTION_CHECK_CALL] = True
    if to_call >= stack:
        mask[ACTION_CHECK_CALL] = False
        mask[ACTION_BET_15] = True

    return mask


class StateEncoder:
    def __init__(self, device: str = "cpu"):
        self.device = device

    def encode(
        self,
        hole_cards: List[int],
        board_cards: List[int],
        state_dict: dict,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        hole_vec = encode_cards(hole_cards).to(self.device)
        board_vec = encode_cards(board_cards).to(self.device)
        rank_vec = encode_hand_rank_features(hole_cards + board_cards).to(self.device)
        suit_vec = encode_hand_suit_features(hole_cards + board_cards).to(self.device)
        bet_vec = encode_betting_features(state_dict, state_dict.get("player_id", 0)).to(self.device)
        hist_vec = encode_action_history(state_dict.get("action_history", [])).to(self.device)

        combined = torch.cat([hole_vec, board_vec, rank_vec, suit_vec, bet_vec, hist_vec])
        action_mask = compute_action_mask(state_dict).to(self.device)

        legal_binary = action_mask.float()
        legal_binary[ACTION_FOLD] = 1.0
        legal_binary[ACTION_CHECK_CALL] = 1.0

        return combined, action_mask, legal_binary

    def batch_encode(
        self,
        batch_hole_cards: List[List[int]],
        batch_board_cards: List[List[int]],
        batch_state_dicts: List[dict],
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        tensors = []
        masks = []
        legal_binaries = []

        for hole, board, state in zip(batch_hole_cards, batch_board_cards, batch_state_dicts):
            t, m, l = self.encode(hole, board, state)
            tensors.append(t)
            masks.append(m)
            legal_binaries.append(l)

        return (
            torch.stack(tensors),
            torch.stack(masks),
            torch.stack(legal_binaries),
        )

    @property
    def state_dim(self) -> int:
        __tracebackhide__ = True
        return (
            NUM_CARDS * 2
            + NUM_RANKS
            + NUM_SUITS
            + 3
            + NUM_STREETS
            + MAX_PLAYERS
            + 1
            + 8 * 3
        )


NUM_ACTIONS = 6
