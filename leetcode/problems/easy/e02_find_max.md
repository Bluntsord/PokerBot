# E02 — Find Maximum

**Difficulty:** Easy  
**Category:** Arrays / Conditionals

## Problem

Given a numeric array `arr`, return the largest element **without using `max()`**.

## Signature

```matlab
function m = findMax(arr)
```

## Rules
- Do **not** use `max(arr)`
- Loop through elements, track the largest seen so far
- Handle scalar input (just return it)

## Examples

```matlab
arr = [3 7 1 9 2]
% Expected: 9

arr = [-5 -2 -8]
% Expected: -2

arr = [10; 20; 5]
% Expected: 20

arr = 42
% Expected: 42
```

## MATLAB Lesson
- **Linear indexing** — `arr(k)` walks column-by-column
- **Tracking state** — keep a variable updated in the loop
- **`-inf`** — smallest possible number, good for initial max variable
