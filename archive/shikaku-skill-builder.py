import sys
import os
from typing import Any, Tuple, List

Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = "True"


def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


def print_board(board: Board, visited=None) -> None:
    # Print a dictionary board made of points and chars
    if visited is None:
        visited = set()
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"

    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            p = r, c
            if p in board:
                print(RED + str(board[p]) + RESETCOL, end="")
            else:
                print(".", end="")
        print()
    print()


def create_rectangle_options(num: int):
    # Build a list of all possible rectangles for a given number
    # Each rectangle is represented as a tuple (height, width)
    # For example, for num = 6, the options would be [(1, 6), (2, 3), (3, 2), (6, 1)]
    options = []
    for i in range(1, num + 1):
        for j in range(1, num + 1):
            if i * j == num:
                options.append((i, j))
    return options


def find_numbers_in_rectangle(start: Point, rectangle: Tuple[int, int]) -> List[int]:
    # Find all numbers in a rectangle starting from a given point
    # The rectangle is defined by its height and width
    height, width = rectangle
    included_numbers = []
    for i in range(height):
        for j in range(width):
            p = start[0] + i, start[1] + j
            if p in BOARD:
                included_numbers.append(BOARD[p])
    return included_numbers


def get_start_parameters() -> Board:
    # Get Game Start Parameters
    if HOME_PC:
        w, h = 5, 5
        data = ["6 0 0 0 0", "0 2 0 4 0", "0 0 9 0 0", "0 0 0 0 0", "0 0 0 0 0"]
    else:
        True

    board = {}
    data = [[int(x) for x in line.split()] for line in data]
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char != 0:
                board[(row, col)] = char

    num_rows = max(k[0] for k in board) + 1
    num_cols = max(k[1] for k in board) + 1

    return board, num_rows, num_cols


# ********************************************************

BOARD, NUM_ROWS, NUM_COLS = get_start_parameters()
print_board(BOARD)

solutions = {pos: [] for pos in BOARD.keys()}

for pos_of_number, number in BOARD.items():
    rectangles = create_rectangle_options(number)
    for rectangle in rectangles:
        RECT_H, RECT_W = rectangle
        ROW_START = pos_of_number[0] - RECT_H + 1
        ROW_START = min(ROW_START, 0)
        ROW_END = pos_of_number[0] + 1
        COL_START = pos_of_number[1] - RECT_W + 1
        COL_START = min(COL_START, 0)
        COL_END = pos_of_number[1] + 1
        start_positions = [(i, j) for i in range(ROW_START, ROW_END) for j in range(COL_START, COL_END)]
        for start_position in start_positions:
            START_R, START_C = start_position
            if START_R < 0 or START_C < 0:
                continue
            if START_R + RECT_H > NUM_ROWS or START_C + RECT_W > NUM_COLS:
                continue
            included_numbers = find_numbers_in_rectangle(start_position, rectangle)
            if len(included_numbers) == 1 and included_numbers[0] == RECT_W * RECT_H:
                # Found a valid rectangle
                print(start_position, rectangle, included_numbers)
                s = f"{start_position[0]} {start_position[1]} {rectangle[1]} {rectangle[0]}"
                solutions[pos_of_number].append(s)

for pos in solutions:
    for k in solutions[pos]:
        print(k)


# Themen
# - Rasenmäher
# - Andere Leute nutzen den Spielplatz; Haftbarkeit; Leute die wir nicht wollen; Leute die bedrohlich rauchen
# - Es ist verboten zu parkieren
# - Die Hecken werden unterschiedlich hoch geschnitten


# Entscheidungen
# - Aenderung Gärtner
# - Anschaffung Rasenmäher
# - Tafeln "Privatgrundstück"
