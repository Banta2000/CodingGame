import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> list:
    if HOME_PC:
        board = [[1, 3, 2, 1], [1, 3, 2, 1], [1, 3, 2, 1], [1, 3, 2, 1]]
    else:
        board = []
        h = int(input())
        for _ in range(h):
            line = input()
            line = [int(x) for x in line.split(" ")]
            board.append(line)

    if print_input:
        myPrint(board)

    return board


def encode_line(line):
    lookup = {True: ".", False: "O"}
    flipflop = True
    res = ""
    for num in line:
        res += num * lookup[flipflop]
        flipflop = not flipflop
    return res


def encode_board(board):
    res = [encode_line(line) for line in board]
    return res


# ********************************************************

board = get_start_parameters(print_input=True)
res = encode_board(board)
line_len = [len(line) for line in res]
line_len = set(line_len)
if len(line_len) != 1:
    print("INVALID")
else:
    for line in res:
        print(line)
