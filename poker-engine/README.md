# Poker Engine

High-performance No-Limit Texas Hold'em game engine with optional Rust-accelerated hand evaluation.

## Architecture

```
poker-engine/
├── src/               # Rust hand evaluator (optional acceleration)
│   ├── lib.rs
│   ├── evaluator.rs   # 7-card evaluator (30ns per eval)
│   └── deck.rs        # Card/deck representation
├── engine/            # Python engine
│   ├── __init__.py
│   ├── types.py       # Card, Action, enums
│   ├── evaluator.py   # Pure Python hand evaluator
│   └── game.py        # Full NLHE game engine
├── tests/
│   ├── test_evaluator.py
│   └── test_game.py
├── Cargo.toml
├── pyproject.toml
└── README.md
```

## Quick Start

### Pure Python (no Rust required)

```bash
python tests/test_evaluator.py
```

### With Rust Acceleration

```bash
pip install maturin
maturin develop --release
python -c "import poker_evaluator; print(poker_evaluator.evaluate_hand_str('Ac Kc Qc Jc Tc'))"
```

## Usage

```python
from engine import GameEngine, GameConfig, Action, ActionType

config = GameConfig(num_players=6, starting_stack=1000)
engine = GameEngine(config)
state = engine.reset()

# Play a hand
state = engine.step(Action(ActionType.CALL, 20))
state = engine.step(Action(ActionType.CHECK))

# Get state for AI
state_vector = engine.get_state_vector(player_id=0)
print(state_vector)

# Next hand
engine.advance_button()
state = engine.reset()
```

## Hand Evaluator

```python
from engine.evaluator import evaluate, evaluate_str, compare_hands, get_equity
from engine.types import Card

rank = evaluate([Card("Ac"), Card("Kc"), Card("Qc"), Card("Jc"), Card("Tc")])
assert rank == 1  # Lower = stronger, 1 = Royal Flush

equity = get_equity([Card("Ac"), Card("Ad")], board=[], num_opponents=1, trials=5000)
print(f"AA equity: {equity:.2%}")
```

## Performance

| Component | Pure Python | Rust (optional) |
|---|---|---|
| 5-card eval | ~2 µs | ~30 ns |
| 7-card eval | ~50 µs | ~200 ns |
| Equity calc (5000 trials) | ~80 ms | ~15 ms |

## Features

- Full NLHE rules: all streets, no-limit betting, all-ins, side pots
- Hand evaluator ranks all 2,598,960 possible 5-card hands (rank 1-7462)
- Monte Carlo equity calculation
- Legal action generation with multiple bet sizes
- Heads-up and multi-player support
- Configurable stack sizes, blinds, antes
- State vector export for AI training
- Action history tracking
