import os
from typing import Any, Tuple, List
from collections import deque


Point = Tuple[int, int]
Board = dict[Point, Any]


class InputReader:
    def __init__(self, case_nr=None):
        if case_nr is None:
            self.from_web = True
            self.lines = None
            self.line_index = 0
        else:
            self.from_web = False
            self.lines = self._read_case_from_file(case_nr)
            self.line_index = 0

    def _read_case_from_file(self, case_nr: int) -> list[str]:
        """Read a specific test case from file and return all lines."""
        current_file = os.path.basename(__file__)[:-3]
        testcases_filename = current_file + "-testcases.txt"

        with open(testcases_filename, "r") as f:
            # Find the specific test case
            search_string = f"=== Input {case_nr} ===\n"
            for line in f:
                if search_string in line:
                    break
            else:
                raise ValueError(f"Test case {case_nr} not found")

            # Read lines until next case or end of file
            lines = []
            for next_line in f:
                if next_line.startswith("==="):  # Stop at next case
                    break
                lines.append(next_line.rstrip())

            # Remove empty line at the end if it exists
            if lines and not lines[-1]:
                lines.pop()

            return lines

    def input(self) -> str:
        """Read one line at a time, mimicking input()."""
        if self.from_web:
            return input()
        else:
            if not self.lines or self.line_index >= len(self.lines):
                raise IndexError("No more lines to read")
            line = self.lines[self.line_index]
            self.line_index += 1
            return line

    def get_start_parameters(self):
        w, h = [int(i) for i in self.input().split()]
        lines = [self.input() for _ in range(h)]
        board = {}
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                board[(r, c)] = ch
                if ch == "S":
                    start_pos = (r, c)
                if ch == "E":
                    end_pos = (r, c)
        return w, h, board, start_pos, end_pos


def print_board():
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            p = (r, c)
            print(board[p], end="")
        print("")


def get_neighbours(p: Point) -> List[Point]:
    r, c = p
    neighbours = []
    # left and right
    neighbours.append((r, (c - 1) % NUM_COLS))
    neighbours.append((r, (c + 1) % NUM_COLS))
    if r % 2 == 0:
        # even row
        neighbours.append(((r - 1) % NUM_ROWS, (c - 1) % NUM_COLS))
        neighbours.append(((r - 1) % NUM_ROWS, c))
        neighbours.append(((r + 1) % NUM_ROWS, (c - 1) % NUM_COLS))
        neighbours.append(((r + 1) % NUM_ROWS, c))

    else:
        # odd row
        neighbours.append(((r - 1) % NUM_ROWS, c))
        neighbours.append(((r - 1) % NUM_ROWS, (c + 1) % NUM_COLS))
        neighbours.append(((r + 1) % NUM_ROWS, c))
        neighbours.append(((r + 1) % NUM_ROWS, (c + 1) % NUM_COLS))
    return neighbours


def bfs(start_point: Point):
    stack = deque([])
    stack.append(start_point)
    visited = {start_point: None}
    while stack:
        curr = stack.popleft()
        if board[curr] == "E":
            return visited
        neighbours = get_neighbours(curr)
        for n in neighbours:
            if n not in visited and board[n] != "#":
                visited[n] = curr
                stack.append(n)


def reconstruct_path(visited, end_pos: Point):
    p = end_pos
    while visited[p] != None:
        p = visited[p]
        board[p] = "."
    board[p] = "S"


# ********************************************************

reader = InputReader(3)
NUM_COLS, NUM_ROWS, board, start_pos, end_pos = reader.get_start_parameters()
visited = bfs(start_pos)
reconstruct_path(visited, end_pos)
print_board()
