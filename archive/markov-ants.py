from typing import Any, Tuple, List
from collections import defaultdict

Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = True


def get_start_parameters():
    def _parse(data):
        board = set()
        start = None
        for r, line in enumerate(data):
            for c, char in enumerate(line):
                p = (r, c)
                if char not in ["+", "-", "|"]:
                    board.add(p)
                if char == "A":
                    start = p
        return board, start

    if HOME_PC:
        step = 1
        data = ["+---+", "|...|", "|.A.|", "|...|", "+---+"]
    else:
        step = int(input())
        w, h = [int(i) for i in input().split()]
        data = [input() for _ in range(h)]

    board, start = _parse(data)
    return board, start, step


def get_neighbours_one_point(p: Point, step: int):
    # For a given point, returns the four cardinal steps
    delta = [(0, step), (step, 0), (0, -step), (-step, 0)]
    n = [(p[0] + d[0], p[1] + d[1]) for d in delta]
    return n


def calculate_new_board(board, step: int):
    # Input: board consists of points (keys) each one with a probability (value)
    # For each point, calculate its neighbours with * 0.25 probability
    new_board = defaultdict(list)
    for p, prob in board.items():
        neighbours = get_neighbours_one_point(p, step)
        for n in neighbours:
            new_board[n].append(prob * 0.25)

    res = {p: sum(probs) for p, probs in new_board.items()}
    return res


def separate_outside_boarder(prob_board: Board, board):
    # Separates the points inside the board and outside the board
    # Input: the probability board (a dict of pos and probs) and the actual board
    # Output: two dictionaries, one for inside and one for outside the board
    inside_board = {}
    outside_board = {}
    for pos, prob in prob_board.items():
        if pos in board:
            inside_board[pos] = prob
        else:
            outside_board[pos] = prob
    return inside_board, outside_board


def sum_probs_outside_board(board: Board) -> float:
    # Sums the probabilities of points outside the border
    total = 0.0
    return sum(list(board.values()))


# ********************************************************

board, start, step = get_start_parameters()
prob_board = {start: 1.0}

endres = 0
time = 0
for _ in range(200):
    time += 1
    prob_board = calculate_new_board(prob_board, step)
    prob_board, outside_board = separate_outside_boarder(prob_board, board)
    temp_probability = sum_probs_outside_board(outside_board)
    endres += temp_probability * time
print(f"{endres:.1f}")
