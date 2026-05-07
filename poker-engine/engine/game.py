from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import random

from engine.types import (
    Card, Action, PlayerState, Street, ActionType, ALL_CARDS,
)
from engine.evaluator import evaluate, compare_hands, evaluate_str, HAND_RANK_TABLE


@dataclass
class GameConfig:
    num_players: int = 6
    starting_stack: int = 10000
    small_blind: int = 10
    big_blind: int = 20
    ante: int = 0
    min_bet: int = 20


@dataclass
class GameState:
    config: GameConfig
    players: List[PlayerState] = field(default_factory=list)
    deck: List[Card] = field(default_factory=list)
    board: List[Card] = field(default_factory=list)
    pot: int = 0
    street: Street = Street.PREFLOP
    current_bet: int = 0
    min_raise: int = 0
    last_raise_size: int = 0
    current_player: int = 0
    action_history: List[Tuple[int, Action]] = field(default_factory=list)
    hand_over: bool = False
    winners: List[Tuple[int, int, str]] = field(default_factory=list)
    button_position: int = 0
    hand_number: int = 0

    @property
    def active_players(self) -> List[PlayerState]:
        return [p for p in self.players if not p.folded and p.is_active]

    @property
    def num_active(self) -> int:
        return sum(1 for p in self.players if not p.folded and p.is_active)

    @property
    def num_to_act(self) -> int:
        return sum(1 for p in self.players if p.can_act())

    @property
    def current_player_state(self) -> Optional[PlayerState]:
        if 0 <= self.current_player < len(self.players):
            return self.players[self.current_player]
        return None

    @property
    def sb_position(self) -> int:
        if self.config.num_players == 2:
            return self.button_position
        return (self.button_position + 1) % self.config.num_players

    @property
    def bb_position(self) -> int:
        if self.config.num_players == 2:
            return (self.button_position + 1) % self.config.num_players
        return (self.button_position + 2) % self.config.num_players

    def get_legal_actions(self) -> List[Action]:
        player = self.current_player_state
        if player is None or not player.can_act():
            return []

        actions = []
        call_amount = self.current_bet - player.current_bet
        is_preflop = self.street == Street.PREFLOP

        if call_amount == 0:
            actions.append(Action(ActionType.CHECK))
        else:
            actions.append(Action(ActionType.FOLD))
            if call_amount >= player.stack:
                actions.append(Action(ActionType.ALL_IN, player.stack, is_all_in=True))
            else:
                actions.append(Action(ActionType.CALL, call_amount))

        if self.current_bet == 0:
            if is_preflop and self.config.big_blind < player.stack:
                actions.append(Action(ActionType.BET, self.config.big_blind))
            elif not is_preflop and self.config.big_blind < player.stack:
                actions.append(Action(ActionType.BET, self.config.big_blind))

            for frac in [0.5, 0.66, 0.75, 1.0, 1.5, 2.0, 3.0]:
                pot_size = self.pot + sum(p.current_bet for p in self.players)
                bet_amt = int(pot_size * frac)
                if self.config.big_blind <= bet_amt < player.stack:
                    actions.append(Action(ActionType.BET, bet_amt))

        elif self.current_bet > 0 and call_amount < player.stack:
            min_raise_to = self.current_bet + max(self.min_raise, self.last_raise_size)
            if is_preflop and min_raise_to < player.stack:
                min_raise_to = max(min_raise_to, self.current_bet + self.config.big_blind)

            raise_amount = min_raise_to - player.current_bet
            if raise_amount < player.stack:
                for mult in [1.0, 2.0, 2.5, 3.0, 4.0]:
                    ra = int(raise_amount * mult)
                    if raise_amount <= ra < player.stack:
                        actual_total = player.current_bet + ra
                        if actual_total > self.current_bet:
                            actions.append(Action(ActionType.RAISE, ra))

        if player.stack > 0:
            actions.append(Action(ActionType.ALL_IN, player.stack, is_all_in=True))

        seen = {}
        unique = []
        for a in actions:
            key = (a.action_type, a.amount, a.is_all_in)
            if key not in seen:
                seen[key] = True
                unique.append(a)
        return unique

    def apply_action(self, action: Action):
        player = self.current_player_state
        if player is None:
            return

        self.action_history.append((self.current_player, action))
        player.last_action = action

        if action.action_type == ActionType.FOLD:
            player.folded = True
        elif action.action_type == ActionType.CHECK:
            pass
        elif action.action_type == ActionType.CALL:
            call_amount = self.current_bet - player.current_bet
            player.bet_amount(player.current_bet + call_amount)
        elif action.action_type == ActionType.BET:
            self.last_raise_size = action.amount
            self.min_raise = action.amount
            player.bet_amount(player.current_bet + action.amount)
            self.current_bet = player.current_bet
        elif action.action_type == ActionType.RAISE:
            self.last_raise_size = action.amount
            self.min_raise = action.amount
            player.bet_amount(player.current_bet + action.amount)
            self.current_bet = player.current_bet
        elif action.action_type == ActionType.ALL_IN:
            bet_amount = player.stack + player.current_bet
            player.bet_amount(bet_amount)
            if bet_amount > self.current_bet:
                self.last_raise_size = bet_amount - self.current_bet
                self.min_raise = self.last_raise_size
                self.current_bet = bet_amount

        self._advance_player()

    def _advance_player(self):
        active_acted = [p for p in self.players
                        if p.is_active and not p.folded and not p.is_all_in]
        if len(active_acted) == 0:
            self._advance_street()
            return

        if self._street_complete():
            self._advance_street()
            return

        next_p = self._find_next_actor()
        if next_p is not None:
            self.current_player = next_p
        else:
            self._advance_street()

    def _find_next_actor(self) -> int | None:
        for i in range(1, self.config.num_players + 1):
            pid = (self.current_player + i) % self.config.num_players
            p = self.players[pid]
            if p.can_act():
                return pid
        return None

    def _street_complete(self) -> bool:
        for p in self.players:
            if not p.is_active or p.folded:
                continue
            if p.is_all_in:
                continue
            if p.current_bet != self.current_bet:
                return False
        return True

    def _street_ready(self) -> bool:
        active = [p for p in self.players if not p.folded and p.is_active]
        if len(active) <= 1:
            return True
        for p in active:
            if p.can_act() and p.current_bet != self.current_bet:
                return False
        return True

    def _advance_street(self):
        self._collect_bets()
        for p in self.players:
            p.reset_for_street()
        self.current_bet = 0
        self.last_raise_size = 0
        self.min_raise = self.config.big_blind

        active = [p for p in self.players if not p.folded and p.is_active]
        if len(active) <= 1:
            self._run_showdown()
            return

        all_allin = all(p.is_all_in for p in active)
        if all_allin and self.street != Street.RIVER:
            while self.street != Street.RIVER:
                if self.street == Street.PREFLOP:
                    self.street = Street.FLOP
                    self.board.extend(self._deal_cards(3))
                elif self.street == Street.FLOP:
                    self.street = Street.TURN
                    self.board.append(self._deal_cards(1)[0])
                elif self.street == Street.TURN:
                    self.street = Street.RIVER
                    self.board.append(self._deal_cards(1)[0])
            self._run_showdown()
            return

        if self.street == Street.RIVER:
            self._run_showdown()
            return

        if self.street == Street.PREFLOP:
            self.street = Street.FLOP
            self.board.extend(self._deal_cards(3))
        elif self.street == Street.FLOP:
            self.street = Street.TURN
            self.board.append(self._deal_cards(1)[0])
        elif self.street == Street.TURN:
            self.street = Street.RIVER
            self.board.append(self._deal_cards(1)[0])

        self.current_player = self.button_position
        self._skip_inactive_players()
        self._skip_inactive_players()
        if self.config.num_players > 2:
            self._skip_inactive_players()

        if self.num_active == 2:
            sb = self.players[self.sb_position]
            bb = self.players[self.bb_position]
            if bb.can_act() and not bb.folded:
                self.current_player = self.bb_position
            elif sb.can_act() and not sb.folded:
                self.current_player = self.sb_position
            else:
                self.current_player = self.button_position

    def _skip_inactive_players(self):
        for _ in range(self.config.num_players):
            self.current_player = (self.current_player + 1) % self.config.num_players
            p = self.current_player_state
            if p and p.can_act() and not p.folded:
                return

    def _collect_bets(self):
        for p in self.players:
            self.pot += p.current_bet
            p.current_bet = 0

    def _run_showdown(self):
        self._collect_bets()
        self.street = Street.SHOWDOWN
        self.hand_over = True

        active = [p for p in self.players if not p.folded and p.is_active]
        if len(active) == 1:
            winner = active[0]
            winner.stack += self.pot
            self.winners = [(winner.player_id, self.pot, "fold")]
            self.pot = 0
            return

        best_rank = 7463
        best_players = []
        player_hands = []

        for p in active:
            seven = p.hole_cards + self.board
            rank = evaluate(seven)
            player_hands.append((p.player_id, rank))
            if rank < best_rank:
                best_rank = rank
                best_players = [p]
            elif rank == best_rank:
                best_players.append(p)

        chips_per_winner = self.pot // len(best_players)
        remainder = self.pot % len(best_players)

        for p in best_players:
            p.stack += chips_per_winner
        if remainder and best_players:
            best_players[0].stack += remainder

        self.winners = [(p.player_id, chips_per_winner, "win") for p in best_players]
        self.pot = 0

    def _deal_cards(self, count: int) -> List[Card]:
        cards = self.deck[:count]
        self.deck = self.deck[count:]
        return cards


class GameEngine:
    def __init__(self, config: GameConfig):
        self.config = config
        self.state = GameState(config=config)

    def reset(self, seed: Optional[int] = None) -> GameState:
        if seed is not None:
            random.seed(seed)

        deck = list(ALL_CARDS)
        random.shuffle(deck)

        old_button = self.state.button_position if hasattr(self, 'state') and self.state else 0

        self.state = GameState(
            config=self.config,
            deck=deck,
            button_position=old_button if old_button else 0,
        )
        s = self.state

        for i in range(self.config.num_players):
            cards = [s._deal_cards(1)[0], s._deal_cards(1)[0]]
            player = PlayerState(
                player_id=i,
                stack=self.config.starting_stack,
                hole_cards=cards,
            )
            s.players.append(player)

        s.current_bet = self.config.big_blind
        s.min_raise = self.config.big_blind
        s.current_player = s.button_position
        s.hand_number += 1

        if self.config.num_players == 2:
            sb_player = s.players[s.sb_position]
            sb_amount = min(self.config.small_blind, sb_player.stack)
            sb_player.bet_amount(sb_amount)
            s.current_bet = max(s.current_bet, sb_player.current_bet)

            bb_player = s.players[s.bb_position]
            bb_amount = min(self.config.big_blind, bb_player.stack)
            bb_player.bet_amount(bb_amount)
            s.current_bet = max(s.current_bet, bb_player.current_bet)

            s.current_player = s.sb_position
        else:
            sb_pos = s.sb_position
            bb_pos = s.bb_position

            sb_player = s.players[sb_pos]
            sb_amount = min(self.config.small_blind, sb_player.stack)
            sb_player.bet_amount(sb_amount)

            bb_player = s.players[bb_pos]
            bb_amount = min(self.config.big_blind, bb_player.stack)
            bb_player.bet_amount(bb_amount)
            s.current_bet = bb_amount

            utg = (bb_pos + 1) % self.config.num_players
            s.current_player = utg

        if self.config.ante > 0:
            for p in s.players:
                ante_amt = min(self.config.ante, p.stack)
                p.bet_amount(p.current_bet + ante_amt)
                s.pot += ante_amt
                p.current_bet -= ante_amt

        return s

    def step(self, action: Action) -> GameState:
        self.state.apply_action(action)
        return self.state

    def advance_button(self):
        self.state.button_position = (self.state.button_position + 1) % self.config.num_players
        eliminated = [p for p in self.state.players if p.stack == 0]
        while self.state.players[self.state.button_position] in eliminated:
            self.state.button_position = (self.state.button_position + 1) % self.config.num_players

    def get_state_vector(self, player_id: int) -> dict:
        s = self.state
        player = s.players[player_id]
        return {
            "player_id": player_id,
            "hole_cards": [str(c) for c in player.hole_cards],
            "board": [str(c) for c in s.board],
            "pot": s.pot,
            "stack": player.stack,
            "current_bet": player.current_bet,
            "total_bet": player.total_bet,
            "to_call": s.current_bet - player.current_bet,
            "street": s.street.name,
            "position": (player_id - s.button_position) % s.config.num_players,
            "is_my_turn": player_id == s.current_player,
            "folded": player.folded,
            "is_all_in": player.is_all_in,
            "legal_actions": [
                {"type": a.action_type.name, "amount": a.amount}
                for a in s.get_legal_actions()
            ] if player_id == s.current_player else [],
            "hand_number": s.hand_number,
            "num_active": s.num_active,
            "action_history": [
                {"player": pid, "action": act.action_type.name, "amount": act.amount}
                for pid, act in s.action_history[-20:]
            ],
        }
