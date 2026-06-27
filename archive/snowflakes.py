from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper
from cgutils.polynomio import Polynomio


Point = Tuple[int, int]
Board = dict[Point, Any]
PointSet = frozenset[Point]


def read_input(reader: CodingGameHelper) -> list[str]:
    h, _ = [int(i) for i in reader.input().split()]
    return [reader.input() for _ in range(h)]


def parse_input(lines: list[str]) -> Board:
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
        # Add neighbors (up, down, left, right)
        stack.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])
    return visited


def find_all_islands(board: Board) -> list[PointSet]:
    """Find all islands in the board. Returns a list of sets of points."""
    visited = set()
    islands = []
    for p in board:
        if p not in visited:
            if board[p] == ".":
                visited.add(p)
                continue
            island = find_island(board, p)
            islands.append(island)
            visited.update(island)
    return islands


# ********************************************************


for case_nr in range(1, 4):
    CGH = CodingGameHelper(case_nr, __file__)
    lines = read_input(CGH)
    board = parse_input(lines)
    islands = find_all_islands(board)
    unique_shapes = set(Polynomio(island).normalized() for island in islands)
    CGH.add_output_line(len(islands))
    CGH.add_output_line(len(unique_shapes))
    CGH.assert_output(verbose=True)
