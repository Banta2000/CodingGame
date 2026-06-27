import sys
import os
from typing import Any, Tuple, List
from collections import namedtuple

Point = tuple[int, int]
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
    num_rows = max(k[0] for k in board.keys()) + 1
    num_cols = max(k[1] for k in board.keys()) + 1

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


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Board:
    if HOME_PC:
        board = {
            (0, 0): 0,
            (0, 1): 0,
            (0, 2): 0,
            (0, 3): 0,
            (0, 4): 0,
            (0, 5): 0,
            (0, 6): 0,
            (0, 7): 0,
            (0, 8): 0,
            (0, 9): 9,
            (0, 10): 0,
            (0, 11): 0,
            (0, 12): 0,
            (0, 13): 0,
            (0, 14): 0,
            (1, 0): 0,
            (1, 1): 8,
            (1, 2): 0,
            (1, 3): 0,
            (1, 4): 0,
            (1, 5): 6,
            (1, 6): 0,
            (1, 7): 0,
            (1, 8): 6,
            (1, 9): 0,
            (1, 10): 0,
            (1, 11): 0,
            (1, 12): 0,
            (1, 13): 0,
            (1, 14): 0,
            (2, 0): 0,
            (2, 1): 0,
            (2, 2): 0,
            (2, 3): 0,
            (2, 4): 0,
            (2, 5): 0,
            (2, 6): 0,
            (2, 7): 0,
            (2, 8): 0,
            (2, 9): 0,
            (2, 10): 0,
            (2, 11): 0,
            (2, 12): 0,
            (2, 13): 0,
            (2, 14): 0,
            (3, 0): 0,
            (3, 1): 0,
            (3, 2): 0,
            (3, 3): 10,
            (3, 4): 0,
            (3, 5): 0,
            (3, 6): 0,
            (3, 7): 0,
            (3, 8): 6,
            (3, 9): 0,
            (3, 10): 6,
            (3, 11): 0,
            (3, 12): 0,
            (3, 13): 0,
            (3, 14): 0,
            (4, 0): 0,
            (4, 1): 10,
            (4, 2): 0,
            (4, 3): 0,
            (4, 4): 0,
            (4, 5): 0,
            (4, 6): 0,
            (4, 7): 0,
            (4, 8): 0,
            (4, 9): 0,
            (4, 10): 0,
            (4, 11): 0,
            (4, 12): 15,
            (4, 13): 0,
            (4, 14): 0,
            (5, 0): 0,
            (5, 1): 0,
            (5, 2): 0,
            (5, 3): 14,
            (5, 4): 0,
            (5, 5): 0,
            (5, 6): 9,
            (5, 7): 0,
            (5, 8): 0,
            (5, 9): 0,
            (5, 10): 6,
            (5, 11): 0,
            (5, 12): 0,
            (5, 13): 0,
            (5, 14): 0,
            (6, 0): 0,
            (6, 1): 0,
            (6, 2): 0,
            (6, 3): 0,
            (6, 4): 0,
            (6, 5): 12,
            (6, 6): 0,
            (6, 7): 0,
            (6, 8): 0,
            (6, 9): 0,
            (6, 10): 0,
            (6, 11): 0,
            (6, 12): 0,
            (6, 13): 0,
            (6, 14): 0,
            (7, 0): 0,
            (7, 1): 0,
            (7, 2): 0,
            (7, 3): 0,
            (7, 4): 0,
            (7, 5): 0,
            (7, 6): 0,
            (7, 7): 0,
            (7, 8): 6,
            (7, 9): 0,
            (7, 10): 0,
            (7, 11): 0,
            (7, 12): 12,
            (7, 13): 0,
            (7, 14): 0,
            (8, 0): 0,
            (8, 1): 0,
            (8, 2): 0,
            (8, 3): 0,
            (8, 4): 0,
            (8, 5): 0,
            (8, 6): 0,
            (8, 7): 0,
            (8, 8): 0,
            (8, 9): 0,
            (8, 10): 0,
            (8, 11): 0,
            (8, 12): 8,
            (8, 13): 0,
            (8, 14): 0,
            (9, 0): 0,
            (9, 1): 0,
            (9, 2): 0,
            (9, 3): 0,
            (9, 4): 0,
            (9, 5): 9,
            (9, 6): 0,
            (9, 7): 0,
            (9, 8): 0,
            (9, 9): 0,
            (9, 10): 0,
            (9, 11): 0,
            (9, 12): 0,
            (9, 13): 0,
            (9, 14): 0,
            (10, 0): 0,
            (10, 1): 0,
            (10, 2): 0,
            (10, 3): 0,
            (10, 4): 0,
            (10, 5): 0,
            (10, 6): 0,
            (10, 7): 0,
            (10, 8): 0,
            (10, 9): 0,
            (10, 10): 0,
            (10, 11): 0,
            (10, 12): 0,
            (10, 13): 0,
            (10, 14): 0,
            (11, 0): 0,
            (11, 1): 14,
            (11, 2): 0,
            (11, 3): 0,
            (11, 4): 0,
            (11, 5): 0,
            (11, 6): 0,
            (11, 7): 0,
            (11, 8): 8,
            (11, 9): 0,
            (11, 10): 0,
            (11, 11): 0,
            (11, 12): 0,
            (11, 13): 0,
            (11, 14): 24,
            (12, 0): 0,
            (12, 1): 0,
            (12, 2): 0,
            (12, 3): 0,
            (12, 4): 0,
            (12, 5): 0,
            (12, 6): 0,
            (12, 7): 0,
            (12, 8): 0,
            (12, 9): 6,
            (12, 10): 0,
            (12, 11): 0,
            (12, 12): 6,
            (12, 13): 0,
            (12, 14): 0,
            (13, 0): 0,
            (13, 1): 0,
            (13, 2): 0,
            (13, 3): 9,
            (13, 4): 0,
            (13, 5): 0,
            (13, 6): 6,
            (13, 7): 0,
            (13, 8): 0,
            (13, 9): 28,
            (13, 10): 0,
            (13, 11): 0,
            (13, 12): 0,
            (13, 13): 0,
            (13, 14): 0,
            (14, 0): 0,
            (14, 1): 0,
            (14, 2): 0,
            (14, 3): 0,
            (14, 4): 0,
            (14, 5): 0,
            (14, 6): 0,
            (14, 7): 0,
            (14, 8): 0,
            (14, 9): 0,
            (14, 10): 0,
            (14, 11): 0,
            (14, 12): 0,
            (14, 13): 0,
            (14, 14): 0,
            (15, 0): 0,
            (15, 1): 0,
            (15, 2): 0,
            (15, 3): 0,
            (15, 4): 0,
            (15, 5): 0,
            (15, 6): 0,
            (15, 7): 8,
            (15, 8): 0,
            (15, 9): 0,
            (15, 10): 0,
            (15, 11): 0,
            (15, 12): 0,
            (15, 13): 0,
            (15, 14): 0,
            (16, 0): 0,
            (16, 1): 0,
            (16, 2): 0,
            (16, 3): 10,
            (16, 4): 0,
            (16, 5): 0,
            (16, 6): 0,
            (16, 7): 0,
            (16, 8): 0,
            (16, 9): 0,
            (16, 10): 0,
            (16, 11): 0,
            (16, 12): 0,
            (16, 13): 0,
            (16, 14): 0,
            (17, 0): 0,
            (17, 1): 0,
            (17, 2): 0,
            (17, 3): 0,
            (17, 4): 0,
            (17, 5): 0,
            (17, 6): 15,
            (17, 7): 0,
            (17, 8): 6,
            (17, 9): 0,
            (17, 10): 0,
            (17, 11): 0,
            (17, 12): 0,
            (17, 13): 0,
            (17, 14): 0,
            (18, 0): 0,
            (18, 1): 0,
            (18, 2): 0,
            (18, 3): 0,
            (18, 4): 0,
            (18, 5): 0,
            (18, 6): 0,
            (18, 7): 0,
            (18, 8): 0,
            (18, 9): 0,
            (18, 10): 0,
            (18, 11): 0,
            (18, 12): 0,
            (18, 13): 0,
            (18, 14): 0,
            (19, 0): 8,
            (19, 1): 0,
            (19, 2): 0,
            (19, 3): 0,
            (19, 4): 0,
            (19, 5): 0,
            (19, 6): 0,
            (19, 7): 0,
            (19, 8): 0,
            (19, 9): 0,
            (19, 10): 0,
            (19, 11): 0,
            (19, 12): 0,
            (19, 13): 0,
            (19, 14): 0,
        }

    else:
        board: Board = {}
        _, h = [int(i) for i in input().split()]
        for row in range(h):
            for col, char in enumerate(input().split()):
                char = int(char)
                p = (row, col)
                board[p] = char

    if print_input:
        myPrint(f"{board=}")

    num_rows = max(k[0] for k in board) + 1
    num_cols = max(k[1] for k in board) + 1

    return board, num_rows, num_cols


# Returns the coordinates of all the points with lenghts in the board that are lower right
def get_lower_right_points(start_point: Point) -> List[Point]:
    res = {k: v for k, v in board_num.items() if k[0] >= start_point[0] and k[1] >= start_point[1]}
    return list(res.keys())


# Explores the next possible rectangle that does not overlap with the previous ones
def dfs(visited: Board = None):
    def _is_already_visited(start_point: Point, end_point: Point, visited) -> bool:
        # Returns true if any point in the rectangle is already visited
        s_row, s_col = start_point
        e_row, e_col = end_point
        for r in range(s_row, e_row + 1):
            for c in range(s_col, e_col + 1):
                if visited[(r, c)] != 0:
                    return True

    if visited and all(v != 0 for v in visited.values()):
        # print("Solution")
        total_solutions.append(visited.copy())
        return

    if visited is None:
        visited = {k: 0 for k in board}
        next_letter = "A"
        start_point = (0, 0)
    else:
        empty_points = [k for k, v in visited.items() if v == 0]
        start_point = sorted(empty_points)[0]
        existing_letters = set(visited.values()) - {0}
        highest_letter = max(existing_letters)
        next_letter = chr(ord(highest_letter) + 1)
        if highest_letter == "Z":
            next_letter = "a"
        else:
            next_letter = chr(ord(highest_letter) + 1)

    for option in solution_board[start_point]:
        # Check for overlap
        if _is_already_visited(start_point, option, visited):
            continue
        new_visited = visited.copy()
        s_row, s_col = start_point
        e_row, e_col = option
        for r in range(s_row, e_row + 1):
            for c in range(s_col, e_col + 1):
                new_visited[(r, c)] = next_letter
        dfs(new_visited)


# Returns the included points with a value
def get_included_points(start_point: Point, end_point: Point) -> List[Point]:
    res = {
        k: v
        for k, v in num_board.items()
        if start_point[0] <= k[0] <= end_point[0] and start_point[1] <= k[1] <= end_point[1]
    }
    return list(res.keys())


# Checks if the rectangle a) contains only one num point, b) the size of the rectangle is the same as the num point
def is_valid_rectangle(start_point: Point, end_point: Point) -> bool:
    res = get_included_points(start_point, end_point)
    if len(res) != 1:
        return False
    else:
        res = res[0]
    w = end_point[0] - start_point[0] + 1
    h = end_point[1] - start_point[1] + 1
    res = num_board[res] == w * h
    return res


# From a starting point, returns all the correct rectangles that can be formed
def get_valid_rectangles(start_point: Point) -> List[Point]:
    res = []
    for row in range(start_point[0], num_rows):
        for col in range(start_point[1], num_cols):
            if is_valid_rectangle(start_point, (row, col)):
                res.append((row, col))
    return res


# Returns solution_board: {start_point: [valid_end_points]} that meet condition: only one num point, size rectangle == num point
def build_solution_board():
    res = {}
    for start_point in board:
        res[start_point] = get_valid_rectangles(start_point)
    return res


# ********************************************************

total_solutions = []
board, num_rows, num_cols = get_start_parameters(print_input=False)
num_board = {k: v for k, v in board.items() if v != 0}
solution_board = build_solution_board()

dfs()

for i, sol in enumerate(total_solutions):
    sorted_points = sorted(sol.keys())
    result_string = "".join(sol[point] for point in sorted_points)
    total_solutions[i] = result_string

print(len(total_solutions))
total_solutions.sort()
final_solution = total_solutions[0]
for i in range(0, len(final_solution), num_cols):
    print(final_solution[i : i + num_cols])
