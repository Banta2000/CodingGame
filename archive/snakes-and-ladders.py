from typing import Any, Tuple, List
from collections import deque

Board = dict[int, int]
HOME_PC: bool = True


def next_positions(current: int, board: Board, dice_size: int) -> List[int]:
    # Rolls all possible dice values (1 to N), returns all possible next positions
    # Respects the board's snakes and ladders as provided by the board
    dice_rolls = [i for i in range(1, dice_size + 1)]
    landings = [current + roll for roll in dice_rolls]
    landings = [board[landing] for landing in landings if landing in board]
    return landings


def get_start_parameters() -> Tuple[Board, int]:
    # Get Game Start Parameters
    snakes_and_ladders = []
    dice_size: int = 0
    if HOME_PC:
        width, height, dice_size = 5, 5, 6
        snakes_and_ladders = [[6, 3], [7, 1], [21, 16], [22, 15], [5, 8], [14, 19]]
    else:
        width, height = [int(i) for i in input().split()]
        dice_size = int(input())
        snake_amount, ladder_amount = [int(i) for i in input().split()]
        for i in range(snake_amount):
            snakes_and_ladders.append([int(j) for j in input().split()])
        for i in range(ladder_amount):
            snakes_and_ladders.append(reversed([int(j) for j in input().split()]))

    board = {n: n for n in range(1, width * height + 1)}
    for start, end in snakes_and_ladders:
        board[start] = end
    return board, dice_size


def bfs(board: Board, dice_size: int):
    # Finds the shortest path to get to the last square
    stack = deque()
    stack.append((1, 0))
    visited = set()
    target = max(board.keys())
    while stack:
        curr, steps = stack.popleft()
        if curr == target:
            print(steps)
            return steps
        options = next_positions(curr, board, dice_size)
        for option in options:
            if option not in visited:
                visited.add(option)
                stack.append((option, steps + 1))


# ********************************************************

board, dice_size = get_start_parameters()
bfs(board, dice_size)
