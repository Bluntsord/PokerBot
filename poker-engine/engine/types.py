from __future__ import annotations
from enum import IntEnum, auto
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import random

RANKS = "23456789TJQKA"
SUITS = "cdhs"
RANK_TO_INT = {r: i for i, r in enumerate(RANKS)}
SUIT_TO_INT = {s: i for i, s in enumerate(SUITS)}


class Street(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4


class ActionType(IntEnum):
    FOLD = 0
    CHECK = 1
    CALL = 2
    BET = 3
    RAISE = 4
    ALL_IN = 5


class HandRank(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


HAND_RANK_NAMES = {
    HandRank.HIGH_CARD: "High Card",
    HandRank.ONE_PAIR: "One Pair",
    HandRank.TWO_PAIR: "Two Pair",
    HandRank.THREE_OF_A_KIND: "Three of a Kind",
    HandRank.STRAIGHT: "Straight",
    HandRank.FLUSH: "Flush",
    HandRank.FULL_HOUSE: "Full House",
    HandRank.FOUR_OF_A_KIND: "Four of a Kind",
    HandRank.STRAIGHT_FLUSH: "Straight Flush",
    HandRank.ROYAL_FLUSH: "Royal Flush",
}


@dataclass
class Card:
    id: int

    def __init__(self, identifier: int | str):
        if isinstance(identifier, int):
            if not 0 <= identifier < 52:
                raise ValueError(f"Card id must be 0-51, got {identifier}")
            self.id = identifier
        elif len(identifier) == 2:
            rank = RANK_TO_INT.get(identifier[0].upper())
            suit = SUIT_TO_INT.get(identifier[1].lower())
            if rank is None or suit is None:
                raise ValueError(f"Invalid card string: {identifier}")
            self.id = rank + 13 * suit
        else:
            raise ValueError(f"Invalid card: {identifier}")

    @property
    def rank(self) -> int:
        return self.id % 13

    @property
    def suit(self) -> int:
        return self.id // 13

    @property
    def rank_char(self) -> str:
        return RANKS[self.rank]

    @property
    def suit_char(self) -> str:
        return SUITS[self.suit]

    def __repr__(self) -> str:
        return f"Card('{self.rank_char}{self.suit_char}')"

    def __str__(self) -> str:
        return f"{self.rank_char}{self.suit_char}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def __lt__(self, other) -> bool:
        return self.id < other.id


ALL_CARDS = [Card(i) for i in range(52)]


@dataclass
class Action:
    action_type: ActionType
    amount: int = 0
    is_all_in: bool = False

    def __repr__(self) -> str:
        name = self.action_type.name
        if self.action_type in (ActionType.BET, ActionType.RAISE):
            return f"Action({name} {self.amount})"
        if self.action_type == ActionType.ALL_IN:
            return f"Action(ALL_IN {self.amount})"
        return f"Action({name})"


@dataclass
class PlayerState:
    player_id: int
    stack: int
    hole_cards: List[Card]
    current_bet: int = 0
    total_bet: int = 0
    folded: bool = False
    is_all_in: bool = False
    is_active: bool = True
    last_action: Optional[Action] = None

    def can_act(self) -> bool:
        return not self.folded and self.is_active and not self.is_all_in

    def bet_amount(self, amount: int):
        diff = amount - self.current_bet
        self.stack -= diff
        self.current_bet = amount
        self.total_bet += diff
        if self.stack == 0:
            self.is_all_in = True

    def reset_for_street(self):
        self.current_bet = 0

    def __repr__(self) -> str:
        cards = " ".join(str(c) for c in self.hole_cards)
        return (
            f"Player[{self.player_id}](stack={self.stack}, bet={self.current_bet}, "
            f"folded={self.folded}, all_in={self.is_all_in}, cards=[{cards}])"
        )
