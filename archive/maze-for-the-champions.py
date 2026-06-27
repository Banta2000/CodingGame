from typing import Tuple
from cgutils import board_utils, point_utils
from cgutils.coding_game_helper import CodingGameHelper
from collections import deque

Point = Tuple[int, int]
Board = dict


def read_input(CGH: CodingGameHelper) -> list[str]:
    _ = int(CGH.input())
    h = int(CGH.input())
    lines = [CGH.input() for _ in range(h)]
    return lines


def pointing_inwards(p: Point, board: Board) -> bool:
    char = board.get(p)
    rows = board_utils.num_rows(board)
    cols = board_utils.num_cols(board)
    if char == ">" and p[1] == 0:
        return True
    if char == "<" and p[1] == cols - 1:
        return True
    if char == "^" and p[0] == rows - 1:
        return True
    if char == "v" and p[0] == 0:
        return True
    return False


def pointing_outwards(p: Point, board: Board) -> bool:
    char = board.get(p)
    rows = board_utils.num_rows(board)
    cols = board_utils.num_cols(board)
    if char == "<" and p[1] == 0:
        return True
    if char == ">" and p[1] == cols - 1:
        return True
    if char == "v" and p[0] == rows - 1:
        return True
    if char == "^" and p[0] == 0:
        return True
    return False


def move_warrior(board: Board, pos: Point) -> list[Point]:
    res = point_utils.neighbors_4(pos)
    res = [p for p in res if p in board and board[p] != "#"]
    return res


def move_dwarf(board: Board, pos: Point) -> list[Point]:
    one_step = [point_utils.move(pos, d) for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
    two_step = [point_utils.move(pos, d) for d in [(-2, 0), (2, 0), (0, -2), (0, 2)]]
    res = []
    for c, n in zip(one_step, two_step):
        if c in board and board[c] != "#":
            res.append(c)
        if c in board and board[c] == "#" and n in board and board[n] != "#":
            res.append(c)
    return res


def move_mage(board: Board, pos: Point) -> list[Point]:
    res = []
    for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        curr = pos
        while True:
            nxt = point_utils.move(curr, delta)
            if nxt not in board or board[nxt] == "#":
                break
            curr = nxt
            res.append(curr)
    return res


def move_elf(board: Board, pos: Point) -> list[Point]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
    res = [point_utils.move(pos, d) for d in directions]
    res = [p for p in res if p in board and board[p] != "#"]
    return res


def bfs(board: Board, start: Point, target: Point, get_neighbors):
    queue = deque([start])
    visited = dict()
    visited[start] = None  # No parent for the start node
    while queue:
        curr = queue.popleft()
        if curr == target:
            break
        for n in get_neighbors(board, curr):
            if n not in visited:
                visited[n] = curr  # Set parent
                queue.append(n)

    # Reconstruct path
    curr = target
    path = []
    while curr is not None:
        path.append(curr)
        curr = visited[curr]
    path.reverse()
    return path


def find_start_and_target(board: Board) -> Tuple[Point, Point]:
    border_points = []
    border_points += board_utils.find(board, ">")
    border_points += board_utils.find(board, "<")
    border_points += board_utils.find(board, "^")
    border_points += board_utils.find(board, "v")
    start = [p for p in border_points if pointing_inwards(p, board)][0]
    target = [p for p in border_points if pointing_outwards(p, board)][0]
    return start, target


def imprint_path(board: Board, path: list[Point]):
    for i in range(len(path) - 1):
        curr = path[i]
        nxt = path[i + 1]
        if curr[0] == nxt[0] and curr[1] < nxt[1]:
            board[curr] = ">"
        elif curr[0] == nxt[0] and curr[1] > nxt[1]:
            board[curr] = "<"
        elif curr[1] == nxt[1] and curr[0] < nxt[0]:
            board[curr] = "v"
        elif curr[1] == nxt[1] and curr[0] > nxt[0]:
            board[curr] = "^"
        else:
            board[curr] = "o"


def get_cost(path: list, cost: int) -> int:
    return len(path) * cost


# ********************************************************

CGH = CodingGameHelper(2, __file__)
lines = read_input(CGH)
board = board_utils.create(lines)
start, target = find_start_and_target(board)

config = [
    ("WARRIOR", move_warrior, 2),
    ("DWARF", move_dwarf, 3),
    ("ELF", move_elf, 4),
    ("MAGE", move_mage, 5),
]

# Collect all results
results = []
for name, fun, cost_per_step in config:
    path = bfs(board, start, target, fun)
    cost = get_cost(path, cost_per_step)
    results.append((name, path, cost))

# Pick the best result
name, path, cost = min(results, key=lambda x: x[2])
print(name, cost)

imprint_path(board, path)
board_utils.print_board(board)
