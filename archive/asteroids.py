import sys
import os
from typing import Any, Tuple, List
from collections import defaultdict

HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Print a dictionary board made of points and chars
def print_board(board, w, h) -> None:
    num_rows = h
    num_cols = w

    for r in range(num_rows):
        for c in range(num_cols):
            p = r, c
            if p in board:
                print(board[p], end="")
            else:
                print(".", end="")
        print()


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Tuple[List[str], List[str]]:
    if HOME_PC:
        pic1 = [
            ".................O..",
            ".....N...........U..",
            ".............L.R....",
            "....................",
            "..........Z..V.H....",
            "................X...",
            ".............P......",
            ".............A......",
            ".Q.............T....",
            "..................F.",
            "....................",
            "......K............W",
            "...............Y....",
            "..............S.....",
            "...........JE......D",
            "...M................",
            "......B..G...C....I.",
            "....................",
            "....................",
            "....................",
        ]
        pic2 = [
            "G...................",
            "...............W....",
            "...................C",
            "...E................",
            "..............K.....",
            "...........T........",
            "............A.......",
            ".....P...FLI......N.",
            "....................",
            "........D...........",
            "......S..Y.........M",
            ".........B....Z.....",
            "....................",
            "....V.............J.",
            ".........O..........",
            "..X...........U.....",
            "....................",
            "....................",
            "..Q................R",
            ".......H............",
        ]
        w = 20
        h = 20
        t1 = 25
        t2 = 75
        t3 = 100
    else:
        w, h, t1, t2, t3 = [int(i) for i in input().split()]
        pic1, pic2 = [], []
        for i in range(h):
            first_picture_row, second_picture_row = input().split()
            pic1.append(first_picture_row)
            pic2.append(second_picture_row)

    if print_input:
        myPrint(f"{pic1=}")
        myPrint(f"{pic2=}")
        myPrint(f"{w=}")
        myPrint(f"{h=}")
        myPrint(f"{t1=}")
        myPrint(f"{t2=}")
        myPrint(f"{t3=}")

    return pic1, pic2, w, h, t1, t2, t3


# Add the points of the picture to the dictionary with the labels
def add_to_dict(pic: List[str], board: dict, label: str) -> dict:
    for r, row in enumerate(pic):
        for c, ch in enumerate(row):
            if ch != ".":
                board[ch][label] = (r, c)
    return


def build_solution_board(board: dict):
    sol_board = defaultdict(list)
    for label, info in board.items():
        pos = info["t3"]
        sol_board[pos].append(label)

    # Simpify solution board, only keep "smallest" letter
    for k, v in sol_board.items():
        sol_board[k] = min(v)

    return sol_board


# ********************************************************

board = defaultdict(dict)
pic1, pic2, w, h, t1, t2, t3 = get_start_parameters(print_input=False)
add_to_dict(pic1, board, "t1")
add_to_dict(pic2, board, "t2")


for label, info in board.items():
    t1_pos = info["t1"]
    t2_pos = info["t2"]
    delta_pos = (t2_pos[0] - t1_pos[0], t2_pos[1] - t1_pos[1])
    delta_t = t2 - t1
    advance_t = t3 - t2
    speed = (delta_pos[0] / delta_t, delta_pos[1] / delta_t)
    new_pos = (advance_t * speed[0] + t2_pos[0], advance_t * speed[1] + t2_pos[1])
    new_pos = (int(new_pos[0] // 1), int(new_pos[1] // 1))
    board[label]["t3"] = new_pos


sol_board = build_solution_board(board)

print_board(sol_board, w, h)
