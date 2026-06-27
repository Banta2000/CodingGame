import sys
import os
from typing import Any, Tuple, Dict, List
from cgutils.coding_game_helper import CodingGameHelper


COUNTER: int = 0

# Constants
EMPTY_TILE = False
FILLED_TILE = "#"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Break up the board into quarters
def break_up_in_quarters(
    q1_p1: Tuple[int, int], q4_p2: Tuple[int, int]
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], ...]:
    q1_y1, q1_x1 = q1_p1
    q4_y2, q4_x2 = q4_p2
    size = (q4_x2 - q1_x1 + 1) // 2

    q1_p2 = (q1_y1 + size - 1, q1_x1 + size - 1)
    q2_p1 = (q1_y1, q1_x1 + size)
    q2_p2 = (q1_y1 + size - 1, q4_x2)
    q3_p1 = (q1_y1 + size, q1_x1)
    q3_p2 = (q4_y2, q1_x1 + size - 1)
    q4_p1 = (q1_y1 + size, q1_x1 + size)

    return (q1_p1, q1_p2), (q2_p1, q2_p2), (q3_p1, q3_p2), (q4_p1, q4_p2)


# Generate points in a quadrant
def generate_points_in_quadrant(p1: Tuple[int, int], p2: Tuple[int, int]) -> List[Tuple[int, int]]:
    r1, c1 = p1
    r2, c2 = p2
    return [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]


# Return the four center points of the quadrants
def return_midpoints(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[Tuple[int, int], ...]:
    r1, c1 = p1
    r2, _ = p2
    size = (r2 - r1 + 1) // 2
    return (
        (r1 + size - 1, c1 + size - 1),
        (r1 + size - 1, c1 + size),
        (r1 + size, c1 + size - 1),
        (r1 + size, c1 + size),
    )


# Get the quadrant with the point
def get_quadrant_with_point(p1: Tuple[int, int], p2: Tuple[int, int], board: Dict[Tuple[int, int], Any]) -> int:
    Q1, Q2, Q3, Q4 = break_up_in_quarters(p1, p2)

    for i, Q in enumerate([Q1, Q2, Q3, Q4]):
        points = generate_points_in_quadrant(Q[0], Q[1])
        if any(board[p] for p in points):
            return i + 1
    return -1


# Depth-first search to fill the board
def dfs(p1: Tuple[int, int], p2: Tuple[int, int], board: Dict[Tuple[int, int], Any]) -> None:
    global COUNTER

    # Base case: 2x2 square
    if p1[0] + 1 == p2[0] and p1[1] + 1 == p2[1]:
        cells = [p1, (p1[0], p1[1] + 1), (p1[0] + 1, p1[1]), p2]
        COUNTER += 1
        for cell in cells:
            if not board[cell]:
                board[cell] = COUNTER
        return

    quadrant_with_point = get_quadrant_with_point(p1, p2, board)
    midpoints = return_midpoints(p1, p2)  # Q1, Q2, Q3, Q4 center midpoints

    COUNTER += 1
    if quadrant_with_point == 1:
        board[midpoints[1]] = board[midpoints[2]] = board[midpoints[3]] = COUNTER
    elif quadrant_with_point == 2:
        board[midpoints[0]] = board[midpoints[2]] = board[midpoints[3]] = COUNTER
    elif quadrant_with_point == 3:
        board[midpoints[0]] = board[midpoints[1]] = board[midpoints[3]] = COUNTER
    elif quadrant_with_point == 4:
        board[midpoints[0]] = board[midpoints[1]] = board[midpoints[2]] = COUNTER

    quarter_1, quarter_2, quarter_3, quarter_4 = break_up_in_quarters(p1, p2)
    dfs(quarter_1[0], quarter_1[1], board)
    dfs(quarter_2[0], quarter_2[1], board)
    dfs(quarter_3[0], quarter_3[1], board)
    dfs(quarter_4[0], quarter_4[1], board)


# Print the board
def print_board(board: Dict[Tuple[int, int], Any]) -> None:
    max_row = max(board, key=lambda x: x[0])[0]
    max_col = max(board, key=lambda x: x[1])[1]

    for row in range(max_row + 1):
        for col in range(max_col + 1):
            print(board[(row, col)], end="")
        print()


# Print the board with double columns
def print_board_double(board: Dict[Tuple[int, int], Any]) -> List[str]:
    max_row = max(board, key=lambda x: x[0])[0]
    max_col = max(board, key=lambda x: x[1])[1]

    lines = []
    for row in range(max_row + 1):
        line = ""
        for col in range(max_col + 1):
            line += str(board[(row, col)])
            if col % 2 == 1:
                line += str(board[(row, col)])
        lines.append(line)
    return lines


# Print the complex board
def print_board_complex(board: Dict[Tuple[int, int], Any]) -> List[str]:
    num_tiles = max(board, key=lambda x: x[0])[0] + 1
    num_pixel = num_tiles * 2 + 1

    b2 = {(row, col): " " for row in range(num_pixel) for col in range(num_pixel)}

    # Generate horizontal and vertical walls
    for row in range(0, num_pixel, 2):
        for col in range(num_pixel):
            b2[(row, col)] = "-"
    for col in range(0, num_pixel, 2):
        for row in range(num_pixel):
            b2[(row, col)] = "|"

    # Generate corners
    for row in range(0, num_pixel, 2):
        for col in range(0, num_pixel, 2):
            b2[(row, col)] = "+"

    # Remove unnecessary walls
    for r_tile in range(num_tiles):
        for c_tile in range(num_tiles):
            r_pixel, c_pixel = r_tile * 2 + 1, c_tile * 2 + 1
            center_tile = (r_tile, c_tile)
            up_tile, down_tile = (r_tile - 1, c_tile), (r_tile + 1, c_tile)
            left_tile, right_tile = (r_tile, c_tile - 1), (r_tile, c_tile + 1)
            if left_tile in board and board[left_tile] == board[center_tile]:
                b2[(r_pixel, c_pixel - 1)] = " "
            if up_tile in board and board[up_tile] == board[center_tile]:
                b2[(r_pixel - 1, c_pixel)] = " "
            if down_tile in board and board[down_tile] == board[center_tile]:
                b2[(r_pixel + 1, c_pixel)] = " "
            if right_tile in board and board[right_tile] == board[center_tile]:
                b2[(r_pixel, c_pixel + 1)] = " "
            if board[center_tile] == FILLED_TILE:
                b2[(r_pixel, c_pixel)] = FILLED_TILE

    return print_board_double(b2)


# Get Game Start Parameters
def read_input(CGH: CodingGameHelper):
    n = int(CGH.input())
    x, y = [int(i) for i in CGH.input().split()]

    board = {(i, j): EMPTY_TILE for i in range(2**n) for j in range(2**n)}
    board[(y, x)] = FILLED_TILE

    return board


# ********************************************************

CGH = CodingGameHelper(4, __file__)
board = read_input(CGH)
max_row = max(board, key=lambda x: x[0])[0]
max_col = max(board, key=lambda x: x[1])[1]

p1, p2 = (0, 0), (max_row, max_col)
dfs(p1, p2, board)
res = print_board_complex(board)

for line in res:
    CGH.add_output_line(line)
CGH.assert_output()
