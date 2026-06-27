HOME_PC = True

import sys
from typing import Any, Tuple, List

Game = dict[str, Any]
Point = Tuple[int, int]
Board = dict[Point, Any]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Print a dictionary board made of points and chars
def print_board(board: Board, visited=None) -> None:
    if visited is None:
        visited = set()
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"
    num_rows = max(k[0] for k in board) + 1
    num_cols = max(k[1] for k in board) + 1

    for r in range(num_rows):
        for c in range(num_cols):
            p = r, c
            if p in visited:
                print(RED + board[p] + RESETCOL, end="")
            elif p in board:
                print(board[p], end="")
            else:
                print(" ", end="")
        print()
    print()


# Get Game Start Parameters
def get_start_parameters() -> Game:
    if HOME_PC:
        True
    else:
        True

    return True


# ********************************************************

G = get_start_parameters()
