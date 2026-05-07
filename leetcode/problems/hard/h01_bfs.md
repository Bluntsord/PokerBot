# H01 — BFS on Adjacency Matrix

**Difficulty:** Hard  
**Category:** Graphs / BFS

## Problem

Given a **directed graph** as an n×n adjacency matrix `adj` (where `adj(i,j)=1` means edge i→j) and a start node `s` (1-indexed), return:
1. `order` — nodes in BFS traversal order from `s`
2. `distances` — shortest distance (in edges) from `s` to every node (`Inf` if unreachable)

## Signature

```matlab
function [order, distances] = bfs(adj, s)
```

## Rules
- BFS visits neighbors in ascending node order
- Use a queue — `[ ]` as an array, push with `[queue, node]`, pop front with `queue(1)` and `queue(1) = []`
- Do **not** use graph/toolbox functions

## Example

```matlab
adj = [0 1 1 0;
       0 0 0 1;
       0 0 0 1;
       0 0 0 0];
s = 1;
[order, dist] = bfs(adj, s)
order  → [1 2 3 4]
dist   → [0 1 1 2]
```

## MATLAB Lesson
- **Queue simulation** — use a numeric array: `queue(end+1) = v` to enqueue, `u = queue(1); queue(1)=[]` to dequeue
- **`Inf`** — initialize unknown distances
- **Boolean visited array** — `false(1, n)` for tracking
