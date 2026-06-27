from typing import Any, Tuple, List
import os
from cgutils import Board
from cgutils import Point2D


class InputReader:
    def __init__(self, case_nr=None):
        if case_nr is None:
            self.from_web = True
        else:
            self.from_web = False
            self.read_case_from_file(case_nr)

    def read_case_from_file(self, case_nr: int) -> None:
        current_file = os.path.basename(__file__)[:-3]  # Remove .py extension
        testcases_filename = current_file + "-testcases.txt"  # Keep hyphens for actual filename

        with open(testcases_filename, "r") as f:
            # Find the specific string (e.g., "=== Input 3 ===")
            search_string = f"=== Input {case_nr} ===\n"
            for line in f:
                if search_string in line:
                    break

            # Now read lines one after another
            lines = []
            for next_line in f:
                if next_line.startswith("==="):  # Stop at next case
                    break
                lines.append(next_line.rstrip())
            self.lines = lines[:-1]

    def input(self) -> str:
        if self.from_web == True:
            return input()
        else:
            return self.lines.pop(0)

    def get_start_parameters(self):
        w, h = [int(i) for i in self.input().split()]
        x, y = [int(i) for i in self.input().split()]
        start_point = Point2D(y, x)
        game_board = Board()
        game_board.load_data([self.input() for _ in range(h)])
        return start_point, game_board


def get_next_point(point, char):
    delta = {
        "^": Point2D(-1, 0),
        "v": Point2D(1, 0),
        "<": Point2D(0, -1),
        ">": Point2D(0, 1),
    }
    return point + delta[char]


def get_rotate_char(char):
    rotation = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^",
    }
    return rotation[char]


# ********************************************************

reader = InputReader(4)
start_point, board = reader.get_start_parameters()

counter = 0
point = start_point
while True:
    char = board[point]
    char = get_rotate_char(char)
    next_point = get_next_point(point, char)
    counter += 1
    if next_point not in board or next_point == start_point:
        break
    board[point] = char
    point = next_point

print(counter)
