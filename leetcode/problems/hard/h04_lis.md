# H04 — Longest Increasing Subsequence

**Difficulty:** Hard  
**Category:** Dynamic Programming

## Problem

Given an array `arr`, return the **length** of the longest strictly increasing subsequence (LIS) using O(n²) DP. A subsequence does not need to be contiguous.

## Signature

```matlab
function maxLen = longestIncreasingSubsequence(arr)
```

## Rules
- Build a DP array `dp(i)` = length of LIS ending at index i
- Formula: `dp(i) = max(1, 1 + max(dp(j) for all j < i where arr(j) < arr(i)))`
- Preallocate `dp` with ones
- Do **not** use the patience sorting / O(n log n) method — just O(n²) DP

## Examples

```matlab
arr = [10 9 2 5 3 7 101 18]
% Expected: 4  (the subsequence [2 3 7 101] or [2 5 7 101])

arr = [3 3 3]
% Expected: 1  (strictly increasing, no duplicates count)

arr = [1 2 3 4 5]
% Expected: 5

arr = [5]
% Expected: 1
```

## MATLAB Lesson
- **Nested loops + `max()`** — DP recurrence over all previous elements
- **Preallocation** — `dp = ones(1, n)` is both allocation and initial value
- **`max()` on empty** — `max([])` returns `-Inf`, so handle the case when no smaller previous element exists
