import sys
import os
from typing import Any, Tuple, List

Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "True"
STRING = "abcdefghijklmnopqrstuvwxyz"


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
                print(board[p], end="")
            else:
                print("-", end="")
        print()


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        data = [
            "qrnwxqufaqpmehg",
            "gqpsdpeqovfjtbv",
            "azdizzjbedhsyzt",
            "mzbegprlfcbaxwv",
            "hoibquzhgbdrggu",
            "gynohfmijkdgpqt",
            "lwemjvulqlmnors",
            "eckkhvwucrblxwc",
            "hxunydbmsxdmpkh",
            "drdzvbronvfjlwz",
            "npnjnjqkfvupezb",
            "hvdaqvyrwhdtxbb",
            "nfpgaffyuefppae",
            "forhbqkezipkinq",
            "usxszgnwvwndzrl",
        ]
    else:
        n = int(input())
        data = [input() for _ in range(n)]

    board = {}
    initial_options = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            board[(row, col)] = char
            if char == "a":
                initial_options.append((row, col))
    return board, initial_options


def get_neighbours(p) -> List[Point]:
    r, c = p
    res = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    res = [x for x in res if x in BOARD]
    return res


def dfs(i, p, path, visited):
    if i == len(STRING) - 1:
        path.append(p)
        return True  # Found solution

    visited.add(p)
    path.append(p)
    next_letter = STRING[i + 1]
    for n in get_neighbours(p):
        if BOARD[n] == next_letter and n not in visited:
            if dfs(i + 1, n, path, visited):
                return True
    path.pop()
    visited.remove(p)
    return False


# ********************************************************

BOARD, initial_options = get_start_parameters()
for initial_option in initial_options:
    path = []
    visited = set()
    if dfs(0, initial_option, path, visited):
        print_board(BOARD, path)
        break
