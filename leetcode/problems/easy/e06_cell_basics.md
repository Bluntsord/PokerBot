# E06 — Cell Array Basics

**Difficulty:** Easy  
**Category:** Cell Arrays

## Problem

Given a cell array `C` containing mixed types (numbers, strings, arrays), return a structure with:
- `firstNumber` — the first numeric element
- `firstString` — the first char/string element
- `allNumeric` — a vector of all numeric elements concatenated

## Signature

```matlab
function result = cellBasics(C)
```

## Rules
- Use `isnumeric()` to check each cell's type
- Use `iscell()` in case you get confused about indexing
- Access cell contents with `C{k}`, not `C(k)`

## Examples

```matlab
C = {42, 'hello', [1 2 3], 'world', 7}
result.firstNumber  → 42
result.firstString  → 'hello'
result.allNumeric   → [42 1 2 3 7]
```

## MATLAB Lesson
- **`C{k}`** — gets the content inside cell k (curly braces)
- **`C(k)`** — gets a 1×1 cell wrapping the content (parentheses)
- **`cellfun`** — apply a function to every cell: `cellfun(@isnumeric, C)`
- **`[arr{:}]`** — concatenate all numeric cell contents
