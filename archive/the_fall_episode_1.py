import sys
import os
from typing import Any, Tuple
from enum import Enum

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


class Direction(Enum):
    TOP = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_start_parameters():
    if HOME_PC:
        (
            w,
            h,
        ) = (
            8,
            4,
        )
        board = [
            [0, 3, 0, 0, 0, 0, 0, 0],
            [0, 11, 2, 2, 2, 2, 13, 0],
            [0, 0, 0, 0, 0, 0, 3, 0],
            [0, 12, 2, 2, 2, 2, 10, 0],
        ]
        ex = 1
    else:
        w, h = [int(i) for i in input().split()]
        board = [input() for _ in range(h)]
        board = [[int(x) for x in line.split(" ")] for line in board]
        ex = int(input())
    myPrint(w, h, board, ex)
    return board


def define_tiles():
    res = {
        0: None,
        1: {Direction.TOP: Direction.DOWN, Direction.LEFT: Direction.DOWN, Direction.RIGHT: Direction.DOWN},
        2: {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT},
        3: {Direction.TOP: Direction.DOWN},
        4: {Direction.TOP: Direction.LEFT, Direction.RIGHT: Direction.DOWN},
        5: {Direction.TOP: Direction.RIGHT, Direction.LEFT: Direction.DOWN},
        6: {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT},
        7: {Direction.TOP: Direction.DOWN, Direction.RIGHT: Direction.DOWN},
        8: {Direction.LEFT: Direction.DOWN, Direction.RIGHT: Direction.DOWN},
        9: {Direction.TOP: Direction.DOWN, Direction.LEFT: Direction.DOWN},
        10: {Direction.TOP: Direction.LEFT},
        11: {Direction.TOP: Direction.RIGHT},
        12: {Direction.RIGHT: Direction.DOWN},
        13: {Direction.LEFT: Direction.DOWN},
    }
    return res


# ********************************************************

Tiles = define_tiles()
G = get_start_parameters()
DIR_CHANGES = {Direction.TOP: (0, -1), Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0), Direction.DOWN: (0, 1)}

# while True:
while True:
    inputs = input().split()
    # inputs = ["1", "0", "TOP"]
    xi = int(inputs[0])
    yi = int(inputs[1])
    pos = inputs[2]

    room_type_nr = G[yi][xi]
    room_layout = Tiles[room_type_nr]
    room_enter_dir = Direction[pos]

    exit_dir = room_layout[room_enter_dir]
    delta = DIR_CHANGES[exit_dir]
    x_out = xi + delta[0]
    y_out = yi + delta[1]
    print(x_out, y_out)
