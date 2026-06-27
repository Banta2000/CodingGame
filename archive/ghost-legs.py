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
        data = [
            "A  B  C  D  E  F  G  H  I  J",
            "|--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |--|  |--|  |",
            "|  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |--|  |--|  |",
            "0  1  2  3  4  5  6  7  8  9",
        ]

        data = [
            "~  !  @  #  $  %  ^  &  *  (  )  +  `  1  2  3  4  5  6  7  8  9  0  =  \\  /",
            "|  |--|  |  |--|  |  |--|  |--|  |  |--|  |  |  |--|  |--|  |  |--|  |  |--|",
            "|--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |  |--|  |--|  |  |  |--|  |",
            "|  |--|  |--|  |  |  |  |  |--|  |--|  |  |  |  |--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |--|",
            "|--|  |  |  |  |--|  |  |--|  |  |  |  |--|  |--|  |--|  |--|  |--|  |--|  |",
            "|  |--|  |  |--|  |--|  |  |--|  |  |--|  |--|  |  |  |--|  |  |--|  |--|  |",
            "|  |  |  |--|  |--|  |--|  |  |  |--|  |--|  |  |--|  |--|  |--|  |--|  |--|",
            "|--|  |  |  |--|  |--|  |--|  |  |  |--|  |--|  |--|  |  |--|  |  |--|  |--|",
            "|  |  |--|  |  |  |  |--|  |  |--|  |  |  |  |  |  |--|  |  |  |--|  |--|  |",
            "|  |  |  |--|  |  |--|  |  |  |  |--|  |  |--|  |--|  |--|  |--|  |--|  |--|",
            "|  |--|  |--|  |  |  |  |  |--|  |--|  |  |  |  |--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |--|",
            "|--|  |  |  |  |--|  |  |--|  |  |  |  |--|  |--|  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |  |--|  |  |  |--|  |  |--|",
            "|  |--|  |  |--|  |--|  |  |--|  |  |--|  |--|  |  |  |--|  |  |--|  |--|  |",
            "|  |--|  |  |--|  |  |  |  |--|  |  |--|  |  |--|  |--|  |--|  |--|  |--|  |",
            "|--|  |  |--|  |  |  |  |--|  |  |--|  |--|  |  |--|  |--|  |--|  |--|  |--|",
            "|--|  |--|  |  |  |--|  |--|  |--|  |  |  |--|  |  |--|  |  |  |--|  |  |--|",
            "|  |--|  |  |--|  |  |--|  |--|  |  |  |--|  |--|  |  |--|  |--|  |--|  |--|",
            "|  |  |  |--|  |  |--|  |  |  |  |--|  |  |--|  |  |--|  |--|  |--|  |--|  |",
            "|--|  |--|  |--|  |--|  |--|  |--|  |--|  |--|  |--|  |--|  |  |  |  |  |--|",
            "a  A  b  B  c  C  d  D  e  E  f  F  g  G  h  H  i  I  j  J  k  K  l  L  m  M",
        ]

    else:
        w, h = [int(i) for i in input().split()]
        data = [input() for _ in range(h)]

    max_width = max(len(line) for line in data)
    max_length = len(data)
    board = {}
    for r in range(max_length):
        for c in range(max_width):
            p = r, c
            board[p] = data[r][c]
    
    starts = {}
    for c in range(max_width):
        if data[0][c] != " ":
            starts[data[0][c]] = 0, c
        
    if print_input:
        myPrint(data)

    return board, starts


def explore_path(p):
    # print_board(board, {p})
    max_rows = max(k[0] for k in board.keys())
    r, c = p
    if r == max_rows:
        return board[p]
    left = r, c - 1
    right = r, c + 1
    down = r + 1, c
    left_and_down = r + 1, c - 3
    right_and_down = r + 1, c + 3
    if left in board and board[left] == "-":
        return explore_path(left_and_down)
    elif right in board and board[right] == "-":
        return explore_path(right_and_down)
    else:
        return explore_path(down)


# Print a dictionary board made of points and chars
def print_board(board, visited):
    os.system("cls")
    if visited is None:
        visited = set()
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"
    num_rows = max(k[0] for k in board.keys()) + 1
    num_cols = max(k[1] for k in board.keys()) + 1

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


# ********************************************************

board, starts = get_start_parameters(print_input=False)

for start in starts:
    r = explore_path(starts[start])
    print(f"{start}{r}")
