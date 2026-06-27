import sys
import os
import copy
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> List[str]:
    if HOME_PC:
        board = ['o  ', '  O', '  *']
    else:
        n = int(input())
        board = [input() for _ in range(n)]

    if print_input:
        myPrint(board)

    board = [list(line) for line in board]
    return board


def mirror_right(board: List) -> List:
    res = []
    for line in board:
        r = mirror_line_right(line)
        res.append(r)
    return res
    

def mirror_line_right(line: list) -> list:
    lookup = {"(": ")", "{": "}", "[": "]", "<": ">", ")": "(", "}": "{", "]": "[", ">": "<", "/": "\\", "\\": "/"}
    res = line
    for c in reversed(line[:-1]):
        if c in lookup:
            res += lookup[c]
        else:
            res += c
    return res
    
def mirror_line_down(line: list) -> list:
    lookup = {"^": "v", "A": "V", "w": "m", "W": "M", "u": "n", "/": "\\", "\\": "/", "V": "A", "m": "w", "v": "^", "M": "W", "n": "u"}
    res = []
    for c in line:
        if c in lookup:
            res += lookup[c]
        else:
            res += c
    return res

def mirror_down(board: List) -> List:
    res = [line for line in board]
    for line in reversed(board[:-1]):
        r = mirror_line_down(line)
        res.append(r)
    return res


def stitch_lines_together(l):
    l = "".join(l)
    return "|" + l + "|" + l + "|"

def create_2_x_2_tile(board: List) -> List:
    def _create_lid(board):
        res = "+" + "-" * len(board[0]) + "+" + "-" * len(board[0]) + "+"
        return res
    
    lid = _create_lid(board)
    
    res = [lid]

    for l in board:
        r = stitch_lines_together(l)
        res.append(r)
    
    res.append(lid)

    for l in board:
        r = stitch_lines_together(l)
        res.append(r)
    
    res.append(lid)
    
    return res


def print_board(board: List) -> None:
    for line in board:
        print("".join(line))

# ********************************************************

board = get_start_parameters(print_input=False)
board = mirror_right(board)
board = mirror_down(board)

res = create_2_x_2_tile(board)

for line in res:
    print(line)
