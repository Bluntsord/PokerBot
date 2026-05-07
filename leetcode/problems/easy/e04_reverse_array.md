# E04 — Reverse Array

**Difficulty:** Easy  
**Category:** Arrays / Indexing

## Problem

Given a numeric 1D array `arr`, return it in reversed order **without using `flip()` or `fliplr()`**.

## Signature

```matlab
function result = reverseArray(arr)
```

## Rules
- Do **not** use `flip(arr)`, `fliplr(arr)`, or `arr(end:-1:1)`
- Build the output yourself using a loop and index arithmetic
- Preallocate with `zeros(1, n)`

## Examples

```matlab
arr = [1 2 3 4 5]
% Expected: [5 4 3 2 1]

arr = [10]
% Expected: [10]

arr = [1; 2; 3]   % column vector
% Expected: [3; 2; 1]
```

## MATLAB Lesson
- **Preallocation** — `zeros(size(arr))` keeps same shape
- **Index arithmetic** — `result(i) = arr(end - i + 1)`
- **Preserving row/column** — use `size(arr)` to match dimensions
