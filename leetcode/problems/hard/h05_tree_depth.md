# H05 — Tree Max Depth

**Difficulty:** Hard  
**Category:** Trees / Recursion

## Problem

A binary tree node is a **struct** with fields:
- `val`   — integer value
- `left`  — left child (struct, or empty `[]`)
- `right` — right child (struct, or empty `[]`)

Return the **maximum depth** (number of nodes on the longest root-to-leaf path).

## Signature

```matlab
function d = maxDepth(root)
```

## Rules
- Use recursion
- An empty root `[]` has depth 0
- A single node has depth 1

## Examples

```matlab
root = struct('val',1, 'left', [], 'right', []);
maxDepth(root)  → 1

% Tree:   1
%        / \
%       2   3
%      /
%     4
root.left  = struct('val',2, 'left', struct('val',4,'left',[],'right',[]), 'right', []);
root.right = struct('val',3, 'left', [], 'right', []);
maxDepth(root)  → 3
```

## MATLAB Lesson
- **Structs in MATLAB** — `struct('field', value, ...)`, access with `root.left`
- **`isempty()`** — check if a child exists: `isempty(root.left)`
- **Recursion** — `1 + max(maxDepth(root.left), maxDepth(root.right))`
- **Struct arrays vs single structs** — use `isempty()` not `isempty(fieldnames(...))` for empty `[]`
