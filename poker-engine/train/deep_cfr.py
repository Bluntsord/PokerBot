from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random
import time
import os
import json
from typing import List, Tuple, Dict, Optional
from collections import defaultdict
from pathlib import Path

from engine.game import GameEngine, GameConfig, GameState
from engine.types import Action, ActionType, Card, Street, PlayerState
from engine.evaluator import evaluate, ensure_initialized

from train.config import (
    TrainingConfig, ModelConfig, GameConfig as TrainGameConfig,
    NUM_ACTIONS, ACTION_FOLD, ACTION_CHECK_CALL,
    ACTION_BET_05, ACTION_BET_075, ACTION_BET_10, ACTION_BET_15,
    ACTION_ALL_IN, AVAILABLE_ACTIONS, NUM_CARDS,
)
from train.encoding import StateEncoder
from train.model import DeepCFRNet, SmallCFRNet, create_model
from train.buffer import ReplayBuffer, RegretBuffer

TRAVERSE_BATCH_SIZE = 512


class DeepCFRTrainer:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.device = torch.device(config.device if torch.cuda.is_available() else "cpu")
        if self.device.type == "cuda":
            torch.backends.cudnn.benchmark = True

        ensure_initialized()

        self.encoder = StateEncoder(device=self.device)

        self.value_net = create_model(config.model, device=self.device.type)
        self.target_net = create_model(config.model, device=self.device.type)
        self.target_net.load_state_dict(self.value_net.state_dict())

        self.value_buffer = ReplayBuffer(
            capacity=config.buffer_capacity,
            state_dim=self.encoder.state_dim,
            device=self.device.type,
        )

        self.optimizer = torch.optim.AdamW(
            self.value_net.parameters(),
            lr=config.value_net_lr,
            weight_decay=config.value_net_weight_decay,
        )
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            self.optimizer, T_0=100, T_mult=2
        )

        self.scaler = torch.amp.GradScaler("cuda") if config.use_amp and self.device.type == "cuda" else None

        self.strategy_sum: dict = {}
        self.strategy_count: dict = {}

        self.iteration = 0
        self.best_exploitability = float("inf")
        self.total_traversals = 0

        if config.resume_from and os.path.exists(config.resume_from):
            self._load_checkpoint(config.resume_from)

        if config.wandb_project:
            import wandb
            self.wandb = wandb
            self.wandb.init(
                project=config.wandb_project,
                entity=config.wandb_entity,
                config={
                    "game": config.game.__dict__,
                    "model": config.model.__dict__,
                    "num_iterations": config.num_iterations,
                    "batch_size": config.batch_size,
                },
                name=f"deep_cfr_{int(time.time())}",
            )
        else:
            self.wandb = None

    def _load_checkpoint(self, path: str):
        checkpoint = torch.load(path, map_location=self.device, weights_only=False)
        self.value_net.load_state_dict(checkpoint["value_net"])
        self.target_net.load_state_dict(checkpoint["target_net"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.scheduler.load_state_dict(checkpoint["scheduler"])
        self.iteration = checkpoint["iteration"]
        self.strategy_sum = {
            int(k): v.to(self.device) if hasattr(v, 'to') else torch.tensor(v, device=self.device)
            for k, v in checkpoint.get("strategy_sum", {}).items()
        }
        self.strategy_count = defaultdict(int, {
            int(k): v for k, v in checkpoint.get("strategy_count", {}).items()
        })
        self.best_exploitability = checkpoint.get("best_exploitability", float("inf"))
        print(f"Resumed from iteration {self.iteration}")

    def _save_checkpoint(self, path: str, is_best: bool = False):
        checkpoint = {
            "value_net": self.value_net.state_dict(),
            "target_net": self.target_net.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "scheduler": self.scheduler.state_dict(),
            "iteration": self.iteration,
            "strategy_sum": {k: v.cpu() if hasattr(v, 'cpu') else v for k, v in self.strategy_sum.items()},
            "strategy_count": dict(self.strategy_count),
            "best_exploitability": self.best_exploitability,
        }
        torch.save(checkpoint, path)
        if is_best:
            best_path = path.replace(".pt", "_best.pt")
            torch.save(checkpoint, best_path)

    def _make_state_dict(self, engine: GameEngine, player_id: int) -> dict:
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
            "opp_stack": max(
                (p.stack for i, p in enumerate(state.players)
                 if i != player_id and not p.folded),
                default=0,
            ),
            "starting_stack": engine.config.starting_stack,
            "big_blind": engine.config.big_blind,
            "action_history": [
                {"action": a.action_type.name, "amount": a.amount}
                for _, a in state.action_history[-20:]
            ],
        }

    def _action_to_discrete(
        self, action: Action, state_dict: dict, player: PlayerState
    ) -> Tuple[int, int]:
        if action.action_type == ActionType.FOLD:
            return ACTION_FOLD, 0
        elif action.action_type in (ActionType.CHECK, ActionType.CALL):
            return ACTION_CHECK_CALL, state_dict["to_call"]
        elif action.action_type in (ActionType.BET, ActionType.RAISE):
            pot = state_dict["pot"]
            if pot <= 0:
                return ACTION_BET_05, action.amount
            frac = action.amount / pot
            if frac <= 0.6:
                return ACTION_BET_05, action.amount
            elif frac <= 0.85:
                return ACTION_BET_075, action.amount
            elif frac <= 1.25:
                return ACTION_BET_10, action.amount
            else:
                return ACTION_BET_15, action.amount
        elif action.action_type == ActionType.ALL_IN:
            return ACTION_BET_15, player.stack + player.current_bet
        return ACTION_CHECK_CALL, state_dict["to_call"]

    def _discrete_to_action(
        self, discrete_action: int, state_dict: dict, player: PlayerState
    ) -> Action:
        to_call = state_dict["to_call"]
        pot = state_dict["pot"]
        stack = player.stack
        bb = self.config.game.big_blind

        if discrete_action == ACTION_FOLD:
            return Action(ActionType.FOLD)
        elif discrete_action == ACTION_CHECK_CALL:
            if to_call == 0:
                return Action(ActionType.CHECK)
            elif to_call >= stack:
                return Action(ActionType.ALL_IN, stack, is_all_in=True)
            else:
                return Action(ActionType.CALL, to_call)

        fractions = {ACTION_BET_05: 0.5, ACTION_BET_075: 0.75, ACTION_BET_10: 1.0, ACTION_BET_15: 1.5}
        frac = fractions.get(discrete_action, 0.5)
        amt = max(int(pot * frac), bb * 2) if pot > 0 else bb * (2 + discrete_action - ACTION_BET_05)

        if to_call == 0:
            if amt >= stack:
                return Action(ActionType.ALL_IN, stack, is_all_in=True)
            return Action(ActionType.BET, amt)
        else:
            total = player.current_bet + to_call + amt
            if total >= stack + player.current_bet:
                return Action(ActionType.ALL_IN, stack, is_all_in=True)
            return Action(ActionType.RAISE, to_call + amt - player.current_bet)

    def _compute_strategy(self, enc: torch.Tensor, mask: torch.Tensor, legal: torch.Tensor) -> torch.Tensor:
        enc_b = enc.unsqueeze(0)
        mask_b = mask.unsqueeze(0)
        with torch.no_grad():
            advantages, logits = self.value_net(enc_b, mask_b)
        strategy = F.softmax(logits.squeeze(0) / 0.5, dim=-1)
        strategy = strategy * legal
        s = strategy.sum()
        return strategy / s if s > 0 else legal / legal.sum()

    def _compute_strategies_batch(
        self, encodings: torch.Tensor, masks: torch.Tensor, legals: torch.Tensor
    ) -> torch.Tensor:
        B = encodings.shape[0]
        with torch.no_grad():
            advantages, logits = self.value_net(encodings, masks)
        strategies = F.softmax(logits / 0.5, dim=-1)
        strategies = strategies * legals
        strategies = strategies / (strategies.sum(dim=-1, keepdim=True) + 1e-8)
        return strategies

    def _hash_state(self, state_dict: dict) -> int:
        key = (
            state_dict.get("street", "PREFLOP"),
            state_dict.get("position", 0),
            state_dict.get("num_active", 2),
            round(state_dict.get("pot", 0) / max(state_dict.get("starting_stack", 200), 1), 2),
            round(state_dict.get("to_call", 0) / max(state_dict.get("pot", 1), 1), 2),
            round(state_dict.get("stack", 200) / max(state_dict.get("starting_stack", 200), 1), 2),
        )
        return hash(key)

    def _compute_counterfactual_values(
        self,
        enc: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        enc_b = enc.unsqueeze(0)
        with torch.no_grad():
            advantages, _ = self.value_net(enc_b)

        return advantages.squeeze(0)

    def _make_game(self) -> GameEngine:
        return GameEngine(GameConfig(
            num_players=self.config.game.num_players,
            starting_stack=self.config.game.starting_stack,
            small_blind=self.config.game.small_blind,
            big_blind=self.config.game.big_blind,
        ))

    def _traverse_batch(self) -> int:
        games = [self._make_game() for _ in range(TRAVERSE_BATCH_SIZE)]
        for g in games:
            g.reset()
        traversers = [random.randint(0, self.config.game.num_players - 1) for _ in range(TRAVERSE_BATCH_SIZE)]
        active = [True] * TRAVERSE_BATCH_SIZE
        total_samples = 0

        while any(active):
            batch_encs, batch_masks, batch_legals, batch_idxs = [], [], [], []
            batch_hole, batch_board, batch_sd = [], [], []

            for i in range(TRAVERSE_BATCH_SIZE):
                if not active[i]:
                    continue
                g = games[i]
                if g.state.hand_over:
                    active[i] = False
                    continue

                cur = g.state.current_player
                p = g.state.players[cur]
                if not p.can_act() or p.folded:
                    active[i] = False
                    continue

                sd = self._make_state_dict(g, cur)
                hole = [c.id for c in p.hole_cards]
                board = [c.id for c in g.state.board]
                enc, mask, legal = self.encoder.encode(hole, board, sd)

                batch_encs.append(enc)
                batch_masks.append(mask)
                batch_legals.append(legal)
                batch_idxs.append(i)
                batch_hole.append(hole)
                batch_board.append(board)
                batch_sd.append(sd)

            if not batch_encs:
                continue

            enc_t = torch.stack(batch_encs).to(self.device)
            mask_t = torch.stack(batch_masks).to(self.device)
            legal_t = torch.stack(batch_legals).to(self.device)

            strategies = self._compute_strategies_batch(enc_t, mask_t, legal_t)

            for j, i in enumerate(batch_idxs):
                if not active[i]:
                    continue

                g = games[i]
                cur = g.state.current_player
                p = g.state.players[cur]
                t = traversers[i]

                strategy = strategies[j]

                if cur == t:
                    sh = self._hash_state(batch_sd[j])
                    if sh not in self.strategy_sum:
                        self.strategy_sum[sh] = torch.zeros(NUM_ACTIONS, device=self.device)
                        self.strategy_count[sh] = 0
                    self.strategy_sum[sh] = self.strategy_sum[sh] + strategy.detach()
                    self.strategy_count[sh] += 1

                    cfr_vals = self._compute_counterfactual_values(enc_t[j], mask_t[j])
                    self.value_buffer.add(enc_t[j].cpu(), cfr_vals.cpu(), mask_t[j].cpu())
                    total_samples += 1

                sampled = torch.multinomial(strategy, 1).item()
                action = self._discrete_to_action(sampled, batch_sd[j], p)
                g.step(action)

        return total_samples

    def traverse(self) -> int:
        return self._traverse_batch()

    def _train_value_network(self) -> float:
        if len(self.value_buffer) < self.config.batch_size:
            return 0.0

        total_loss = 0.0
        num_batches = 0
        batches_per_epoch = min(50, len(self.value_buffer) // self.config.batch_size)

        for _ in range(self.config.value_net_epochs_per_iter):
            for _ in range(batches_per_epoch):
                states, targets, masks, weights = self.value_buffer.sample(
                    self.config.batch_size
                )
                if states.shape[0] == 0:
                    continue

                self.optimizer.zero_grad()

                if self.scaler is not None:
                    with torch.amp.autocast("cuda"):
                        pred, _ = self.value_net(states)
                        loss = F.mse_loss(pred, targets, reduction="none")
                        loss = (loss.mean(dim=-1) * weights).mean()
                    self.scaler.scale(loss).backward()
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(
                        self.value_net.parameters(), self.config.model.grad_clip_norm
                    )
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                else:
                    pred, _ = self.value_net(states)
                    loss = F.mse_loss(pred, targets, reduction="none")
                    loss = (loss.mean(dim=-1) * weights).mean()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        self.value_net.parameters(), self.config.model.grad_clip_norm
                    )
                    self.optimizer.step()

                total_loss += loss.item()
                num_batches += 1

        self.scheduler.step()
        return total_loss / max(num_batches, 1)

    def _update_target_network(self):
        with torch.no_grad():
            for tp, sp in zip(self.target_net.parameters(), self.value_net.parameters()):
                tp.data.copy_(0.95 * tp.data + 0.05 * sp.data)

    def train_iteration(self) -> Dict:
        start_time = time.time()
        samples_collected = 0

        num_batches = max(1, self.config.traversals_per_iteration // TRAVERSE_BATCH_SIZE)
        for _ in range(num_batches):
            n = self._traverse_batch()
            samples_collected += n

        train_loss = self._train_value_network()
        self._update_target_network()
        self.iteration += 1

        metrics = {
            "iteration": self.iteration,
            "samples": samples_collected,
            "buffer_size": len(self.value_buffer),
            "train_loss": train_loss,
            "lr": self.optimizer.param_groups[0]["lr"],
            "time": time.time() - start_time,
        }

        if self.iteration % self.config.save_interval == 0:
            path = os.path.join(self.config.checkpoint_dir, f"ckpt_{self.iteration:06d}.pt")
            self._save_checkpoint(path)

        if self.iteration % self.config.log_interval == 0:
            avg_count = sum(self.strategy_count.values()) / max(len(self.strategy_count), 1)
            print(
                f"Iter {self.iteration:6d} | "
                f"Samples: {samples_collected:6d} | "
                f"Buf: {len(self.value_buffer):8d} | "
                f"Loss: {train_loss:.6f} | "
                f"States: {len(self.strategy_count):6d} | "
                f"Avg visits: {avg_count:.1f} | "
                f"Time: {metrics['time']:.1f}s"
            )

        if self.wandb:
            self.wandb.log(metrics)

        return metrics

    def train(self):
        print(f"Device: {self.device}")
        print(f"Model params: {sum(p.numel() for p in self.value_net.parameters()):,}")
        print(f"Starting from iteration {self.iteration}")
        print(f"Target: {self.config.num_iterations}")
        print("-" * 60)

        for _ in range(self.iteration, self.config.num_iterations):
            metrics = self.train_iteration()

            if self.iteration % self.config.eval_interval == 0:
                expl = self._estimate_exploitability()
                metrics["exploitability"] = expl
                print(f"  → Exploitability: {expl:.4f} BB/hand")

                if expl < self.best_exploitability:
                    self.best_exploitability = expl
                    bp = os.path.join(self.config.checkpoint_dir, f"best_{self.iteration:06d}.pt")
                    self._save_checkpoint(bp, is_best=True)
                    print(f"  → New best!")

        fp = os.path.join(self.config.checkpoint_dir, "final.pt")
        self._save_checkpoint(fp)
        print(f"\nDone. Final model: {fp}")
        print(f"Best exploitability: {self.best_exploitability:.4f} BB/hand")

    def _estimate_exploitability(self) -> float:
        game_cfg = GameConfig(
            num_players=self.config.game.num_players,
            starting_stack=self.config.game.starting_stack,
            small_blind=self.config.game.small_blind,
            big_blind=self.config.game.big_blind,
        )
        n_hands = min(self.config.exploitability_eval_hands, 500)
        total = 0.0

        for _ in range(n_hands):
            engine = GameEngine(game_cfg)
            engine.reset()

            while not engine.state.hand_over:
                cur = engine.state.current_player
                p = engine.state.players[cur]
                if not p.can_act():
                    break

                sd = self._make_state_dict(engine, cur)
                hole = [c.id for c in p.hole_cards]
                board = [c.id for c in engine.state.board]
                enc, mask, legal = self.encoder.encode(hole, board, sd)

                strat = self._compute_strategy(enc, mask, legal)
                idx = torch.multinomial(strat, 1).item()
                action = self._discrete_to_action(idx, sd, p)
                engine.step(action)

            for wid, chips, _ in engine.state.winners:
                total += chips if wid == 0 else -chips

        avg = total / n_hands
        return abs(avg) / self.config.game.big_blind
