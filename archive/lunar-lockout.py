import sys
import os
from typing import Any, Tuple, List
from collections import deque

Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Print a dictionary board made of points and chars
def print_board(board: Board, visited=None) -> None:
    if visited is None:
        visited = set()
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"

    for r in range(num_rows):
        for c in range(num_cols):
            p = r, c
            if p in board:
                print(board[p], end="")
            else:
                print(".", end="")
        print()


# Get Game Start Parameters
def get_start_parameters(dataset: str) -> Board:
    def parse(data):
        res = {}
        for r, line in enumerate(data):
            for c, char in enumerate(line):
                if char != ".":
                    res[(r, c)] = char
        return res

    if HOME_PC:
        data1 = [
            ".....",
            "A.D..",
            ".C...",
            "..X..",
            "B....",
        ]

        if dataset == "data1":
            data = data1
    else:
        data = [input() for _ in range(5)]

    num_rows = len(data)
    num_cols = len(data[0])
    target = (num_rows // 2, num_cols // 2)
    data = parse(data)
    return data, target, num_rows, num_cols


def execute_move(board: Board, instruction: str, target_cell: Point):
    # Execute a move on the board based on the instruction and target cell
    # Input: ("AD", (3,0)) moves the A piece down to (3,0)
    old_pos = [pos for pos, char in board.items() if char == instruction[0]][0]
    # Delete the old position
    del board[old_pos]
    # Add the new position
    board[target_cell] = instruction[0]
    return board


def check_four_directions(board: Board, p: Point) -> List:
    # Checks the four directions from point, returns list of points where p will stop
    # Returns: [("XU", (0,1)), ("XD", (0,-1)), ("XL", (-1,0)), ("XR", (1,0))]

    def check_one_direction(board: Board, p: Point, delta: Tuple[int, int], dir_name: str):
        if p not in board:
            return

        point_name = board[p]
        curr = p
        neighbour = (curr[0] + delta[0], curr[1] + delta[1])
        if neighbour in board:
            return

        for _ in range(10):
            new_p = (curr[0] + delta[0], curr[1] + delta[1])
            if new_p in board:
                return (f"{point_name}{dir_name}", curr)
            curr = new_p

        return

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dir_names = ["U", "D", "L", "R"]
    res = [
        result
        for result in (
            check_one_direction(board, p, dir_delta, dir_name) for dir_delta, dir_name in zip(directions, dir_names)
        )
        if result is not None
    ]
    return res


def dfs(board, target, path=None):
    if path is None:
        path = []

    pos_x = [x for x in board if board[x] == "X"][0]
    if pos_x == target:
        return path, board

    options = []
    for pos, pos_name in board.items():
        options += check_four_directions(board, pos)
    options.sort()

    print_board(board)
    print("Path: ", path)
    # print("Moves:", options)

    for instruction, target_cell in options:
        print("Trying", instruction, "to", target_cell)
        new_board = execute_move(board.copy(), instruction, target_cell)
        res = dfs(new_board, target, path + [instruction])
        if res is not None:
            return res
    return None


def bfs(board, target):
    queue = deque([(board, [])])
    visited = set()
    while queue:
        current_board, path = queue.popleft()
        pos_x = [x for x in current_board if current_board[x] == "X"][0]
        if pos_x == target:
            return path, current_board
        options = []
        for pos, pos_name in current_board.items():
            options += check_four_directions(current_board, pos)
        options.sort()

        for instruction, target_cell in options:
            new_board = execute_move(current_board.copy(), instruction, target_cell)
            hashed_board = tuple(sorted(new_board.items()))
            if hashed_board in visited:
                continue
            visited.add(hashed_board)
            queue.append((new_board, path + [instruction]))
    return None, None


# ********************************************************

board, target, num_rows, num_cols = get_start_parameters("data1")
# path, board = dfs(board, target)
path, board = bfs(board, target)
path = " ".join(path)
print(path)
print("")
print_board(board)
