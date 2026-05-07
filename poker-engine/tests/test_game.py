import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.game import GameEngine, GameConfig, GameState
from engine.types import Action, ActionType, Card, Street, PlayerState
from engine.evaluator import ensure_initialized


class TestGameEngine:
    def test_basic_setup(self):
        config = GameConfig(num_players=6, starting_stack=1000, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()

        assert len(state.players) == 6
        assert state.street == Street.PREFLOP
        assert state.current_bet == 10
        assert state.hand_number == 1

        for player in state.players:
            assert len(player.hole_cards) == 2
            assert player.stack in (990, 995, 1000)

    def test_heads_up_setup(self):
        config = GameConfig(num_players=2, starting_stack=500, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()

        assert len(state.players) == 2
        assert state.current_player == state.sb_position

    def test_preflop_folds_to_one_player(self):
        config = GameConfig(num_players=3, starting_stack=1000, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()

        while not state.hand_over:
            state = engine.step(Action(ActionType.FOLD))

        assert state.hand_over
        assert state.street == Street.SHOWDOWN
        assert len(state.winners) == 1

    def test_preflop_all_in(self):
        config = GameConfig(num_players=2, starting_stack=100, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()

        current = state.current_player
        state = engine.step(Action(ActionType.ALL_IN, state.players[current].stack, is_all_in=True))

        while not state.hand_over:
            legal = state.get_legal_actions()
            call_or_allin = [a for a in legal if a.action_type in (ActionType.CALL, ActionType.ALL_IN)]
            if call_or_allin:
                state = engine.step(call_or_allin[0])
            else:
                break

        assert state.hand_over

    def test_side_pots(self):
        config = GameConfig(num_players=3, starting_stack=100, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()

        while not state.hand_over:
            legal = state.get_legal_actions()
            allin_actions = [a for a in legal if a.action_type == ActionType.ALL_IN]
            if allin_actions:
                state = engine.step(allin_actions[0])
            else:
                call_actions = [a for a in legal if a.action_type == ActionType.CALL]
                if call_actions:
                    state = engine.step(call_actions[0])
                else:
                    state = engine.step(legal[0])

        assert state.hand_over

    def test_button_rotation(self):
        config = GameConfig(num_players=6, starting_stack=1000, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        s1 = engine.reset()
        btn1 = s1.button_position
        engine.advance_button()
        s2 = engine.reset()
        btn2 = s2.button_position
        assert btn2 == (btn1 + 1) % 6

    def test_get_state_vector(self):
        config = GameConfig(num_players=2, starting_stack=500, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        engine.reset()

        sv = engine.get_state_vector(0)
        assert sv["player_id"] == 0
        assert len(sv["hole_cards"]) == 2
        assert sv["hand_number"] == 1

    def test_button_rotation(self):
        config = GameConfig(num_players=6, starting_stack=1000, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()
        btn1 = state.button_position
        engine.advance_button()
        state = engine.reset()
        btn2 = state.button_position
        assert btn2 == (btn1 + 1) % 6

    def test_side_pots(self):
        config = GameConfig(num_players=3, starting_stack=100, small_blind=5, big_blind=10)
        engine = GameEngine(config)
        state = engine.reset()

        current = state.current_player
        state = engine.step(Action(ActionType.ALL_IN, state.players[current].stack, is_all_in=True))

        current = state.current_player
        state = engine.step(Action(ActionType.ALL_IN, state.players[current].stack, is_all_in=True))

        current = state.current_player
        state = engine.step(Action(ActionType.CALL, state.current_bet))

        assert state.hand_over

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
    print("Testing Game Engine...")
    tester = TestGameEngine()
    success = tester.run_all()
    sys.exit(0 if success else 1)
