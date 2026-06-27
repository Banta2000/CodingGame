import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"
Point = Tuple[int, int]
Board = dict[Point, Any]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Game:
    if HOME_PC:
        board = {(0, "0"): 0, (1, "0"): 0, (1, "2"): 2, (2, "0"): 0}
        board = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (1, 0): 0, (1, 1): 2, (1, 2): 0, (2, 0): 0, (2, 1): 0, (2, 2): 0}

        board = {
            (0, 0): 0,
            (0, 1): 0,
            (0, 2): 0,
            (0, 3): 0,
            (0, 4): 0,
            (0, 5): 0,
            (0, 6): 0,
            (0, 7): 0,
            (0, 8): 0,
            (0, 9): 0,
            (0, 10): 0,
            (0, 11): 0,
            (0, 12): 0,
            (1, 0): 0,
            (1, 1): 9,
            (1, 2): 9,
            (1, 3): 8,
            (1, 4): 7,
            (1, 5): 7,
            (1, 6): 7,
            (1, 7): 7,
            (1, 8): 7,
            (1, 9): 8,
            (1, 10): 9,
            (1, 11): 9,
            (1, 12): 0,
            (2, 0): 0,
            (2, 1): 9,
            (2, 2): 9,
            (2, 3): 5,
            (2, 4): 5,
            (2, 5): 5,
            (2, 6): 6,
            (2, 7): 5,
            (2, 8): 5,
            (2, 9): 5,
            (2, 10): 9,
            (2, 11): 9,
            (2, 12): 0,
            (3, 0): 0,
            (3, 1): 8,
            (3, 2): 5,
            (3, 3): 5,
            (3, 4): 5,
            (3, 5): 5,
            (3, 6): 6,
            (3, 7): 5,
            (3, 8): 5,
            (3, 9): 5,
            (3, 10): 5,
            (3, 11): 8,
            (3, 12): 0,
            (4, 0): 0,
            (4, 1): 7,
            (4, 2): 5,
            (4, 3): 5,
            (4, 4): 7,
            (4, 5): 6,
            (4, 6): 6,
            (4, 7): 6,
            (4, 8): 7,
            (4, 9): 5,
            (4, 10): 5,
            (4, 11): 7,
            (4, 12): 0,
            (5, 0): 0,
            (5, 1): 7,
            (5, 2): 5,
            (5, 3): 5,
            (5, 4): 7,
            (5, 5): 6,
            (5, 6): 6,
            (5, 7): 6,
            (5, 8): 7,
            (5, 9): 5,
            (5, 10): 5,
            (5, 11): 7,
            (5, 12): 0,
            (6, 0): 0,
            (6, 1): 7,
            (6, 2): 6,
            (6, 3): 5,
            (6, 4): 7,
            (6, 5): 6,
            (6, 6): 6,
            (6, 7): 6,
            (6, 8): 7,
            (6, 9): 5,
            (6, 10): 5,
            (6, 11): 6,
            (6, 12): 0,
            (7, 0): 0,
            (7, 1): 7,
            (7, 2): 5,
            (7, 3): 5,
            (7, 4): 8,
            (7, 5): 7,
            (7, 6): 7,
            (7, 7): 7,
            (7, 8): 8,
            (7, 9): 5,
            (7, 10): 5,
            (7, 11): 7,
            (7, 12): 0,
            (8, 0): 0,
            (8, 1): 7,
            (8, 2): 5,
            (8, 3): 5,
            (8, 4): 4,
            (8, 5): 4,
            (8, 6): 3,
            (8, 7): 4,
            (8, 8): 4,
            (8, 9): 5,
            (8, 10): 5,
            (8, 11): 7,
            (8, 12): 0,
            (9, 0): 0,
            (9, 1): 7,
            (9, 2): 5,
            (9, 3): 5,
            (9, 4): 4,
            (9, 5): 4,
            (9, 6): 3,
            (9, 7): 4,
            (9, 8): 4,
            (9, 9): 5,
            (9, 10): 5,
            (9, 11): 8,
            (9, 12): 0,
            (10, 0): 0,
            (10, 1): 9,
            (10, 2): 9,
            (10, 3): 8,
            (10, 4): 7,
            (10, 5): 7,
            (10, 6): 7,
            (10, 7): 7,
            (10, 8): 7,
            (10, 9): 8,
            (10, 10): 9,
            (10, 11): 9,
            (10, 12): 0,
            (11, 0): 0,
            (11, 1): 9,
            (11, 2): 9,
            (11, 3): 1,
            (11, 4): 1,
            (11, 5): 2,
            (11, 6): 3,
            (11, 7): 2,
            (11, 8): 1,
            (11, 9): 1,
            (11, 10): 9,
            (11, 11): 9,
            (11, 12): 0,
            (12, 0): 0,
            (12, 1): 0,
            (12, 2): 0,
            (12, 3): 0,
            (12, 4): 0,
            (12, 5): 0,
            (12, 6): 0,
            (12, 7): 0,
            (12, 8): 0,
            (12, 9): 0,
            (12, 10): 0,
            (12, 11): 0,
            (12, 12): 0,
        }

        board = {
            (0, 0): 0,
            (0, 1): 0,
            (0, 2): 0,
            (0, 3): 0,
            (0, 4): 0,
            (1, 0): 0,
            (1, 1): 0,
            (1, 2): 2,
            (1, 3): 2,
            (1, 4): 0,
            (2, 0): 0,
            (2, 1): 2,
            (2, 2): 3,
            (2, 3): 2,
            (2, 4): 0,
            (3, 0): 0,
            (3, 1): 2,
            (3, 2): 2,
            (3, 3): 0,
            (3, 4): 0,
            (4, 0): 0,
            (4, 1): 0,
            (4, 2): 0,
            (4, 3): 0,
            (4, 4): 0,
        }
    else:
        board = {}
        n = int(input())
        for r in range(n):
            for c, char in enumerate(input().split()):
                board[r, c] = int(char)

    max_row = max(k[0] for k in board.keys())
    max_col = max(k[1] for k in board.keys())
    midpoint = (max_row // 2, max_col // 2)

    if print_input:
        myPrint(board, midpoint)

    return board, midpoint


# Print a dictionary board made of points and chars
def print_board(board: Board, visited=set()) -> None:
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"
    rows = max(k[0] for k in board.keys()) + 1
    cols = max(k[1] for k in board.keys()) + 1

    for r in range(rows):
        for c in range(cols):
            p = r, c
            if p in visited:
                myPrint(RED + board[p] + RESETCOL, end="")
            elif p in board:
                myPrint(board[p], end="")
            else:
                myPrint(" ", end="")
        myPrint()
    myPrint()


def dfs(pos: Point, board: Board) -> None:
    def _get_pos_neighbours(p: Point) -> list[Point]:
        r, c = p
        return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    
    if board[pos] == -1:
        return False

    max_row = max(k[0] for k in board.keys())
    max_col = max(k[1] for k in board.keys())
    r, c = pos
    if r == 0 or r == max_row or c == 0 or c == max_col:
        return True

    curr_val = board[pos]
    board[pos] = -1

    neighbours = _get_pos_neighbours(pos)
    neighbours = [n for n in neighbours if n in board and board[n] != -1 and abs(board[n] - curr_val) <= 1]
    for pos in neighbours:
        if dfs(pos, board):
            return True
    return False


# ********************************************************

board, midpoint = get_start_parameters(print_input=True)
print_board(board)

r = dfs(midpoint, board)
print("yes" if r else "no")
