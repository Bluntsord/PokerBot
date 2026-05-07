#!/bin/bash
# Long-running training with automatic checkpointing and restart
# Designed for RunPod / Lambda Labs / Vast.ai
# Usage: ./train_loop.sh

set -e

ITERATIONS=100000
SAVE_EVERY=500
LOG_EVERY=50

source .venv/bin/activate

echo "=== Poker AI Training Loop ==="
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'none')"
echo "Iterations: $ITERATIONS"
echo "Started: $(date)"
echo "================================"

python -m train.train \
    --iterations "$ITERATIONS" \
    --traversals 10000 \
    --batch-size 512 \
    --hidden-dim 512 \
    --num-layers 6 \
    --device cuda \
    --starting-stack 200 \
    --checkpoint-dir checkpoints \
    --save-interval "$SAVE_EVERY" \
    --log-interval "$LOG_EVERY" \
    --wandb poker-ai \
    --amp

echo "Done at $(date)"
