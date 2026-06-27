from typing import Any, Tuple, List
from cgutils import Board, Point2D

SAMPLES: dict[str, str] = {
    "data1": "fg9 ls11 oe7",
    "data2": "ee7 ou7 eu7 oe7 jm7 dm5 pm5",
    "data3": "ft17 PLANTft9 nf17 PLANTnf9 PLANTjm5",
    "data4": "jm31 PLANTMOWjm27 PLANTMOWjm23 PLANTMOWjm19 PLANTMOWjm15 PLANTMOWjm11 PLANTMOWjm7 PLANTMOWjm1",
    "data5": "je9 ju9 em7 om7 PLANTMOWjm21",
}

# Point = Tuple[int, int]
# Board = dict[Point, Any]

CHAR_TO_NUM = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
}


def get_start_parameters(start_data: str | None = None):
    def parse(s: str) -> list[tuple[str, Point2D, float]]:
        parts = s.strip().split(" ")
        res = []
        for part in parts:
            if part.startswith("PLANTMOW"):
                ins = "PLANTMOW"
                part = part[len("PLANTMOW") :]
            elif part.startswith("PLANT"):
                ins = "PLANT"
                part = part[len("PLANT") :]
            else:
                ins = "NORMAL"
            col = CHAR_TO_NUM[part[0]]
            row = CHAR_TO_NUM[part[1]]
            size = int(part[2:]) / 2
            res.append((ins, Point2D(row, col), size))
        return res

    if start_data and start_data in SAMPLES:
        instructions = SAMPLES[start_data]
    else:
        instructions = input()

    return parse(instructions)


def in_circle(p, center, radius):
    return (p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2 <= radius**2


def execute_circle(board: Board, center: Point2D, radius: float, ins):
    for point in board.keys():
        if in_circle(point, center, radius):
            if ins == "NORMAL":
                board[point] = "#"
            elif ins == "PLANT":
                board[point] = "."
            elif ins == "PLANTMOW":
                if board[point] == "#":
                    board[point] = "."
                else:
                    board[point] = "#"


def print_board(board: Board):
    max_row = max(p[0] for p in board.keys())
    max_col = max(p[1] for p in board.keys())

    for r in range(max_row + 1):
        for c in range(max_col + 1):
            p = (r, c)
            if board[p] == ".":
                print("{}", end="")
            else:
                print("  ", end="")
        print()


# ********************************************************

instructions = get_start_parameters("data5")
test = ["." * 19 for _ in range(25)]
board = Board()
board.load_data(test)

for ins, center, size in instructions:
    execute_circle(board, center, size, ins)

print_board(board)
# board.print()
