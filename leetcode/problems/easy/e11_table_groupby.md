# E11 — Table GroupBy

**Difficulty:** Medium  
**Category:** Tables / Grouping

## Problem

Given a table `T` with columns `Department` (cellstr) and `Salary` (double), return:
1. `departments` — unique department names, sorted
2. `avgSalaries` — average salary per department (same order as departments)
3. `bestPaid` — name of the department with the highest average salary

Do **not** use `groupsummary` or `findgroups`. Use `unique()` and a loop.

## Signature

```matlab
function [departments, avgSalaries, bestPaid] = groupByDepartment(T)
```

## Examples

```matlab
Dept = {'Eng'; 'Sales'; 'Eng'; 'Sales'; 'Mktg'};
Salary = [100; 80; 120; 90; 70];
T = table(Dept, Salary);

departments → {'Eng'; 'Mktg'; 'Sales'}
avgSalaries → [110; 70; 85]
bestPaid   → 'Eng'
```

## MATLAB Lesson
- **`unique(T.Department)`** — distinct departments
- **`ismember(T.Department, dept)`** — logical mask for rows in a specific dept
- **`mean(T.Salary(mask))`** — average salary for matching rows
- **`[~, idx] = max(...)`** — find index of max value, then use it to index into departments
