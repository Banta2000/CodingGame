import sys
import os
from typing import Any, Tuple, Dict, Set
from collections import defaultdict

Game = Dict[str, Any]
Point = Tuple[int, int]
Board = Dict[Point, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


class Duck:
    def __init__(self, id: int, p1: Point, p2: Point):
        self.id = id
        self.pos = p2
        self.vel = (p2[0] - p1[0], p2[1] - p1[1])

    def __str__(self):
        return f"Duck({self.id}: pos: {self.pos}  vel: {self.vel})"

    # Return the number of turns before the duck is out of the picture
    def how_many_turns_before_out_of_picture(self, num_rows: int, num_cols: int) -> int:
        turns = 0
        r, c = self.pos
        dr, dc = self.vel
        while 0 <= r < num_rows and 0 <= c < num_cols:
            r += dr
            c += dc
            turns += 1
            if turns > 100:  # Avoid infinite loop
                break
        return turns

    # Move the duck
    def fly(self):
        r, c = self.pos
        dr, dc = self.vel
        self.pos = (r + dr, c + dc)


# Modified printing
def my_print(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Print a dictionary board made of points and chars
def print_board(board: Board, visited: Set[Point] = None) -> None:
    if visited is None:
        visited = set()
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"
    num_rows = max(k[0] for k in board) + 1
    num_cols = max(k[1] for k in board) + 1

    for r in range(num_rows):
        for c in range(num_cols):
            p = (r, c)
            if p in visited:
                print(RED + str(board[p]) + RESETCOL, end="")
            elif p in board:
                print(board[p], end="")
            else:
                print(" ", end="")
        print()
    print()


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        # s0 = ["......", "...1..", "......", ".2....", "......"]
        # s1 = ["......", "..1...", "...2..", "......", "......"]
        s0 = [
            "1.........................",
            "2.........................",
            "3.........................",
            "4.........................",
            "5.........................",
            "6.........................",
        ]
        s1 = [
            ".......1..................",
            "......2...................",
            "3.........................",
            ".........4................",
            ".....5....................",
            "....6.....................",
        ]
    else:
        w = int(input())
        h = int(input())
        s0 = [input() for _ in range(h)]
        s1 = [input() for _ in range(h)]

    if print_input:
        my_print(f"{s0=}")
        my_print(f"{s1=}")

    num_rows = len(s0)
    num_cols = len(s0[0])

    return s0, s1, num_rows, num_cols


# Return a dict of ducks with their positions in a list {1: [(1, 3), (2, 2)], 2: [(3, 1), (4, 2)]}
def parse_picture_to_pos(s0, s1):
    board = defaultdict(list)
    for r, row in enumerate(s0):
        for c, cell in enumerate(row):
            if cell != ".":
                board[(int(cell))].append((r, c))
    for r, row in enumerate(s1):
        for c, cell in enumerate(row):
            if cell != ".":
                board[(int(cell))].append((r, c))
    return board


def parse_pos_to_ducks(board):
    ducks = []
    for k, v in board.items():
        temp = Duck(k, v[0], v[1])
        ducks.append(temp)
    return ducks


# ********************************************************

s0, s1, num_rows, num_cols = get_start_parameters(print_input=False)
# for line in s1: print(line)
board = parse_picture_to_pos(s0, s1)
ducks = parse_pos_to_ducks(board)
ducks = sorted(ducks, key=lambda x: x.how_many_turns_before_out_of_picture(num_rows, num_cols))
while ducks:
    for d in ducks:
        d.fly()
    while True:
        tempDuck = ducks.pop(0)
        if 0 <= tempDuck.pos[0] < num_rows and 0 <= tempDuck.pos[1] < num_cols:
            break
    print(f"{tempDuck.id} {tempDuck.pos[1]} {tempDuck.pos[0]}")
