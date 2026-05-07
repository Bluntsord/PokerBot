use std::collections::HashSet;

pub const NUM_CARDS: usize = 52;
pub const NUM_SUITS: usize = 4;
pub const NUM_RANKS: usize = 13;

const RANKS: &[u8] = b"23456789TJQKA";
const SUITS: &[u8] = b"cdhs";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Card(pub u8);

impl Card {
    pub fn new(id: u8) -> Self {
        assert!(id < 52, "Card id must be 0-51");
        Card(id)
    }

    pub fn from_str(s: &str) -> Option<Self> {
        let bytes = s.as_bytes();
        if bytes.len() != 2 {
            return None;
        }
        let rank = RANKS.iter().position(|&r| r == bytes[0].to_ascii_uppercase())?;
        let suit = SUITS.iter().position(|&r| r == bytes[1].to_ascii_lowercase())?;
        Some(Card((rank + 13 * suit) as u8))
    }

    pub fn rank(&self) -> usize {
        (self.0 % 13) as usize
    }

    pub fn suit(&self) -> usize {
        (self.0 / 13) as usize
    }

    pub fn to_str(&self) -> String {
        let r = RANKS[self.rank()] as char;
        let s = SUITS[self.suit()] as char;
        format!("{}{}", r, s)
    }
}

pub struct Deck {
    cards: Vec<Card>,
    next: usize,
}

impl Deck {
    pub fn new() -> Self {
        Deck {
            cards: (0..52).map(Card).collect(),
            next: 0,
        }
    }

    pub fn shuffled(rng: &mut impl rand::Rng) -> Self {
        let mut cards: Vec<Card> = (0..52).map(Card).collect();
        for i in (1..52).rev() {
            let j = rng.gen_range(0..=i);
            cards.swap(i, j);
        }
        Deck { cards, next: 0 }
    }

    pub fn deal(&mut self, count: usize) -> Vec<Card> {
        let result: Vec<Card> = self.cards[self.next..self.next + count].to_vec();
        self.next += count;
        result
    }

    pub fn deal_one(&mut self) -> Card {
        let card = self.cards[self.next];
        self.next += 1;
        card
    }

    pub fn remaining(&self) -> usize {
        52 - self.next
    }

    pub fn reset(&mut self) {
        self.next = 0;
    }
}

pub fn parse_cards(s: &str) -> Vec<Card> {
    s.split_whitespace()
        .filter_map(Card::from_str)
        .collect()
}

pub fn cards_to_str(cards: &[Card]) -> String {
    cards.iter().map(|c| c.to_str()).collect::<Vec<_>>().join(" ")
}
