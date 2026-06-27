import os
from typing import Any, Tuple
from cgutils.coding_game_helper import CodingGameHelper
from collections import deque


Point = Tuple[int, int, int]
Board = dict[Point, Any]


def read_input(CGH: CodingGameHelper) -> Tuple[Board, Point, Point]:
    first = [int(x) for x in CGH.input().split(" ")]
    second = int(CGH.input())
    lines = [CGH.input() for _ in range(second)]
    lines = lines[1:]
    floors = []
    floor = []
    for line in lines:
        if line == "":
            floors.append(floor)
            floor = []
            continue
        floor.append(line)
    floors.append(floor)

    start: Point = (0, 0, 0)
    target: Point = (0, 0, 0)
    board: Board = {}
    for z, floor in enumerate(floors):
        for y, line in enumerate(floor):
            for x, c in enumerate(line):
                if c == "A":
                    start = (x, y, z)
                if c == "S":
                    target = (x, y, z)
                board[(x, y, z)] = c

    return board, start, target


def get_orthogonal(p: Point) -> list[Point]:
    x, y, z = p
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


def bfs(board: Board, start: Point, target: Point) -> str:
    queue = deque([start])
    visited: Board = {start: None}
    curr: Point = start
    while queue:
        curr = queue.popleft()
        if curr == target:
            break
        candidates = get_orthogonal(curr)
        candidates = [c for c in candidates if c in board and board[c] != "#"]
        for c in candidates:
            if c not in visited:
                visited[c] = curr
                queue.append(c)

    if curr != target:
        return "NO PATH"
    steps = 0
    while curr != start:
        curr = visited[curr]
        steps += 1
    return str(steps)


# ********************************************************

for case_nr in range(1, 11):
    CGH = CodingGameHelper(case_nr, __file__)
    board, start, target = read_input(CGH)
    steps = bfs(board, start, target)
    CGH.add_output_line(steps)
    CGH.assert_output()


# https://www.codingame.com/ide/puzzle/dungeon-3d
