import sys
import os
from typing import Any, Tuple, List
from Point2D import Point2D
from collections import deque

HOME_PC = True


# Get Game Start Parameters
def get_start_parameters():
    def parse(data: List[str]):
        board = set()
        start = None
        target = None
        for r, line in enumerate(data):
            for c, char in enumerate(line):
                p = Point2D(r, c)
                if char == "^":
                    board.add(p)
                if char == "B":
                    start = p
                if char == "M":
                    target = p
        return board, start, target

    if HOME_PC:
        data2 = [
            "^^^^^^^^^^",
            "^B        ",
            "^^^^^^^^^^",
            "^^^^^^^^^^",
            "^^^^^^^^^^",
            "^^^^^^^^^^",
            "^^^^^^^^^^",
            "^^^^^^^^^^",
            "^M        ",
            "^^^^^^^^^^",
        ]

        data = [
            "^^^^^^^^^^ ^^^^^^^^^ ",
            "^M        ^         ^",
            "^ ^^^^ ^^ ^  ^^^^^^ ^",
            "^     ^     ^       ^",
            " ^^^  ^ ^^  ^ ^^^^ ^^",
            "^   ^ ^   ^ ^     ^ ^",
            "^ ^ ^  ^^ ^  ^^^^ ^^^",
            "^ ^   ^     ^     ^^^",
            "^  ^^^  ^^^^ ^^^^ ^^^",
            "^                B^^^",
            " ^^^^^^^^^^^^^^^^^ ^^",
        ]
    else:
        h, w = [int(i) for i in input().split()]
        data = [input() for _ in range(h)]

    board, start, target = parse(data)
    return board, start, target


def get_neighbours(current: Point2D) -> List[Point2D]:
    neighbors = [p for p in current.neighbors_4() if p not in board]
    N = current.up()
    E = current.right()
    S = current.down()
    W = current.left()
    NE = current.up().right()
    SE = current.down().right()
    SW = current.down().left()
    NW = current.up().left()
    if NE not in board and (N not in board or E not in board):
        neighbors.append(NE)
    if SE not in board and (S not in board or E not in board):
        neighbors.append(SE)
    if SW not in board and (S not in board or W not in board):
        neighbors.append(SW)
    if NW not in board and (N not in board or W not in board):
        neighbors.append(NW)
    return neighbors


def bfs(start, target):
    entry = (start, 0)
    stack = deque([entry])
    visited = {start}
    while stack:
        current, steps = stack.popleft()
        if current == target:
            return steps
        neighbours = get_neighbours(current)
        for n in neighbours:
            if n not in visited:
                stack.append((n, steps + 1))
                visited.add(n)


# ********************************************************

board, start, target = get_start_parameters()
r = bfs(start, target)
if r == 1:
    print("1 league")
else:
    print(f"{r} leagues")
