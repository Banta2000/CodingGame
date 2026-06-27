from typing import Any, Tuple, List
from collections import deque


def get_start_parameters(demo: int | None = None):
    if not demo:
        demo = int(input())
    return demo


def bfs(target: int):
    # Performs a BFS, at every step i can either +1, -1 or *2
    stack = deque()
    stack.append((0, 0))
    visited = set()
    while stack:
        curr, steps = stack.popleft()
        if curr == target:
            return steps
        options = [curr - 1, curr + 1, curr * 2]
        for option in options:
            if option > 0 and option not in visited:
                visited.add(option)
                stack.append((option, steps + 1))


# ********************************************************

N = get_start_parameters()
res = bfs(N)
print(res)
