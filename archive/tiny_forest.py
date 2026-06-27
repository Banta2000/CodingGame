import sys
import os
from typing import Any, Tuple


Board = dict[(int, int), Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_initial_GS() -> Board:
    if HOME_PC:
        board = [
            "....................",
            "..Y......Y.....Y....",
            "....................",
            "..Y.............Y...",
            "........Y...........",
            "....................",
            "......Y......Y......",
            ".Y..................",
            "....................",
            "...........Y...Y....",
            "....................",
            "..Y................Y",
            "..........Y.........",
            "..Y............Y....",
            "........Y..........Y",
            "....................",
            "..............Y.....",
            ".Y..................",
            ".........Y..........",
            "....Y...............",
        ]

        board = [".....", ".....", ".....", ".....", "....Y"]

        board = [".....", ".....", ".....", ".....", "....."]
    else:
        _ = int(input())
        h = int(input())
        board = [input() for _ in range(h)]

    res = {}
    for row, line in enumerate(board):
        for col, char in enumerate(line):
            res[(row, col)] = char
    return res


def print_board(B: Board) -> None:
    num_rows = max([row for (row, col) in B]) + 1
    num_cols = max([col for (row, col) in B]) + 1
    for row in range(num_rows):
        for col in range(num_cols):
            p = (row, col)
            print(B[p], end="")
        print()
    print()


def grow_trees(B: Board) -> None:
    for p in B:
        if isinstance(B[p], int):
            B[p] += 1
            if B[p] == 10:
                B[p] = "A"
        elif B[p] == "A":
            B[p] = "Y"


def grow_new_seeds(B: Board) -> None:
    for p in B:
        if B[p] == "Y":
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_p = (p[0] + d[0], p[1] + d[1])
                if new_p in B and B[new_p] == ".":
                    B[new_p] = 0


def simulate_forest_growth(B: Board, start) -> None:
    S = B.copy()
    S[start] = 0
    for year in range(1, 34):
        grow_trees(S)
        grow_new_seeds(S)
    return final_count(S)


def final_count(B: Board) -> int:
    return len([x for x in list(B.values()) if x == "Y" or x == "A"])


def get_possible_starting_points(B: Board) -> list[Tuple[int, int]]:
    return [p for p in B if B[p] == "."]

# ********************************************************

board = get_initial_GS()
start_points = get_possible_starting_points(board)

res_list = [simulate_forest_growth(board, start) for start in start_points]
res = max(res_list)

print(res)

# print(res)
