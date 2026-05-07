#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from train.config import TrainingConfig
from train.deep_cfr import DeepCFRTrainer


def main():
    parser = argparse.ArgumentParser(description="Train Deep CFR poker AI")
    parser.add_argument("--iterations", type=int, default=1000, help="Number of CFR iterations")
    parser.add_argument("--traversals", type=int, default=5000, help="Traversals per iteration")
    parser.add_argument("--batch-size", type=int, default=512, help="Batch size for training")
    parser.add_argument("--buffer-size", type=int, default=2000000, help="Replay buffer capacity")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--hidden-dim", type=int, default=512, help="Hidden layer dimension")
    parser.add_argument("--num-layers", type=int, default=6, help="Number of residual blocks")
    parser.add_argument("--device", type=str, default="cuda", help="Device (cuda/cpu)")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints", help="Checkpoint directory")
    parser.add_argument("--resume", type=str, default=None, help="Resume from checkpoint")
    parser.add_argument("--wandb", type=str, default=None, help="Wandb project name")
    parser.add_argument("--num-players", type=int, default=2, help="Number of players")
    parser.add_argument("--starting-stack", type=int, default=200, help="Starting stack in BB")
    parser.add_argument("--amp", action="store_true", default=True, help="Use mixed precision")
    parser.add_argument("--no-amp", action="store_false", dest="amp", help="Disable mixed precision")
    parser.add_argument("--epochs", type=int, default=4, help="Value net epochs per iteration")
    parser.add_argument("--eval-hands", type=int, default=1000, help="Hands for exploitability eval")
    parser.add_argument("--save-interval", type=int, default=50, help="Save checkpoint every N iters")
    parser.add_argument("--log-interval", type=int, default=10, help="Log metrics every N iters")

    args = parser.parse_args()

    config = TrainingConfig(
        num_iterations=args.iterations,
        traversals_per_iteration=args.traversals,
        batch_size=args.batch_size,
        buffer_capacity=args.buffer_size,
        value_net_lr=args.lr,
        value_net_epochs_per_iter=args.epochs,
        device=args.device if args.device == "cpu" or (args.device == "cuda" and __import__("torch").cuda.is_available()) else "cpu",
        use_amp=args.amp,
        checkpoint_dir=args.checkpoint_dir,
        resume_from=args.resume,
        wandb_project=args.wandb,
        save_interval=args.save_interval,
        log_interval=args.log_interval,
        exploitability_eval_hands=args.eval_hands,
    )

    config.game.num_players = args.num_players
    config.game.starting_stack = args.starting_stack
    config.game.small_blind = 1
    config.game.big_blind = 2

    config.model.hidden_dim = args.hidden_dim
    config.model.num_layers = args.num_layers

    print("=" * 60)
    print("Deep CFR Training Configuration")
    print("=" * 60)
    print(f"Players: {config.game.num_players}")
    print(f"Stack: {config.game.starting_stack} BB (SB={config.game.small_blind}, BB={config.game.big_blind})")
    print(f"Iterations: {config.num_iterations}")
    print(f"Traversals/iter: {config.traversals_per_iteration}")
    print(f"Batch size: {config.batch_size}")
    print(f"Buffer capacity: {config.buffer_capacity:,}")
    print(f"Learning rate: {config.value_net_lr}")
    print(f"Hidden dim: {config.model.hidden_dim}")
    print(f"Residual blocks: {config.model.num_layers}")
    print(f"Device: {config.device}")
    print(f"Mixed precision: {config.use_amp}")
    print(f"Checkpoint dir: {config.checkpoint_dir}")
    print(f"Resume from: {config.resume_from}")
    print(f"Wandb: {config.wandb_project}")
    print("=" * 60)

    trainer = DeepCFRTrainer(config)
    trainer.train()


if __name__ == "__main__":
    main()
