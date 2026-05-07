pub mod deck;
pub mod evaluator;

use pyo3::prelude::*;

#[pyfunction]
fn evaluate_hand(cards: Vec<u8>) -> u16 {
    let cards: Vec<deck::Card> = cards.into_iter().map(deck::Card).collect();
    evaluator::evaluate(&cards)
}

#[pyfunction]
fn evaluate_hand_str(cards_str: &str) -> u16 {
    evaluator::evaluate_str(cards_str)
}

#[pyfunction]
fn get_rank_name(rank: u16) -> String {
    evaluator::get_rank_name(rank).to_string()
}

#[pymodule]
fn poker_evaluator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evaluate_hand, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_hand_str, m)?)?;
    m.add_function(wrap_pyfunction!(get_rank_name, m)?)?;
    Ok(())
}
