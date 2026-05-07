# 04 — Game of Life

**Difficulty:** Medium  
**Category:** Simulation / 2D Grid

## Problem

Implement one step of Conway's Game of Life on an m×n binary grid where:
- `1` = live cell, `0` = dead cell

**Rules** (applied simultaneously):
1. Live cell with < 2 live neighbors → dies (underpopulation)
2. Live cell with 2 or 3 live neighbors → lives on
3. Live cell with > 3 live neighbors → dies (overpopulation)
4. Dead cell with exactly 3 live neighbors → becomes alive (reproduction)

Neighbors are the 8 surrounding cells. Cells on the edge have fewer neighbors.

## Signature

```matlab
function nextGrid = gameOfLife(grid)
```

## Rules
- Return a **new** matrix (do not mutate input)
- Handle edge cells correctly
- Preallocate the output

## Hint
<details><summary>Click if stuck</summary>

Use `conv2()` with a kernel of ones(3,3) to count neighbors, then subtract the center cell. Or manually loop with explicit boundary checks.

For `conv2`: `neighbors = conv2(grid, ones(3), 'same') - grid;`

</details>

## Examples

```matlab
% Example 1: Blinker (oscillator)
% Period-2 blinker — horizontal → vertical
Input:  [0 0 0 0 0; 0 0 1 0 0; 0 0 1 0 0; 0 0 1 0 0; 0 0 0 0 0]
Output: [0 0 0 0 0; 0 0 0 0 0; 0 1 1 1 0; 0 0 0 0 0; 0 0 0 0 0]

% Example 2: Block (still life — stays the same)
Input:  [1 1; 1 1]
Output: [1 1; 1 1]

% Example 3: Single live cell → dies
Input:  [0 0 0; 0 1 0; 0 0 0]
Output: zeros(3)

% Example 4: Empty grid
Input:  zeros(4)
Output: zeros(4)
```

## MATLAB Lesson
- **`conv2()`** for convolution-based neighbor counting (fast, concise)
- **Logical indexing** — `grid == 1`, `grid == 0` to apply rules selectively
- **Edge behavior** — `conv2(..., 'same')` handles padding automatically
- **Preallocation** — `nextGrid = zeros(size(grid))`
