# E10 — Table Filter

**Difficulty:** Easy  
**Category:** Tables / Logical Indexing

## Problem

Given a table `T` with columns `Name` (cellstr), `Score` (double), and a threshold `minScore`, return:
1. `passed` — a new table containing only rows where Score >= minScore
2. `failedNames` — cell array of Names that failed

## Signature

```matlab
function [passed, failedNames] = filterTable(T, minScore)
```

## Rules
- Use logical indexing: `T(T.Score >= minScore, :)`
- Use logical indexing to extract names: `T.Name(~logical_index)`

## Examples

```matlab
Name = {'A'; 'B'; 'C'; 'D'}; Score = [75; 45; 90; 55];
T = table(Name, Score);

[passed, failed] = filterTable(T, 60)
passed  → table with rows A, C
failed  → {'B'; 'D'}
```

## MATLAB Lesson
- **`T(condition, :)`** — keep rows where condition is true
- **`T(condition, 'ColumnName')`** — extract column values for matching rows
- **`~` negation** — `~condition` flips true/false for "failed" filter
