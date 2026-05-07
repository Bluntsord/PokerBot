# 01 — Matrix Multiplication

**Difficulty:** Easy  
**Category:** Matrix Operations

## Problem

Implement matrix multiplication **without using the `*` operator**. Given two matrices `A` (m×k) and `B` (k×n), return their product `C = A × B` where each element is:

```
C(i, j) = sum_{p=1}^{k} A(i, p) * B(p, j)
```

## Signature

```matlab
function C = multiply(A, B)
```

## Rules
- Do **not** use `A * B` anywhere in your code
- You may use `size()`, `zeros()`, and `sum()`
- Handle dimension mismatch by throwing an error via `error('message')`
- Preallocate your output matrix (hint: `zeros(m, n)`)

## Examples

```matlab
% Example 1: Standard 2x2 * 2x2
A = [1 2; 3 4];
B = [5 6; 7 8];
% Expected: [19 22; 43 50]

% Example 2: 3x2 * 2x3 = 3x3
A = [1 0; 2 1; 0 3];
B = [1 2 3; 0 1 1];
% Expected: [1 2 3; 2 5 7; 0 3 3]

% Example 3: Identity — A * eye(k) = A
A = [4 2 1; 3 5 6];
B = eye(3);
% Expected: A

% Example 4: Row × Column = scalar
A = [1 2 3];
B = [4; 5; 6];
% Expected: 32

% Example 5: Dimension mismatch → error
A = [1 2; 3 4]; B = [1 2 3];
% Expected: error
```

## MATLAB Lesson
- **Preallocation** — always `zeros(m,n)` before filling a matrix in loops
- **Triple-nested loops** — understand `i`, `j`, `p` indexing for matrix multiply
- **`size(A, 2)`** returns columns, `size(B, 1)` returns rows — compare these for dimension check
