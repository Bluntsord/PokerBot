# H03 — Fibonacci (DP / Memoization)

**Difficulty:** Hard  
**Category:** Dynamic Programming

## Problem

Compute the nth Fibonacci number using **memoization** (top-down DP with caching). `F(1)=1, F(2)=1, F(n)=F(n-1)+F(n-2)`.

Do **not** use a simple loop. Use recursion with a `containers.Map` to cache results.

## Signature

```matlab
function result = fibonacci(n)
```

## Rules
- Use recursion — the function calls itself
- Use `containers.Map` to cache already-computed values
- Handle `n <= 0` by throwing an error

## Examples

```matlab
fibonacci(1)   → 1
fibonacci(2)   → 1
fibonacci(10)  → 55
fibonacci(30)  → 832040
```

## MATLAB Lesson
- **`containers.Map`** — MATLAB's hashmap/dictionary
  ```matlab
  cache = containers.Map('KeyType', 'double', 'ValueType', 'double');
  cache(key) = value;
  isKey(cache, key)   % check if cached
  ```
- **Recursion in MATLAB** — functions can call themselves (set recursion limit with `set(0,'RecursionLimit', N)` if needed)
- **Memoization pattern** — check cache first, compute only if missing
