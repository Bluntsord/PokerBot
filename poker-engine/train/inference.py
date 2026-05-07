from __future__ import annotations
import torch
import random
from typing import List, Tuple, Dict, Optional

from engine.game import GameEngine, GameConfig, GameState
from engine.types import Action, ActionType, Card, Street, PlayerState
from engine.evaluator import ensure_initialized

from train.config import (
    TrainingConfig, NUM_ACTIONS, ACTION_FOLD, ACTION_CHECK_CALL,
    ACTION_BET_05, ACTION_BET_075, ACTION_BET_10, ACTION_BET_15,
    NUM_CARDS, AVAILABLE_ACTIONS,
)
from train.encoding import StateEncoder
from train.model import DeepCFRNet, create_model


class CFRInferenceAgent:
    def __init__(
        self,
        checkpoint_path: str,
        device: str = "cuda",
        temperature: float = 0.1,
    ):
        ensure_initialized()

        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.temperature = temperature

        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        model_config_dict = checkpoint.get("config", {})
        model_config = model_config_dict.get("model", {})
        if isinstance(model_config, dict):
            from train.config import ModelConfig
            cfg = ModelConfig(**model_config)
        else:
            from train.config import ModelConfig
            cfg = ModelConfig()

        self.model = create_model(cfg, device=self.device.type)
        self.model.load_state_dict(checkpoint["value_net"])
        self.model.eval()

        self.encoder = StateEncoder(device=self.device)

        self.strategy_sum = {}
        self.strategy_count = {}
        strat_data = checkpoint.get("strategy_sum", {})
        count_data = checkpoint.get("strategy_count", {})
        for k, v in strat_data.items():
            self.strategy_sum[int(k)] = v.to(self.device)
        for k, v in count_data.items():
            self.strategy_count[int(k)] = int(v)

        self.avg_strategy = {}
        for state_hash in self.strategy_sum:
            count = self.strategy_count.get(state_hash, 1)
            self.avg_strategy[state_hash] = self.strategy_sum[state_hash] / max(count, 1)

    def get_action(
        self,
        hole_cards: List[int],
        board_cards: List[int],
        state_dict: dict,
    ) -> Tuple[int, torch.Tensor]:
        enc, mask, legal = self.encoder.encode(hole_cards, board_cards, state_dict)

        strategy = self._get_strategy(enc, mask, legal)

        probs = strategy.cpu().numpy()
        probs = probs / probs.sum()

        action_idx = int(torch.multinomial(strategy, 1).item())
        return action_idx, strategy

    def _get_strategy(
        self, enc: torch.Tensor, mask: torch.Tensor, legal: torch.Tensor
    ) -> torch.Tensor:
        enc_b = enc.unsqueeze(0)
        mask_b = mask.unsqueeze(0)

        with torch.no_grad():
            advantages, logits = self.model(enc_b, mask_b)

        strategy = torch.softmax(logits.squeeze(0) / self.temperature, dim=-1)
        strategy = strategy * legal
        strategy = strategy / (strategy.sum() + 1e-8)
        return strategy

    def _discrete_to_action(
        self, discrete_action: int, state_dict: dict, to_call: int, stack: int
    ) -> Action:
        pot = state_dict.get("pot", 0)
        bb = state_dict.get("big_blind", 2)

        if discrete_action == ACTION_FOLD:
            return Action(ActionType.FOLD)
        elif discrete_action == ACTION_CHECK_CALL:
            if to_call == 0:
                return Action(ActionType.CHECK)
            elif to_call >= stack:
                return Action(ActionType.ALL_IN, stack, is_all_in=True)
            else:
                return Action(ActionType.CALL, to_call)
        elif discrete_action == ACTION_BET_05:
            amt = max(int(pot * 0.5), bb) if pot > 0 else bb * 2
            if to_call == 0:
                if amt >= stack:
                    return Action(ActionType.ALL_IN, stack, is_all_in=True)
                return Action(ActionType.BET, amt)
            else:
                raise_total = to_call + amt
                current_bet = state_dict.get("current_bet", 0)
                if raise_total >= stack + current_bet:
                    return Action(ActionType.ALL_IN, stack, is_all_in=True)
                return Action(ActionType.RAISE, raise_total - current_bet)
        elif discrete_action == ACTION_BET_10:
            amt = max(int(pot * 1.0), bb * 2) if pot > 0 else bb * 3
            if to_call == 0:
                if amt >= stack:
                    return Action(ActionType.ALL_IN, stack, is_all_in=True)
                return Action(ActionType.BET, amt)
            else:
                raise_total = to_call + amt
                current_bet = state_dict.get("current_bet", 0)
                if raise_total >= stack + current_bet:
                    return Action(ActionType.ALL_IN, stack, is_all_in=True)
                return Action(ActionType.RAISE, raise_total - current_bet)
        elif discrete_action == ACTION_BET_15:
            amt = max(int(pot * 1.5), bb * 2) if pot > 0 else bb * 4
            if to_call == 0:
                if amt >= stack:
                    return Action(ActionType.ALL_IN, stack, is_all_in=True)
                return Action(ActionType.BET, amt)
            else:
                raise_total = to_call + amt
                current_bet = state_dict.get("current_bet", 0)
                if raise_total >= stack + current_bet:
                    return Action(ActionType.ALL_IN, stack, is_all_in=True)
                return Action(ActionType.RAISE, raise_total - current_bet)
        return Action(ActionType.CHECK)

    def play_hand(self, game_engine: GameEngine, player_id: int) -> GameState:
        engine = game_engine
        state = engine.state

        while not state.hand_over:
            if state.current_player != player_id:
                break

            player = state.players[player_id]
            state_dict = {
                "player_id": player_id,
                "hole_cards": [c.id for c in player.hole_cards],
                "board_cards": [c.id for c in state.board],
                "pot": state.pot,
                "stack": player.stack,
                "current_bet": player.current_bet,
                "to_call": state.current_bet - player.current_bet,
                "street": state.street.name,
                "position": (player_id - state.button_position) % len(state.players),
                "num_players": len(state.players),
                "num_active": sum(1 for p in state.players if not p.folded and p.is_active),
                "starting_stack": engine.config.starting_stack,
                "big_blind": engine.config.big_blind,
                "action_history": [
                    {"action": a.action_type.name, "amount": a.amount}
                    for _, a in state.action_history[-20:]
                ],
            }

            hole_cards = [c.id for c in player.hole_cards]
            board_cards = [c.id for c in state.board]

            action_idx, strategy = self.get_action(hole_cards, board_cards, state_dict)
            action = self._discrete_to_action(
                action_idx, state_dict, state_dict["to_call"], player.stack
            )

            engine.step(action)
            state = engine.state

        return engine.state


def load_agent(checkpoint_path: str, device: str = "cuda") -> CFRInferenceAgent:
    return CFRInferenceAgent(checkpoint_path, device=device)
