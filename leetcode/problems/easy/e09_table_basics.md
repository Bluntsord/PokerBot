# E09 — Table Basics

**Difficulty:** Easy  
**Category:** Tables

## Problem

You're given three parallel arrays — `names` (cell array of strings), `ages` (numeric), `scores` (numeric) — representing people. Build a table from them, then return:
1. `T` — the table with columns `Name`, `Age`, `Score`
2. `averageScore` — the mean of the Score column
3. `oldestName` — the Name of the person with the max Age

## Signature

```matlab
function [T, averageScore, oldestName] = buildTable(names, ages, scores)
```

## Rules
- Use `table()` to construct
- Access columns with `T.Score` or `T{:, 'Score'}`
- Use `max()` to find the oldest

## Examples

```matlab
names = {'Alice', 'Bob', 'Carol'};
ages  = [25 30 22];
scores = [88 92 85];

T.Name    → {'Alice'; 'Bob'; 'Carol'}
averageScore → 88.3333
oldestName → 'Bob'
```

## MATLAB Lesson
- **`table(A, B, C, 'VariableNames', {...})`** — create table from arrays
- **`T.ColumnName`** — dot-access a column (like a struct field)
- **`mean(T.Score)`** — compute stats on a table column
- **Find row by condition**: `T.Name(T.Age == max(T.Age))`
