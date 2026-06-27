from typing import Any, Tuple, List


Point = Tuple[int, int]
Board = dict[Point, Any]
PointSet = frozenset[Point]


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
