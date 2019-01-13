# n-queen

This program find answer state of n-queens problem.
Answer of n-queens problem is a displacement that no two queens attack each other

## Supported Algorithms
* min conflict
* backtracking
* hill climbing

## Notice
Because number of cases of n-puzzle is to big, bfs, dfs and ids can take quite a long time.
A* work well at 8-puzzle. And also work well at 15-puzzle with -s option when small [count] used.

## Usage

```
$python3 main.py [Algorithm] [Number of queens]
```

## References
* For min conflict, look "Efficient Local Search with Conflict Minimization: A Case Study of the n-Queens Problem" by R. Sosic and J. Gu
* For others, look "Artificial Intelligence: A Modern Approach" by Stuart Russell and Peter Norvig
