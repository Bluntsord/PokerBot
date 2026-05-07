# H02 — Connected Components

**Difficulty:** Hard  
**Category:** Graphs / DFS

## Problem

Given an **undirected** graph as an n×n adjacency matrix `adj` (symmetric, `adj(i,j)=1` means edge between i and j), return:
1. `numComponents` — number of connected components
2. `labels` — vector length n, where `labels(i)` is the component ID (1 through numComponents) of node i

## Signature

```matlab
function [numComponents, labels] = connectedComponents(adj)
```

## Rules
- Use DFS or BFS to explore from each unvisited node
- Do **not** use `graph` or `conncomp` toolbox functions
- The graph is undirected (matrix is symmetric)

## Example

```matlab
adj = [0 1 0 0 0;
       1 0 0 0 0;
       0 0 0 1 1;
       0 0 1 0 1;
       0 0 1 1 0];
% Nodes: {1,2} form component 1, {3,4,5} form component 2
[num, labs] = connectedComponents(adj)
num   → 2
labs  → [1 1 2 2 2]
```

## MATLAB Lesson
- **DFS recursion** — MATLAB supports recursion (watch stack depth)
- **Symmetric matrix** — `adj(i,:)` gives all neighbors of node i
- **Component labeling** — assign incrementing IDs to each BFS/DFS start
