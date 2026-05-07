from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional

from train.config import (
    ModelConfig, NUM_ACTIONS, NUM_CARDS, NUM_RANKS, NUM_SUITS,
    NUM_STREETS, MAX_PLAYERS, ACTION_FOLD, ACTION_CHECK_CALL,
)


class ResidualBlock(nn.Module):
    def __init__(self, dim: int, dropout: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, dim),
            nn.LayerNorm(dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(dim, dim),
            nn.LayerNorm(dim),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.relu(x + self.net(x))


class CardEncoder(nn.Module):
    def __init__(self, embed_dim: int = 64):
        super().__init__()
        self.card_embed = nn.Embedding(NUM_CARDS, embed_dim)
        self.rank_embed = nn.Embedding(NUM_RANKS, embed_dim // 2)
        self.suit_embed = nn.Embedding(NUM_SUITS, embed_dim // 2)

    def forward(
        self,
        hole_cards: torch.Tensor,
        board_cards: torch.Tensor,
    ) -> torch.Tensor:
        batch_size = hole_cards.shape[0]

        hole = hole_cards.view(batch_size, -1, NUM_CARDS)
        board = board_cards.view(batch_size, -1, NUM_CARDS)

        hole_active = torch.argmax(hole, dim=-1)
        board_active = torch.argmax(board, dim=-1)

        hole_emb = self.card_embed(hole_active).sum(dim=1)
        board_emb = self.card_embed(board_active).sum(dim=1)

        hole_rank = self.rank_embed(hole_active % NUM_RANKS).sum(dim=1)
        hole_suit = self.suit_embed(hole_active // NUM_RANKS).sum(dim=1)
        board_rank = self.rank_embed(board_active % NUM_RANKS).sum(dim=1)
        board_suit = self.suit_embed(board_active // NUM_RANKS).sum(dim=1)

        return torch.cat([hole_emb, board_emb, hole_rank, hole_suit, board_rank, board_suit], dim=-1)


class DeepCFRNet(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()

        self.card_encoder = CardEncoder(embed_dim=config.card_embed_dim)
        card_out_dim = config.card_embed_dim * 4 + config.card_embed_dim * 2

        self.rank_embed = nn.Embedding(NUM_RANKS + 1, config.card_embed_dim // 2)
        self.suit_embed = nn.Embedding(NUM_SUITS + 1, config.card_embed_dim // 4)

        betting_dim = 3 + NUM_STREETS + MAX_PLAYERS + 1
        hist_len = 8

        input_dim = (
            card_out_dim
            + config.card_embed_dim // 2
            + config.card_embed_dim // 4
            + betting_dim
            + hist_len * 3
        )

        self.input_dim = input_dim
        self.betting_dim = betting_dim
        self.hist_len = hist_len

        self.input_proj = nn.Sequential(
            nn.Linear(input_dim, config.hidden_dim),
            nn.LayerNorm(config.hidden_dim),
            nn.ReLU(),
            nn.Dropout(config.dropout),
        )

        self.res_blocks = nn.ModuleList([
            ResidualBlock(config.hidden_dim, config.dropout)
            for _ in range(config.num_layers)
        ])

        self.advantage_head = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim // 2, config.hidden_dim // 4),
            nn.ReLU(),
            nn.Linear(config.hidden_dim // 4, NUM_ACTIONS),
        )

        self.strategy_head = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_dim // 2, config.hidden_dim // 4),
            nn.ReLU(),
            nn.Linear(config.hidden_dim // 4, NUM_ACTIONS),
        )

        self._init_weights()

    def _split_encoded(self, encoded: torch.Tensor):
        hole_cards = encoded[:, :NUM_CARDS]
        board_cards = encoded[:, NUM_CARDS:2 * NUM_CARDS]
        rank_counts = encoded[:, 2 * NUM_CARDS:2 * NUM_CARDS + NUM_RANKS]
        suit_counts = encoded[:, 2 * NUM_CARDS + NUM_RANKS:2 * NUM_CARDS + NUM_RANKS + NUM_SUITS]
        bet_features = encoded[:, 2 * NUM_CARDS + NUM_RANKS + NUM_SUITS:
                                 2 * NUM_CARDS + NUM_RANKS + NUM_SUITS + self.betting_dim]
        hist_flat = encoded[:, 2 * NUM_CARDS + NUM_RANKS + NUM_SUITS + self.betting_dim:
                               2 * NUM_CARDS + NUM_RANKS + NUM_SUITS + self.betting_dim + self.hist_len * 3]
        return hole_cards, board_cards, rank_counts, suit_counts, bet_features, hist_flat

    def forward(
        self,
        encoded: torch.Tensor,
        action_mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        hole_cards, board_cards, rank_counts, suit_counts, bet_features, hist_flat = self._split_encoded(encoded)

        card_feat = self.card_encoder(hole_cards, board_cards)

        rank_max = rank_counts.argmax(dim=-1).clamp(0, NUM_RANKS)
        suit_max = suit_counts.argmax(dim=-1).clamp(0, NUM_SUITS)
        rank_emb = self.rank_embed(rank_max)
        suit_emb = self.suit_embed(suit_max)

        if hist_flat.shape[-1] != self.hist_len * 3:
            hist_flat = hist_flat[:, :self.hist_len * 3]

        x = torch.cat([card_feat, rank_emb, suit_emb, bet_features, hist_flat], dim=-1)

        if x.shape[-1] != self.input_proj[0].in_features:
            if x.shape[-1] > self.input_proj[0].in_features:
                x = x[:, :self.input_proj[0].in_features]
            else:
                pad = torch.zeros(x.shape[0], self.input_proj[0].in_features - x.shape[-1], device=x.device)
                x = torch.cat([x, pad], dim=-1)

        x = self.input_proj(x)

        for block in self.res_blocks:
            x = block(x)

        advantages = self.advantage_head(x)
        strategy_logits = self.strategy_head(x)

        if action_mask is not None:
            mask_val = torch.where(action_mask, 0.0, float('-inf'))
            strategy_logits = strategy_logits + mask_val

        return advantages, strategy_logits

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight, gain=nn.init.calculate_gain("relu"))
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def get_strategy(self, logits: torch.Tensor, temperature: float = 1.0) -> torch.Tensor:
        return F.softmax(logits / temperature, dim=-1)

    def get_action_distribution(
        self,
        hole_cards: torch.Tensor,
        board_cards: torch.Tensor,
        bet_features: torch.Tensor,
        hist_features: torch.Tensor,
        action_mask: torch.Tensor,
        temperature: float = 1.0,
    ) -> torch.Tensor:
        _, logits = self.forward(hole_cards, board_cards, bet_features, hist_features, action_mask)
        return self.get_strategy(logits, temperature)


class SmallCFRNet(nn.Module):
    def __init__(self, config: ModelConfig):
        super().__init__()
        small_hidden = config.hidden_dim // 2

        self.card_encoder = CardEncoder(embed_dim=config.card_embed_dim // 2)
        card_out_dim = config.card_embed_dim + config.card_embed_dim * 2

        betting_dim = 3 + NUM_STREETS + MAX_PLAYERS + 1
        hist_dim = 8 * (3 + NUM_CARDS)
        input_dim = card_out_dim + betting_dim + hist_dim

        self.net = nn.Sequential(
            nn.Linear(input_dim, small_hidden),
            nn.LayerNorm(small_hidden),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(small_hidden, small_hidden),
            nn.LayerNorm(small_hidden),
            nn.ReLU(),
            nn.Dropout(config.dropout),
            nn.Linear(small_hidden, small_hidden // 2),
            nn.LayerNorm(small_hidden // 2),
            nn.ReLU(),
            nn.Linear(small_hidden // 2, NUM_ACTIONS),
        )

    def forward(
        self,
        hole_cards: torch.Tensor,
        board_cards: torch.Tensor,
        bet_features: torch.Tensor,
        hist_features: torch.Tensor,
        action_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        card_feat = self.card_encoder(hole_cards, board_cards)
        x = torch.cat([card_feat, bet_features, hist_features], dim=-1)
        return self.net(x)


def create_model(config: ModelConfig, device: str = "cuda") -> nn.Module:
    model = DeepCFRNet(config)
    model = model.to(device)
    return model
