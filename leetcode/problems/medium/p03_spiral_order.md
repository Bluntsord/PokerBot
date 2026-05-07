# 03 — Spiral Order

**Difficulty:** Medium  
**Category:** Matrix Traversal

## Problem

Given an m×n matrix, return **a 1D row vector** of all elements in spiral order (clockwise, starting from top-left).

## Signature

```matlab
function result = spiralOrder(matrix)
```

## Rules
- Return `[]` for empty matrix
- Handle any dimensions: 1×1, 1×n, m×1, m×n
- Preallocate your output (hint: `zeros(1, m*n)`)

## Examples

```matlab
% Example 1: 3x3
Input:  [1 2 3; 4 5 6; 7 8 9]
Output: [1 2 3 6 9 8 7 4 5]

% Example 2: 3x4
Input:  [1 2 3 4; 5 6 7 8; 9 10 11 12]
Output: [1 2 3 4 8 12 11 10 9 5 6 7]

% Example 3: 1x5 (single row)
Input:  [1 2 3 4 5]
Output: [1 2 3 4 5]

% Example 4: 4x1 (single column)
Input:  [1; 2; 3; 4]
Output: [1 2 3 4]

% Example 5: Empty
Input:  []
Output: []
```

## MATLAB Lesson
- **Boundary tracking** — maintain `top`, `bottom`, `left`, `right` indices that shrink inward
- **Preallocation with known final size** — `zeros(1, m*n)` then fill in order
- **Early return pattern** — check empty input at the top and return `[]`
