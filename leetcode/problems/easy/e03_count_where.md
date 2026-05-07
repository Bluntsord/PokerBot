# E03 — Count Where

**Difficulty:** Easy  
**Category:** Arrays / Conditionals

## Problem

Given an array `arr` and a threshold `t`, return two counts:
1. How many elements are **greater than** `t`
2. How many elements are **equal to** `t`

## Signature

```matlab
function [countGreater, countEqual] = countWhere(arr, t)
```

## Rules
- Return two separate outputs
- Loop through elements, use `if` / `elseif`

## Examples

```matlab
[g, e] = countWhere([1 5 3 5 2], 3)
% Expected: g = 2 (the 5s), e = 1 (the 3)

[g, e] = countWhere([10 20 30], 25)
% Expected: g = 1, e = 0

[g, e] = countWhere([7], 7)
% Expected: g = 0, e = 1

[g, e] = countWhere([], 5)
% Expected: g = 0, e = 0
```

## MATLAB Lesson
- **Multiple return values** — `function [a, b] = ...`
- **`if` / `elseif`** — only use `elseif` not `else if`
- **Empty input handling** — check `isempty(arr)` early
