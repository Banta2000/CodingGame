import os
from typing import Any, Tuple, List, Dict
from cgutils.coding_game_helper import CodingGameHelper


Point = Tuple[int, int]
Board = Dict[Point, Any]


def read_input(CGH: CodingGameHelper) -> Tuple[int, Dict[Point, Any]]:
    w, h, num_rounds = [int(i) for i in CGH.input().split()]
    lines = [CGH.input() for _ in range(h)]

    board: Board = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            board[(r, c)] = char

    return num_rounds, board


# Define winning conditions in a dictionary
WINNING_CONDITIONS = {
    "R": ["C", "L"],
    "P": ["R", "S"],
    "C": ["P", "L"],
    "L": ["P", "S"],
    "S": ["R", "C"],
}


# Rock crushes Lizard
# Rock crushes Scissors

# Paper covers Rock
# Paper disproves Spock

# Scissors cuts Paper
# Scissors decapitates Lizard

# Lizard poisons Spock
# Lizard eats Paper

# Spock smashes Scissors
# Spock vaporizes Rock


def get_winner(p1_sign: str, p2_sign: str) -> str:
    if p1_sign == p2_sign:
        return p1_sign
    elif p2_sign in WINNING_CONDITIONS[p1_sign]:
        return p1_sign
    else:
        return p2_sign


def print_board(board: Board) -> list[str]:
    num_row = max(point[0] for point in board.keys()) + 1
    num_col = max(point[1] for point in board.keys()) + 1
    lines = []
    for r in range(num_row):
        line = ""
        for c in range(num_col):
            line += board[(r, c)]
        lines.append(line)
    return lines


def one_round(board: Board) -> Board:
    new_board = {point: [] for point in board.keys()}

    num_rows = max(point[0] for point in board.keys()) + 1
    num_cols = max(point[1] for point in board.keys()) + 1

    for r in range(num_rows):
        for c in range(num_cols):
            curr_p = (r, c)
            for next_p in [(r + 1, c), (r, c + 1)]:
                if next_p in board:
                    winner = get_winner(board[curr_p], board[next_p])
                    new_board[next_p].append(winner)
                    new_board[curr_p].append(winner)

    for k, v in new_board.items():
        if len(v) == 0:
            print("Error")
        elif len(v) == 1:
            new_board[k] = v[0]
        else:
            v = list(set(v))
            if len(v) == 1:
                new_board[k] = v[0]
            elif len(v) == 2:
                winner = get_winner(v[0], v[1])
                new_board[k] = winner
            else:
                if board[k] in v:
                    v = list(set(v)-set([board[k]]))
                    winner = get_winner(v[0], v[1])
                    new_board[k] = winner
    return new_board


# ********************************************************

for case in range(1, 11):

    CGH = CodingGameHelper(case, __file__)
    num_rounds, board = read_input(CGH)

    for _ in range(num_rounds):
        board = one_round(board)

    lines = print_board(board)
    for line in lines:
        CGH.add_output_line(line)

    CGH.assert_output()
