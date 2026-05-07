# E08 — Matrix Row/Col Operations

**Difficulty:** Easy  
**Category:** Matrix Manipulation

## Problem

Given a matrix `M`, return:
1. `rowSums` — column vector of each row's sum
2. `colMaxes` — row vector of each column's maximum
3. `rowMeans` — column vector of each row's mean

Without using `sum()`, `max()`, or `mean()` directly on the whole matrix — but you can use them inside a loop.

## Signature

```matlab
function [rowSums, colMaxes, rowMeans] = matrixStats(M)
```

## Examples

```matlab
M = [1 2 3; 4 5 6]
rowSums  → [6; 15]
colMaxes → [4 5 6]
rowMeans → [2; 5]
```

## MATLAB Lesson
- **`M(i, :)`** — entire row i
- **`M(:, j)`** — entire column j
- **`sum(v)`**, **`max(v)`**, **`mean(v)`** — apply to a single row/col slice
- **Preallocation** — `zeros(size(M, 1), 1)` for column vector output
