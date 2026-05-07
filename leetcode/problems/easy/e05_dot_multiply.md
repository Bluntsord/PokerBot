# E05 — Dot Multiply

**Difficulty:** Easy  
**Category:** Arrays / Element-wise

## Problem

Given two arrays `A` and `B` of the **same size**, return their element-wise (Hadamard) product **without using `.*`**.

## Signature

```matlab
function C = dotMultiply(A, B)
```

## Rules
- Do **not** use `A .* B`
- Check that `size(A) == size(B)`, throw error if not
- Loop through every element and multiply each pair

## Examples

```matlab
A = [1 2; 3 4]; B = [5 6; 7 8]
% Expected: [5 12; 21 32]

A = [1 2 3]; B = [4 5 6]
% Expected: [4 10 18]

A = [10]; B = [3]
% Expected: 30

A = [1 2]; B = [3 4 5]
% Expected: error
```

## MATLAB Lesson
- **Element-wise vs matrix multiply** — `.*` vs `*`
- **Size comparison** — `isequal(size(A), size(B))` or compare outputs of `size()`
- **Preallocation** — `zeros(size(A))` creates an output matching the input shape
