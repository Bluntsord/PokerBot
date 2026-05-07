import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.evaluator import evaluate, evaluate_str, compare_hands, get_equity, ensure_initialized
from engine.types import Card, HandRank


class TestHandEvaluator:
    def test_royal_flush(self):
        cards = [Card("Ac"), Card("Kc"), Card("Qc"), Card("Jc"), Card("Tc")]
        rank = evaluate(cards)
        assert rank == 1, f"Royal flush should be rank 1, got {rank}"

    def test_straight_flush(self):
        cards = [Card("9d"), Card("8d"), Card("7d"), Card("6d"), Card("5d")]
        rank = evaluate(cards)
        assert 2 <= rank <= 20, f"Nine-high straight flush should be rank 2-20, got {rank}"

    def test_wheel_straight_flush(self):
        cards = [Card("Ah"), Card("2h"), Card("3h"), Card("4h"), Card("5h")]
        rank = evaluate(cards)
        assert 2 <= rank <= 20, f"Wheel straight flush should be rank 2-20, got {rank}"

    def test_four_of_a_kind(self):
        cards = [Card("Ac"), Card("Ad"), Card("Ah"), Card("As"), Card("Kc")]
        rank = evaluate(cards)
        assert 10 <= rank <= 200, f"Quads should be low rank, got {rank}"

    def test_full_house(self):
        cards = [Card("Ac"), Card("Ad"), Card("Ah"), Card("Kc"), Card("Kd")]
        rank = evaluate(cards)
        assert 200 <= rank <= 700, f"Full house should be rank 200-700, got {rank}"

    def test_flush(self):
        cards = [Card("Ac"), Card("Jc"), Card("8c"), Card("6c"), Card("2c")]
        rank = evaluate(cards)
        assert 200 <= rank <= 2000, f"Flush should be rank 200-2000, got {rank}"

    def test_straight(self):
        cards = [Card("9c"), Card("8d"), Card("7h"), Card("6s"), Card("5c")]
        rank = evaluate(cards)
        assert 200 <= rank <= 3000, f"Straight should be rank 200-3000, got {rank}"

    def test_wheel_straight(self):
        cards = [Card("Ac"), Card("2d"), Card("3h"), Card("4s"), Card("5c")]
        rank = evaluate(cards)
        assert 200 <= rank <= 3000, f"Wheel straight should be rank 200-3000, got {rank}"

    def test_trips(self):
        cards = [Card("Ac"), Card("Ad"), Card("Ah"), Card("Kc"), Card("Qd")]
        rank = evaluate(cards)
        assert 2000 <= rank <= 4000, f"Trips should be rank 2000-4000, got {rank}"

    def test_two_pair(self):
        cards = [Card("Ac"), Card("Ad"), Card("Kc"), Card("Kd"), Card("Qc")]
        rank = evaluate(cards)
        assert 2000 <= rank <= 5500, f"Two pair should be rank 2000-5500, got {rank}"

    def test_one_pair(self):
        cards = [Card("Ac"), Card("Ad"), Card("Kc"), Card("Qd"), Card("Jc")]
        rank = evaluate(cards)
        assert 3000 <= rank <= 7500, f"One pair should be rank 3000-7500, got {rank}"

    def test_high_card(self):
        cards = [Card("Ac"), Card("Kd"), Card("Qc"), Card("Jd"), Card("9c")]
        rank = evaluate(cards)
        assert rank >= 3, f"High card should have very high rank, got {rank}"

    def test_relative_ordering(self):
        sf = evaluate_str("9d 8d 7d 6d 5d")
        quads = evaluate_str("Ac Ad Ah As Kc")
        fh = evaluate_str("Ac Ad Ah Kc Kd")
        flush = evaluate_str("Ac Jc 8c 6c 2c")
        straight = evaluate_str("9c 8d 7h 6s 5c")
        trips = evaluate_str("Ac Ad Ah Kc Qd")
        two_pair = evaluate_str("Ac Ad Kc Kd Qc")
        one_pair = evaluate_str("Ac Ad Kc Qd Jc")
        high = evaluate_str("Ac Kd Qc Jd 9c")

        assert sf < quads < fh < flush < straight < trips < two_pair < one_pair < high, (
            f"Ordering wrong: sf={sf}, q={quads}, fh={fh}, fl={flush}, "
            f"st={straight}, tr={trips}, tp={two_pair}, op={one_pair}, hc={high}"
        )

    def test_seven_card(self):
        cards = [Card("Ac"), Card("Kc"), Card("Qc"), Card("Jc"), Card("Tc"), Card("2d"), Card("3h")]
        rank = evaluate(cards)
        assert rank == 1, f"7-card should find royal flush, got {rank}"

    def test_seven_card_pair(self):
        cards = [Card("Ac"), Card("Ad"), Card("2c"), Card("3d"), Card("4h"), Card("5s"), Card("6c")]
        rank = evaluate(cards)
        assert 3 <= rank <= 7462, f"7-card should evaluate, got {rank}"

    def test_compare_hands(self):
        hand1 = [Card("Ac"), Card("Ad"), Card("Ah"), Card("As"), Card("Kc")]
        hand2 = [Card("Kc"), Card("Kd"), Card("Kh"), Card("Ks"), Card("Qc")]
        assert compare_hands(hand1, hand2) == 1, "Aces quads should beat kings quads"

        hand3 = [Card("Ac"), Card("Ad")]
        board = [Card("Qc"), Card("Qd"), Card("3h"), Card("2s"), Card("3c")]
        r3 = compare_hands(hand3 + board, [Card("Kc"), Card("Jc"), Card("Qc"), Card("Qd"), Card("3h")])
        assert r3 == 1, f"AA on QQ33x beats single pair, got {r3}"

    def test_equity_calculation(self):
        hole = [Card("Ac"), Card("Ad")]
        equity = get_equity(hole, [], num_opponents=1, trials=2000)
        assert 0.7 < equity < 0.9, f"AA vs random should be ~85%, got {equity:.2%}"

        hole2 = [Card("2c"), Card("7d")]
        equity2 = get_equity(hole2, [], num_opponents=1, trials=2000)
        assert 0.25 < equity2 < 0.55, f"72o vs random should be ~35%, got {equity2:.2%}"

    def test_full_house(self):
        cards = [Card("Ac"), Card("Ad"), Card("Ah"), Card("Kc"), Card("Kd")]
        rank = evaluate(cards)
        assert 100 <= rank <= 500, f"Full house should be rank 100-500, got {rank}"

    def test_trips(self):
        cards = [Card("Ac"), Card("Ad"), Card("Ah"), Card("Kc"), Card("Qd")]
        rank = evaluate(cards)
        assert 1000 <= rank <= 2500, f"Trips should be rank 1000-2500, got {rank}"

    def test_evaluate_str(self):
        assert evaluate_str("Ac Kc Qc Jc Tc") == 1
        wheel_sf = evaluate_str("Ah 2h 3h 4h 5h")
        assert 2 <= wheel_sf <= 20, f"Wheel SF should be 2-20, got {wheel_sf}"
        assert evaluate_str("2s 3h 4d 5c 7s") > 4000

    def test_card_creation(self):
        c1 = Card(0)
        c2 = Card("2c")
        assert c1 == c2
        assert str(c1) == "2c"

        c3 = Card(51)
        c4 = Card("As")
        assert c3 == c4
        assert str(c3) == "As"

    def test_all_cards_unique(self):
        all_cards = [Card(i) for i in range(52)]
        assert len(set(c.id for c in all_cards)) == 52

    def test_ranks_and_suits(self):
        c = Card("Ah")
        assert c.rank == 12
        assert c.suit == 2
        assert c.rank_char == "A"
        assert c.suit_char == "h"

        c2 = Card("2c")
        assert c2.rank == 0
        assert c2.suit == 0

    def run_all(self):
        tests = [
            m for m in dir(self)
            if m.startswith("test_") and callable(getattr(self, m))
        ]
        passed = 0
        failed = 0
        for test_name in tests:
            try:
                getattr(self, test_name)()
                print(f"  ✓ {test_name}")
                passed += 1
            except Exception as e:
                print(f"  ✗ {test_name}: {e}")
                failed += 1
        print(f"\n  {passed} passed, {failed} failed")
        return failed == 0


if __name__ == "__main__":
    ensure_initialized()
    print("Testing Hand Evaluator...")
    tester = TestHandEvaluator()
    success = tester.run_all()

    print("\nRunning game engine tests...")
    from test_game import TestGameEngine

    game_tester = TestGameEngine()
    success = game_tester.run_all() and success

    sys.exit(0 if success else 1)
