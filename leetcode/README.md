# LeetCode-Style MATLAB Problems

## Structure

```
leetcode/
  problems/{easy,medium,hard}/   ← problem descriptions
  solutions/{easy,medium,hard}/  ← reference answers
  user/{easy,medium,hard}/       ← your implementations
  tests/{easy,medium,hard}/      ← test runners
```

## Quick Run

```matlab
cd('leetcode/tests/easy');   runEasyTest           % easy: your solutions
cd('leetcode/tests/easy');   runEasyTest(3)        % just E03
cd('leetcode/tests/easy');   runEasyTest('answer') % easy: reference

cd('leetcode/tests/medium'); test_all              % medium: your solutions
cd('leetcode/tests/medium'); runTestP01(3)         % just P01 case 3

cd('leetcode/tests/hard');   runHardTest           % hard: your solutions
cd('leetcode/tests/hard');   runHardTest('answer') % hard: reference
```

## Learning Path (do in this order)

### Easy — Syntax Fundamentals
| # | Topic | Skill |
|---|-------|-------|
| E01 | Array Sum | Loops, linear indexing |
| E02 | Find Max | Tracking state, comparisons |
| E03 | Count Where | `if/elseif`, multiple outputs |
| E04 | Reverse Array | Index arithmetic, preallocation |
| E05 | Dot Multiply | Element-wise, size check |
| E06 | Cell Basics | `C{k}`, `isnumeric()` |
| E07 | Set Membership | `ismember()`, `intersect()`, `setdiff()` |
| E08 | Matrix Row/Col Ops | `M(i,:)`, `M(:,j)` slicing |
| E09 | Table Basics | `table()`, `T.colname` |
| E10 | Table Filter | Logical indexing on tables |
| E11 | Table GroupBy | `unique()`, `ismember()`, group-and-compute |

### Medium — Matrix Operations
| # | Topic | Skill |
|---|-------|-------|
| P01 | Matrix Multiplication | Triple loops, dimensions |
| P02 | Rotate Image | In-place, transpose |
| P03 | Spiral Order | Boundary tracking |
| P04 | Game of Life | Convolution, rules |

### Hard — Algorithms & Data Structures
| # | Topic | Skill |
|---|-------|-------|
| H01 | BFS on Adjacency Matrix | Queue, visited tracking |
| H02 | Connected Components | DFS/stack, component labeling |
| H03 | Fibonacci (DP) | Recursion, `containers.Map` memoization |
| H04 | LIS (DP) | Nested DP, `dp(i) = max(dp(j)+1)` |
| H05 | Tree Max Depth | Recursion on structs |
