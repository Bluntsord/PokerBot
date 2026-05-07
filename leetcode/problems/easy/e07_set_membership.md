# E07 — Set Membership

**Difficulty:** Easy  
**Category:** Sets / ismember

## Problem

Given two arrays `A` and `B`, return:
1. `inBoth` — elements present in both A and B (intersection, no duplicates)
2. `onlyInA` — elements in A but NOT in B (setdiff)
3. `isMember` — a logical array same size as A, true where A(i) is in B

## Signature

```matlab
function [inBoth, onlyInA, isMember] = setOps(A, B)
```

## Rules
- Use `ismember()` and `unique()`
- Sort outputs using `sort()`

## Examples

```matlab
A = [1 2 3 4 5]; B = [3 5 5 7 9]
inBoth   → [3 5]
onlyInA  → [1 2 4]
isMember → [0 0 1 0 1]
```

## MATLAB Lesson
- **`ismember(A, B)`** — logical array, true where A elements are in B
- **`intersect(A, B)`** — sorted unique elements in both
- **`setdiff(A, B)`** — sorted unique elements in A but not B
- **`unique(A)`** — remove duplicates
