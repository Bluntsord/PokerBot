from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from pathlib import Path


@dataclass
class GameConfig:
    num_players: int = 2
    starting_stack: int = 200
    small_blind: int = 1
    big_blind: int = 2
    ante: int = 0


@dataclass
class ModelConfig:
    card_embed_dim: int = 64
    action_embed_dim: int = 16
    hidden_dim: int = 512
    num_layers: int = 6
    dropout: float = 0.1
    use_layer_norm: bool = True
    use_residual: bool = True
    grad_clip_norm: float = 5.0


@dataclass
class TrainingConfig:
    game: GameConfig = field(default_factory=GameConfig)
    model: ModelConfig = field(default_factory=ModelConfig)

    num_iterations: int = 1000
    traversals_per_iteration: int = 5000
    batch_size: int = 512
    buffer_capacity: int = 2_000_000

    value_net_lr: float = 1e-4
    value_net_weight_decay: float = 1e-5
    value_net_epochs_per_iter: int = 4

    regret_discount: float = 0.5

    device: str = "cuda"
    use_amp: bool = True
    num_workers: int = 4

    checkpoint_dir: str = "checkpoints"
    log_interval: int = 10
    eval_interval: int = 50
    save_interval: int = 50

    exploitability_eval_hands: int = 10000

    resume_from: Optional[str] = None
    wandb_project: Optional[str] = None
    wandb_entity: Optional[str] = None

    action_space_bet_fractions: List[float] = field(default_factory=lambda: [0.5, 0.75, 1.0, 1.5])

    def __post_init__(self):
        Path(self.checkpoint_dir).mkdir(parents=True, exist_ok=True)


NUM_ACTIONS = 6

ACTION_FOLD = 0
ACTION_CHECK_CALL = 1
ACTION_BET_05 = 2
ACTION_BET_075 = 3
ACTION_BET_10 = 4
ACTION_BET_15 = 5
ACTION_ALL_IN = -1

ACTION_NAMES = {
    ACTION_FOLD: "fold",
    ACTION_CHECK_CALL: "check/call",
    ACTION_BET_05: "bet 0.5x",
    ACTION_BET_075: "bet 0.75x",
    ACTION_BET_10: "bet 1.0x",
    ACTION_BET_15: "bet 1.5x",
}

AVAILABLE_ACTIONS = [ACTION_FOLD, ACTION_CHECK_CALL, ACTION_BET_05, ACTION_BET_075, ACTION_BET_10, ACTION_BET_15]

NUM_CARDS = 52
NUM_RANKS = 13
NUM_SUITS = 4
NUM_STREETS = 4
MAX_PLAYERS = 6
