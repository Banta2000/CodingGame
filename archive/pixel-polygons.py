import sys
import os
from typing import Any, Tuple, List

Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


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
                print(RED + board[p] + RESETCOL, end="")
            elif p in board:
                print(board[p], end="")
            else:
                print(" ", end="")
        print()
    print()


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Tuple[Board, int, int]:
    if HOME_PC:
        data = [
            "..........",
            ".#.#.#.##.",
            ".########.",
            "...####...",
            ".######.#.",
            "..###.###.",
            ".###......",
            ".########.",
            "..###..##.",
            "..........",
        ]
        # data=['....', '.##.', '.##.', '....']

    else:
        n = int(input())
        data = [input().strip() for _ in range(n)]

    if print_input:
        myPrint(f"{data=}")

    num_rows = len(data)
    num_cols = len(data[0])

    board: Board = {}
    for r in range(num_rows):
        for c in range(num_cols):
            p: Point = r, c
            board[p] = data[r][c]

    return board, num_rows, num_cols


# Returns the points in row or column with a border in the given direction
def get_fields_with_border(search_index: int, direction: str):
    def _get_neighour(p: Point, direction: str) -> Point:
        r, c = p
        mapper = {"N": (r - 1, c), "S": (r + 1, c), "W": (r, c - 1), "E": (r, c + 1)}
        return mapper[direction]

    # Will contain the indexes of the fields which have a border
    res = []

    # Create the line of point to scan
    if direction in "NS":
        row = search_index
        points = [(row, col) for col in range(num_cols)]
    else:
        col = search_index
        points = [(row, col) for row in range(num_rows)]

    for p in points:
        if board[p] == "#" and _get_neighour(p, direction) in board and board[_get_neighour(p, direction)] == ".":
            res.append(p)

    # print(f"{res=}")
    return res


# Returns the number of clusters of points that are neighbouring
def get_neighbouring_clusters(lst: List[Point]) -> int:
    def _are_neighbours(p1: Point, p2: Point) -> bool:
        r1, c1 = p1
        r2, c2 = p2
        return abs(r1 - r2) + abs(c1 - c2) == 1

    if len(lst) == 0:
        return 0

    res = []
    for i in range(len(lst) - 1):
        n1, n2 = lst[i], lst[i + 1]
        if _are_neighbours(n1, n2):
            res.append(0)
        else:
            res.append(1)
    return 1 + sum(res)


# Get the number of borders for a given row/col in a given direction
def get_borders(num: int, direction: str):
    r = get_fields_with_border(num, direction)
    res = get_neighbouring_clusters(r)
    return res


# ********************************************************

board, num_rows, num_cols = get_start_parameters(print_input=False)
# print_board(board)


total = 0
for row in range(num_rows):
    total += get_borders(row, "N")
    total += get_borders(row, "S")
    
for col in range(num_cols):
    total += get_borders(col, "E")
    total += get_borders(col, "W")

print(total)
