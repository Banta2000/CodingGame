import sys
import os
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
def get_start_parameters(print_input: bool = False) -> Game:
    if HOME_PC:
        w=8
        h=3
        t=[10, 10, 4]
    else:
        w = int(input())
        h = int(input())
        t = input()
        t = [int(x) for x in t.split(" ")]

    if print_input:
        myPrint(f"{w=}")
        myPrint(f"{h=}")
        myPrint(f"{t=}")
        
    return w, h, t


# ********************************************************
HOME_PC = True
ink: bool = True
w, h, t = get_start_parameters(print_input=False)

s = ""
mapper = {True: "*", False: " "}
for num in t:
    s += mapper[ink] * num
    ink = not ink
remaining = w * h - len(s)
s += mapper[ink] * remaining

lines = [s[i:i+w] for i in range(0, len(s), w)]
lines = ["|"+line+"|" for line in lines]

for line in lines:
    print(line)
