#!/bin/bash
# RunPod / Vast.ai / Lambda Labs setup script
# Usage: curl -sSL <url> | bash

set -e

echo "=== Poker AI Setup ==="

# Install system deps
apt-get update -qq && apt-get install -y -qq curl git python3-pip python3-venv 2>/dev/null || true

# Clone or pull the repo
REPO_URL="${REPO_URL:-https://github.com/YOUR_USER/poker-engine.git}"
if [ -d "poker-engine" ]; then
    cd poker-engine && git pull
else
    git clone "$REPO_URL" && cd poker-engine
fi

# Create venv and install
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip -q
pip install torch numpy wandb -q

# Download a pretrained checkpoint if available
CHECKPOINT_URL="${CHECKPOINT_URL:-}"
if [ -n "$CHECKPOINT_URL" ]; then
    mkdir -p checkpoints
    curl -L "$CHECKPOINT_URL" -o checkpoints/resume.pt
    echo "Downloaded pretrained checkpoint"
fi

echo "=== Setup complete ==="
echo ""
echo "Run training:"
echo "  source .venv/bin/activate"
echo "  python -m train.train \\"
echo "    --iterations 100000 \\"
echo "    --traversals 10000 \\"
echo "    --batch-size 512 \\"
echo "    --hidden-dim 512 \\"
echo "    --num-layers 6 \\"
echo "    --device cuda \\"
echo "    --starting-stack 200 \\"
echo "    --checkpoint-dir checkpoints \\"
echo "    --wandb poker-ai"
echo ""
echo "Resume from checkpoint:"
echo "  python -m train.train --resume checkpoints/ckpt_001000.pt"
