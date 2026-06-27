from typing import Any, Tuple, List
import sys
import math


Point = Tuple[int, int]
Board = dict[Point, Any]
PointSet = frozenset[Point]


def read_web_input():
    x, y = [int(i) for i in input().split()]
    lines = [input() for _ in range(y)]
    return lines


def read_file_input():
    lines = ["1234567", "1234567", "1234567", "1234567", "7653214", "4127653"]
    return lines


def parse(lines: list[str]) -> Board:
    board: Board = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            p = (r, c)
            board[p] = char
    return board


def find_island(board: Board, start: Point) -> set[Point]:
    """Find all points in the same island as start using DFS. Orthogonal exploration. Uses Board definition as simple dict."""
    match_char = board.get(start)
    visited = set()
    stack = [start]
    while stack:
        p = stack.pop()
        if p in visited or p not in board or board[p] != match_char:
            continue
        visited.add(p)
        r, c = p
        stack.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])
    return visited


def find_all_islands(board: Board) -> list[PointSet]:
    """Find all islands in the board. Returns a list of sets of points."""
    visited = set()
    islands = []
    for p in board:
        if p not in visited:
            island = find_island(board, p)
            islands.append(island)
            visited.update(island)
    return islands


# *************************************************

lines = read_file_input()
board = parse(lines)
islands = find_all_islands(board)

counter = dict()
for island in islands:
    char = list(island)[0]
    char = board[char]
    if char not in counter:
        counter[char] = 0
    counter[char] += 1
keys = sorted(counter.keys())
if keys == ["0"]:
    print("No coloring today")
else:
    for key in keys:
        if key == "0":
            continue
        print(f"{key} -> {counter[key]}")
