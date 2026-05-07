#!/usr/bin/env python3
import sys
import os
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.game import GameEngine, GameConfig
from engine.types import Action, ActionType, Card, Street
from train.inference import CFRInferenceAgent


def play_interactive(checkpoint_path: str, device: str = "cuda"):
    agent = CFRInferenceAgent(checkpoint_path, device=device)

    game_cfg = GameConfig(num_players=2, starting_stack=200, small_blind=1, big_blind=2)
    engine = GameEngine(game_cfg)
    state = engine.reset()

    print("\n" + "=" * 60)
    print("  Poker AI - Interactive Play")
    print("=" * 60)
    print(f"  You vs AI | 200 BB deep | 1/2 blinds")
    print(f"  Actions: f=fold, c=check/call, bX=bet X, rX=raise to X, a=all-in")
    print("=" * 60)

    while True:
        state = engine.reset()
        engine.advance_button()

        while not state.hand_over:
            _display_state(state)

            current = state.current_player
            player = state.players[current]

            if current == 0:
                action = _get_human_action(state, player)
            else:
                state_dict = _make_state_dict(engine, current)
                hole = [c.id for c in player.hole_cards]
                board = [c.id for c in state.board]

                action_idx, strategy = agent.get_action(hole, board, state_dict)
                action = agent._discrete_to_action(
                    action_idx, state_dict, state_dict["to_call"], player.stack
                )
                print(f"\n  AI chooses: {action}")
                time.sleep(0.5)

            engine.step(action)
            state = engine.state

        _display_result(state)
        engine.advance_button()

        again = input("\nPlay another hand? [Y/n]: ").strip().lower()
        if again == "n":
            break


def _display_state(state):
    print(f"\n  --- Hand #{state.hand_number} | {state.street.name} ---")
    print(f"  Board: {' '.join(str(c) for c in state.board) if state.board else '(none)'}")
    print(f"  Pot: {state.pot} | Your stack: {state.players[0].stack}")
    print(f"  Opponent stack: {state.players[1].stack}")
    if not state.hand_over:
        print(f"  Your cards: {' '.join(str(c) for c in state.players[0].hole_cards)}")


def _get_human_action(state, player):
    legal = state.get_legal_actions()
    print(f"\n  Legal actions: ")
    for i, a in enumerate(legal):
        print(f"    [{i}] {a}")

    while True:
        choice = input("  Your action: ").strip().lower()

        if choice == "f":
            for a in legal:
                if a.action_type == ActionType.FOLD:
                    return a
        elif choice == "c":
            for a in legal:
                if a.action_type in (ActionType.CHECK, ActionType.CALL):
                    return a
        elif choice == "a":
            for a in legal:
                if a.action_type == ActionType.ALL_IN:
                    return a
        elif choice.startswith("b"):
            try:
                amt = int(choice[1:])
                if amt <= player.stack:
                    return Action(ActionType.BET, amt)
            except ValueError:
                pass
        elif choice.startswith("r"):
            try:
                amt = int(choice[1:])
                if amt > state.current_bet:
                    return Action(ActionType.RAISE, amt - player.current_bet)
            except ValueError:
                pass

        print("  Invalid action. Try again.")


def _make_state_dict(engine, player_id):
    state = engine.state
    player = state.players[player_id]
    return {
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
        "opp_stack": state.players[1 - player_id].stack,
        "starting_stack": engine.config.starting_stack,
        "big_blind": engine.config.big_blind,
        "action_history": [
            {"action": a.action_type.name, "amount": a.amount}
            for _, a in state.action_history[-20:]
        ],
    }


def _display_result(state):
    print(f"\n  --- Result ---")
    for winner_id, chips, reason in state.winners:
        name = "You" if winner_id == 0 else "AI"
        cards = state.players[winner_id].hole_cards
        print(f"  {name} wins {chips} chips ({reason}) with {' '.join(str(c) for c in cards)}")


def main():
    parser = argparse.ArgumentParser(description="Play against trained poker AI")
    parser.add_argument("checkpoint", type=str, help="Path to model checkpoint")
    parser.add_argument("--device", type=str, default="cuda", help="Device (cuda/cpu)")
    args = parser.parse_args()

    play_interactive(args.checkpoint, args.device)


if __name__ == "__main__":
    main()
