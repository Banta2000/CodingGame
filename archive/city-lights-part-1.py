from typing import Any, Tuple, List
from cgutils import Board, Point2D


SAMPLES: dict[str, list[str]] = {
    "data6": [
        "..4....5......",
        ".....5........",
        "..............",
        "......78......",
        "..............",
        "..............",
        "..............",
        ".......B......",
        "..............",
        ".....6........",
        "..............",
        ".............5",
    ]
}

CHAR_TO_NUM = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 18,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "O": 24,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "U": 30,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
}


NEXT_CHAR = {
    ".": "0",
    "0": "1",
    "1": "2",
    "2": "3",
    "3": "4",
    "4": "5",
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
    "9": "A",
    "A": "B",
    "B": "C",
    "C": "D",
    "D": "E",
    "E": "F",
    "F": "G",
    "G": "H",
    "H": "I",
    "I": "J",
    "J": "K",
    "K": "L",
    "L": "M",
    "M": "N",
    "N": "O",
    "O": "P",
    "P": "Q",
    "Q": "R",
    "R": "S",
    "S": "T",
    "T": "U",
    "U": "V",
    "V": "W",
    "W": "X",
    "X": "Y",
    "Y": "Z",
    "Z": "Z",
}


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        # Placeholder for parsing logic
        return data

    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
    else:
        h = int(input())
        w = int(input())
        data = [input() for _ in range(h)]

    board = Board()
    board.load_data(data)
    return board


def get_light_sources(board: Board) -> dict[Point2D, Any]:
    light_sources = {}
    for point, value in board.items():
        if value != ".":
            light_sources[point] = value
    return light_sources


def shine_light(board: Board, center, value):
    value = CHAR_TO_NUM[value]
    for p in board.keys():
        dist = round(center.euclidean_distance(p))
        if 0 <= dist <= value:
            strenght = value - dist
            original_value = board[p]
            for _ in range(strenght):
                original_value = NEXT_CHAR[original_value]
            board[p] = original_value


# ********************************************************

board = get_start_parameters("data6")
light_sources = get_light_sources(board)

blank_board = Board()
blank_board.load_data(["0" * board.num_cols for _ in range(board.num_rows)])

for point, value in light_sources.items():
    shine_light(blank_board, point, value)


blank_board.print()
