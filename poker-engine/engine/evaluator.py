from __future__ import annotations
from typing import List, Tuple, Optional
from math import comb
import random

from engine.types import Card, HandRank, RANK_TO_INT, SUIT_TO_INT, RANKS

BINOMIAL_CACHE: List[List[int]] = []
HAND_RANK_TABLE: List[int] = []
_INITIALIZED = False


def _build_binomial_cache():
    global BINOMIAL_CACHE
    BINOMIAL_CACHE = [[0] * 6 for _ in range(53)]
    for n in range(53):
        for k in range(min(6, n + 1)):
            BINOMIAL_CACHE[n][k] = comb(n, k)


def _hand_index(cards: List[int]) -> int:
    sorted_cards = sorted(cards)
    index = 0
    for i, card in enumerate(sorted_cards):
        index += BINOMIAL_CACHE[card][i + 1]
    return index


def _evaluate_5_cards_basic(card_ids: List[int]) -> int:
    ranks = [c % 13 for c in card_ids]
    suits = [c // 13 for c in card_ids]
    is_flush = len(set(suits)) == 1
    rank_counts = [0] * 13
    for r in ranks:
        rank_counts[r] += 1

    sorted_ranks = sorted(ranks, reverse=True)
    is_straight = False
    straight_high = -1
    unique = sorted(set(ranks))
    if len(unique) == 5 and unique[-1] - unique[0] == 4:
        is_straight = True
        straight_high = unique[-1]
    if unique == [0, 1, 2, 3, 12]:
        is_straight = True
        straight_high = 3

    if is_flush and is_straight:
        if straight_high == 12:
            return _encode_score(HandRank.ROYAL_FLUSH, [])
        return _encode_score(HandRank.STRAIGHT_FLUSH, [straight_high])

    quads = [r for r in range(13) if rank_counts[r] == 4]
    if quads:
        kicker = [r for r in range(13) if rank_counts[r] == 1][0]
        return _encode_score(HandRank.FOUR_OF_A_KIND, [quads[0], kicker])

    trips = [r for r in range(13) if rank_counts[r] == 3]
    pairs = [r for r in range(13) if rank_counts[r] == 2]
    if trips and pairs:
        return _encode_score(HandRank.FULL_HOUSE, [trips[0], pairs[0]])

    if is_flush:
        return _encode_score(HandRank.FLUSH, sorted_ranks[:5])

    if is_straight:
        return _encode_score(HandRank.STRAIGHT, [straight_high])

    if trips:
        kickers = sorted([r for r in range(13) if rank_counts[r] == 1], reverse=True)
        return _encode_score(HandRank.THREE_OF_A_KIND, [trips[0]] + kickers[:2])

    if len(pairs) == 2:
        kicker = [r for r in range(13) if rank_counts[r] == 1][0]
        return _encode_score(HandRank.TWO_PAIR, sorted(pairs, reverse=True) + [kicker])

    if len(pairs) == 1:
        kickers = sorted([r for r in range(13) if rank_counts[r] == 1], reverse=True)
        return _encode_score(HandRank.ONE_PAIR, [pairs[0]] + kickers[:3])

    return _encode_score(HandRank.HIGH_CARD, sorted_ranks[:5])


def _encode_score(hand_rank: HandRank, kickers: List[int]) -> int:
    score = int(hand_rank) << 20
    for i, k in enumerate(kickers[:5]):
        score |= (k & 0xF) << (16 - i * 4)
    return score


def _decode_score(score: int) -> Tuple[HandRank, List[int]]:
    rank = HandRank((score >> 20) & 0xF)
    kickers = [(score >> (16 - i * 4)) & 0xF for i in range(5)]
    kickers = [k for k in kickers if k > 0 or i < 1 for i, _ in enumerate(kickers)]
    return rank, kickers[:5]


def _build_hand_rank_table():
    global HAND_RANK_TABLE
    total = comb(52, 5)
    HAND_RANK_TABLE = [0] * total
    raw_ranks = [0] * total

    indices = []
    for c0 in range(48):
        for c1 in range(c0 + 1, 49):
            for c2 in range(c1 + 1, 50):
                for c3 in range(c2 + 1, 51):
                    for c4 in range(c3 + 1, 52):
                        cards = [c0, c1, c2, c3, c4]
                        idx = _hand_index(cards)
                        score = _evaluate_5_cards_basic(cards)
                        raw_ranks[idx] = score
                        indices.append(idx)

    score_to_group: dict[int, list[int]] = {}
    for idx in indices:
        score = raw_ranks[idx]
        if score not in score_to_group:
            score_to_group[score] = []
        score_to_group[score].append(idx)

    sorted_scores = sorted(score_to_group.keys(), reverse=True)
    for rank, score in enumerate(sorted_scores):
        for idx in score_to_group[score]:
            HAND_RANK_TABLE[idx] = rank + 1


def ensure_initialized():
    global _INITIALIZED
    if not _INITIALIZED:
        _build_binomial_cache()
        _build_hand_rank_table()
        _INITIALIZED = True


def evaluate(cards: List[Card]) -> int:
    ensure_initialized()
    card_ids = [c.id for c in cards]
    n = len(card_ids)

    if n < 5:
        raise ValueError(f"Need at least 5 cards, got {n}")
    if n > 7:
        raise ValueError(f"Max 7 cards, got {n}")

    if n == 5:
        return HAND_RANK_TABLE[_hand_index(card_ids)]

    best = 7463
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    for e in range(d + 1, n):
                        sub = [card_ids[a], card_ids[b], card_ids[c], card_ids[d], card_ids[e]]
                        idx = _hand_index(sub)
                        rank = HAND_RANK_TABLE[idx]
                        if rank < best:
                            best = rank
    return best


def evaluate_str(cards_str: str) -> int:
    cards = [Card(s) for s in cards_str.split()]
    return evaluate(cards)


def get_hand_rank_info(rank: int) -> Tuple[HandRank, str]:
    ensure_initialized()
    if rank <= 0 or rank > 7462:
        raise ValueError(f"Invalid rank: {rank}")

    if rank == 1:
        return HandRank.ROYAL_FLUSH, "Royal Flush"

    for idx in range(len(HAND_RANK_TABLE)):
        if HAND_RANK_TABLE[idx] == rank:
            card_ids = _unrank_hand(idx)
            score = _evaluate_5_cards_basic(card_ids)
            hr, _ = _decode_score(score)

            from engine.types import HAND_RANK_NAMES

            name = HAND_RANK_NAMES.get(hr, "Unknown")
            if hr == HandRank.STRAIGHT_FLUSH and rank <= 10:
                name = "Straight Flush"
            return hr, name

    return HandRank.HIGH_CARD, "Unknown"


def _unrank_hand(idx: int) -> List[int]:
    cards = []
    for k in range(5, 0, -1):
        for n in range(51, -1, -1):
            if BINOMIAL_CACHE[n][k] <= idx:
                idx -= BINOMIAL_CACHE[n][k]
                cards.append(n)
                break
    return cards


def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
    r1 = evaluate(hand1)
    r2 = evaluate(hand2)
    if r1 < r2:
        return 1
    if r2 < r1:
        return -1
    return 0


def get_equity(hole_cards: List[Card], board_cards: List[Card], num_opponents: int = 1, trials: int = 5000) -> float:
    deck = [Card(i) for i in range(52) if Card(i) not in hole_cards and Card(i) not in board_cards]
    wins = 0
    needed = 5 - len(board_cards)

    for _ in range(trials):
        random.shuffle(deck)
        remaining_board = deck[:needed]
        opp_cards = deck[needed : needed + 2 * num_opponents]

        my_cards = hole_cards + board_cards + remaining_board
        my_rank = evaluate(my_cards)

        opp_ranks = []
        for o in range(num_opponents):
            opp_hand = list(opp_cards[o * 2 : o * 2 + 2]) + board_cards + remaining_board
            opp_ranks.append(evaluate(opp_hand))

        if my_rank < min(opp_ranks):
            wins += 1

    return wins / trials
