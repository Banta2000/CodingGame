import sys
import os
from typing import Any, Tuple, List, Dict

Game = Dict[Tuple[int, int], str]
Sand = List[Tuple[str, int]]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Any, end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Tuple[Game, Sand]:
    if HOME_PC:
        w, h, sand = 3, 3, [("n", 1), ("e", 1), ("o", 1), ("A", 1)]
        w, h, sand = 4, 4, [("S", 0), ("A", 0), ("l", 0), ("N", 0), ("o", 0), ("I", 0), ("D", 0), ("v", 0)]
        w, h, sand = 2, 2, [("S", 0), ("T", 1), ("u", 1), ("J", 1)]
        w, h, sand = (
            11,
            9,
            [
                ("w", 3),
                ("w", 3),
                ("w", 7),
                ("w", 7),
                ("w", 3),
                ("w", 7),
                ("Z", 3),
                ("A", 7),
                ("w", 5),
                ("D", 7),
                ("L", 6),
                ("E", 5),
                ("b", 0),
                ("d", 10),
                ("w", 0),
                ("w", 10),
                ("H", 0),
                ("H", 10),
                ("x", 0),
                ("x", 10),
                ("x", 3),
                ("x", 7),
                ("m", 3),
                ("m", 3),
                ("m", 3),
                ("m", 7),
                ("m", 7),
                ("m", 7),
                ("q", 10),
                ("p", 0),
                ("m", 0),
                ("m", 10),
                ("m", 5),
                ("A", 4),
                ("A", 10),
                ("A", 4),
                ("A", 10),
                ("A", 3),
                ("A", 9),
                ("A", 3),
                ("A", 9),
                ("A", 2),
                ("A", 8),
                ("A", 2),
                ("A", 8),
                ("A", 2),
                ("A", 8),
                ("A", 2),
                ("A", 8),
                ("A", 2),
                ("A", 8),
                ("v", 3),
                ("v", 7),
                ("v", 3),
                ("v", 7),
                ("v", 3),
                ("v", 7),
                ("v", 3),
                ("v", 5),
                ("v", 5),
                ("A", 4),
                ("A", 6),
                ("A", 4),
                ("A", 7),
                ("A", 5),
                ("A", 5),
                ("A", 5),
                ("A", 5),
                ("A", 5),
            ],
        )
    else:
        w, h = [int(i) for i in input().split()]
        n = int(input())
        sand = []
        for i in range(n):
            inputs = input().split()
            s = inputs[0]
            p = int(inputs[1])
            sand.append((s, p))

    if print_input:
        myPrint(w, h, sand)

    board: Game = {}
    for row in range(h):
        for col in range(w):
            board[(row, col)] = "."
    return board, sand


def print_board(board: Game) -> None:
    rows = max(k[0] for k in board.keys()) + 1
    cols = max(k[1] for k in board.keys()) + 1

    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            if board[(row, col)] == ".":
                print(" ", end="")
            else:
                print(board[(row, col)], end="")
        print("|", end="")
        print()

    print("+" + "-" * cols + "+")


def drop_sand(board: Game, sand: Tuple[int, int]) -> None:
    char, start_col = sand
    if char in "abcdefghijklmnopqrstuvwxyz":
        first_right = True
    else:
        first_right = False

    curr = (-1, start_col)
    while True:
        r, c = curr
        below = (r + 1, c)
        below_left = (r + 1, c - 1)
        below_right = (r + 1, c + 1)
        first_option = below
        second_option = below_right if first_right else below_left
        third_option = below_left if first_right else below_right

        if first_option not in board:
            board[curr] = char
            break
        if board[first_option] == ".":
            curr = below
            continue

        if second_option in board and board[second_option] == ".":
            curr = second_option
            continue

        if third_option in board and board[third_option] == ".":
            curr = third_option
            continue

        board[curr] = char
        break
    return board


# ********************************************************

board, sand = get_start_parameters(print_input=True)
for sand_drop in sand:
    board = drop_sand(board, sand_drop)
print_board(board)
