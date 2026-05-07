# 02 — Rotate Image

**Difficulty:** Medium  
**Category:** Matrix / In-Place

## Problem

Given an n×n 2D matrix representing an image, rotate it **90 degrees clockwise in-place**. Do not allocate another 2D matrix.

## Signature

```matlab
function matrix = rotate(matrix)
```

## Rules
- The input must be mutated directly (in-place)
- You may use `size()` and built-in transpose/flip
- Throw `error('Matrix must be square')` if not n×n
- Do not use `imrotate()`

## Hints
<details><summary>Click if stuck</summary>

1. Transpose the matrix (`matrix = matrix'`)
2. Then reverse each row (`matrix(:, i) = flip(matrix(:, i))`)
3. For an in-place transpose, swap elements across the diagonal

</details>

## Examples

```matlab
% Example 1: 3x3
Input:  [1 2 3; 4 5 6; 7 8 9]
Output: [7 4 1; 8 5 2; 9 6 3]

% Example 2: 2x2
Input:  [1 2; 3 4]
Output: [3 1; 4 2]

% Example 3: 1x1
Input:  [42]
Output: [42]

% Example 4: Non-square → error
Input:  [1 2 3; 4 5 6]
Output: error('Matrix must be square')
```

## MATLAB Lesson
- **In-place operations** — modify the input directly instead of copying (saves memory)
- **`'` is complex-conjugate transpose**, `.'` is plain transpose — use `.'` for real matrices
- **`flip()`** reverses along a dimension — `flip(v)` reverses a vector, `flip(M, 2)` reverses columns
