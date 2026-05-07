# E01 — Array Sum

**Difficulty:** Easy  
**Category:** Arrays / Loops

## Problem

Given a numeric array `arr` (any dimensions), return the total sum of all its elements **without using `sum()`**.

## Signature

```matlab
function total = arraySum(arr)
```

## Rules
- Do **not** use `sum(arr)` or `sum(arr, 'all')`
- Loop over every element and accumulate
- Use `numel(arr)` for total count, or nested `for` with `size()`

## Examples

```matlab
arr = [1 2 3 4 5]
% Expected: 15

arr = [-1 0 3]
% Expected: 2

arr = 7
% Expected: 7

arr = [1 2; 3 4]
% Expected: 10
```

## MATLAB Lesson
- **`numel(arr)`** — total number of elements (rows × cols)
- **Linear indexing** — `arr(k)` works for any shape, goes column-by-column
- **Falling back to a loop** — not everything needs built-ins
