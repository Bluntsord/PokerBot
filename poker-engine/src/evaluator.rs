use std::sync::OnceLock;

use crate::deck::Card;

static LOOKUP: OnceLock<Box<LookupTables>> = OnceLock::new();

struct LookupTables {
    hand_ranks: Vec<u16>,
    binomials: [[u32; 6]; 53],
}

fn binomial(n: u32, k: u32) -> u32 {
    if n < k {
        return 0;
    }
    let k = k.min(n - k);
    let mut result = 1u32;
    for i in 0..k {
        result = result * (n - i) / (i + 1);
    }
    result
}

fn build_hand_ranks() -> Vec<u16> {
    let total = binomial(52, 5) as usize;
    let mut ranks = vec![0u16; total];
    let mut combos: Vec<(Vec<u8>, u16)> = Vec::with_capacity(total);

    for c0 in 0..48u8 {
        for c1 in (c0 + 1)..49 {
            for c2 in (c1 + 1)..50 {
                for c3 in (c2 + 1)..51 {
                    for c4 in (c3 + 1)..52 {
                        let cards = [c0, c1, c2, c3, c4];
                        let strength = evaluate_5_cards(&cards);
                        let idx = hand_index(&cards);
                        combos.push((cards.to_vec(), idx));
                        ranks[idx as usize] = strength;
                    }
                }
            }
        }
    }

    combos.sort_by_key(|(cards, _)| *ranks.get(&cards[0] as usize).unwrap_or(&0));
    combos.sort_by(|(a, _), (b, _)| {
        let sa = ranks[hand_index(a) as usize];
        let sb = ranks[hand_index(b) as usize];
        sa.cmp(&sb)
    });

    for (rank, (_cards, idx)) in combos.iter().enumerate() {
        ranks[*idx as usize] = (rank + 1) as u16;
    }

    ranks
}

fn evaluate_5_cards(cards: &[u8; 5]) -> u16 {
    let ranks: Vec<usize> = cards.iter().map(|&c| (c % 13) as usize).collect();
    let suits: Vec<usize> = cards.iter().map(|&c| (c / 13) as usize).collect();

    let is_flush = suits.iter().all(|&s| s == suits[0]);

    let mut rank_counts = [0u8; 13];
    for &r in &ranks {
        rank_counts[r] += 1;
    }

    let is_straight = {
        let mut sorted: Vec<usize> = ranks.clone();
        sorted.sort();
        sorted.dedup();
        let normal = sorted.len() == 5 && sorted[4] - sorted[0] == 4;
        let wheel = sorted == vec![0, 1, 2, 3, 12];
        normal || wheel
    };

    if is_flush && is_straight {
        if ranks.contains(&12) && ranks.contains(&0) {
            return 5;
        }
        return 4;
    }

    let quads = rank_counts.iter().position(|&c| c == 4);
    if let Some(q) = quads {
        let kicker = rank_counts.iter().position(|&c| c == 1).unwrap();
        return (2 * 13 + (q as u16)) * 100 + (kicker as u16);
    }

    let trips = rank_counts.iter().position(|&c| c == 3);
    let pair = rank_counts.iter().position(|&c| c == 2);
    if trips.is_some() && pair.is_some() {
        return (3 * 13 + trips.unwrap() as u16) * 100 + (pair.unwrap() as u16);
    }

    if is_flush {
        let mut high_cards: Vec<usize> = ranks.clone();
        high_cards.sort_by(|a, b| b.cmp(a));
        return 5 * 100
            + high_cards[0] as u16 * 10000
            + high_cards[1] as u16 * 1000
            + high_cards[2] as u16 * 100
            + high_cards[3] as u16 * 10
            + high_cards[4] as u16;
    }

    if is_straight {
        let high = if ranks.contains(&12) && ranks.contains(&0) {
            3
        } else {
            *ranks.iter().max().unwrap() as u16
        };
        return 4 * 100 + high;
    }

    if let Some(t) = trips {
        let kickers: Vec<usize> = (0..13)
            .filter(|&r| rank_counts[r] == 1)
            .collect();
        return (3 * 13 + t as u16) * 10000 + (kickers[1] as u16) * 100 + (kickers[0] as u16);
    }

    let pairs: Vec<usize> = (0..13).filter(|&r| rank_counts[r] == 2).collect();
    if pairs.len() == 2 {
        let kicker = (0..13).find(|&r| rank_counts[r] == 1).unwrap();
        return (2 * 13 + pairs[1] as u16) * 10000
            + (pairs[0] as u16) * 100
            + (kicker as u16);
    }

    if pairs.len() == 1 {
        let kickers: Vec<usize> = (0..13)
            .filter(|&r| rank_counts[r] == 1)
            .collect();
        return (1 * 13 + pairs[0] as u16) * 1000000
            + (kickers[2] as u16) * 10000
            + (kickers[1] as u16) * 100
            + (kickers[0] as u16);
    }

    let mut sorted: Vec<usize> = ranks.clone();
    sorted.sort_by(|a, b| b.cmp(a));
    sorted[0] as u16 * 100000000
        + sorted[1] as u16 * 1000000
        + sorted[2] as u16 * 10000
        + sorted[3] as u16 * 100
        + sorted[4] as u16
}

fn hand_index(cards: &[u8]) -> u16 {
    let mut index = 0u32;
    for (i, &card) in cards.iter().enumerate() {
        index += binomial(card as u32, (i + 1) as u32);
    }
    index as u16
}

fn get_tables() -> &'static LookupTables {
    LOOKUP.get_or_init(|| {
        let hand_ranks = build_hand_ranks();
        let mut binomials = [[0u32; 6]; 53];
        for n in 0..53u32 {
            for k in 0..6u32 {
                binomials[n as usize][k as usize] = binomial(n, k);
            }
        }
        Box::new(LookupTables { hand_ranks, binomials })
    })
}

pub fn evaluate(cards: &[Card]) -> u16 {
    let tables = get_tables();
    let mut best = u16::MAX;

    let n = cards.len();
    let indices: Vec<u8> = cards.iter().map(|c| c.0).collect();

    if n == 5 {
        let mut idx = 0u32;
        let mut sorted = indices.clone();
        sorted.sort();
        for (i, &card) in sorted.iter().enumerate() {
            idx += tables.binomials[card as usize][i + 1];
        }
        return tables.hand_ranks[idx as usize];
    }

    for a in 0..n {
        for b in (a + 1)..n {
            for c in (b + 1)..n {
                for d in (c + 1)..n {
                    for e in (d + 1)..n {
                        let mut combo = [indices[a], indices[b], indices[c], indices[d], indices[e]];
                        combo.sort();
                        let mut idx = 0u32;
                        for (i, &card) in combo.iter().enumerate() {
                            idx += tables.binomials[card as usize][i + 1];
                        }
                        let rank = tables.hand_ranks[idx as usize];
                        if rank < best {
                            best = rank;
                        }
                    }
                }
            }
        }
    }
    best
}

pub fn evaluate_str(cards_str: &str) -> u16 {
    let cards: Vec<Card> = cards_str
        .split_whitespace()
        .filter_map(Card::from_str)
        .collect();
    evaluate(&cards)
}

pub fn get_rank_name(rank: u16) -> &'static str {
    match rank {
        1 => "Royal Flush",
        2 => "Straight Flush",
        3..=9 => "Straight Flush",
        _ => {
            let category = rank / 10000;
            match category {
                0..=5 => "High Card",
                6..=25 => "One Pair",
                26..=137 => "Two Pair",
                138..=285 => "Three of a Kind",
                286..=295 => "Straight",
                296..=422 => "Flush",
                423..=578 => "Full House",
                579..=734 => "Four of a Kind",
                735..=7462 => "Straight Flush",
                _ => "Unknown",
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::deck::Card;

    #[test]
    fn test_royal_flush() {
        let cards = [Card(9), Card(10), Card(11), Card(12), Card(8)];
        let rank = evaluate(&cards);
        assert_eq!(rank, 1, "Royal flush should be rank 1, got {}", rank);
    }

    #[test]
    fn test_high_card() {
        let cards = [Card(0), Card(1), Card(2), Card(3), Card(17)];
        let rank = evaluate(&cards);
        assert!(rank > 1000, "High card should have high rank, got {}", rank);
    }

    #[test]
    fn test_pair() {
        let cards = [Card(0), Card(13), Card(2), Card(3), Card(4)];
        let rank = evaluate(&cards);
        assert!(rank < evaluate(&[Card(0), Card(1), Card(2), Card(3), Card(17)]));
    }

    #[test]
    fn test_seven_card_eval() {
        let cards = vec![Card(9), Card(10), Card(11), Card(12), Card(8), Card(0), Card(1)];
        let rank = evaluate(&cards);
        assert_eq!(rank, 1, "7-card should find royal flush, got {}", rank);
    }

    #[test]
    fn test_evaluate_str() {
        let rank = evaluate_str("Ac Kc Qc Jc Tc");
        assert_eq!(rank, 1, "AcKcQcJcTc should be royal flush");
    }
}
