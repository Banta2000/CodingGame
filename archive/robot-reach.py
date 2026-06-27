import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        r = 36
        c = 27
        t = 12
    else:
        r = int(input())
        c = int(input())
        t = int(input())

    if print_input:
        myPrint("r:", r)
        myPrint("c:", c)
        myPrint("t:", t)

    return r, c, t


def create_board(ROWS: int, COLS: int):
    board = {}
    for r in range(ROWS):
        for c in range(COLS):
            p = r, c
            c_val = sum([int(i) for i in str(c)])
            r_val = sum([int(i) for i in str(r)])
            board[p] = c_val + r_val
    return board


def dfs(board, p, threshold, visited):
    def _get_neighbours(p):
        r, c = p
        return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

    if p in visited:
        return visited
    visited.add(p)
    neighbours = _get_neighbours(p)
    neighbours = [n for n in neighbours if n in board and board[n] <= threshold]
    for n in neighbours:
        r = dfs(board, n, threshold, visited)
        visited.update(r)
    return visited


# ********************************************************

ROWS, COLS, t = get_start_parameters(print_input=True)
board = create_board(ROWS, COLS)
visited = dfs(board, (0, 0), t, set())
print(len(visited))
