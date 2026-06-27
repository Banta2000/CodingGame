import os
from typing import Any, Tuple, List


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
        r, c = [int(i) for i in reader.input().split()]
        res = []
        for i in range(r):
            line = reader.input()
            res.append(line)
        return res


Point = Tuple[int, int]
Board = dict[Point, Any]


def collect_connect_points(p: Point):
    num_rows = len(data)
    num_cols = len(data[0]) if num_rows > 0 else 0
    # a == anchhor
    a_r, a_c = p

    connected_points = []

    # Check horziontal right
    for c in range(a_c + 1, num_cols):
        if len(data[a_r]) <= c or data[a_r][c] == " " or data[a_r][c] == "|":
            break
        if data[a_r][c] == "+":
            connected_points.append((a_r, c))

    # Check vertical down
    for r in range(a_r + 1, num_rows):
        if len(data[r]) <= a_c or data[r][a_c] == " " or data[r][a_c] == "-":
            break
        if data[r][a_c] == "+":
            connected_points.append((r, a_c))
    return connected_points


def create_graph():
    graph = {}
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == "+":
                graph[(row, col)] = collect_connect_points((row, col))
    return graph


def is_square(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    if p2 not in graph or p4 not in graph:
        return False
    p1_to_p2 = p2 in graph[p1]
    p1_to_p3 = p3 in graph[p1]
    p2_to_p4 = p4 in graph[p2]
    p3_to_p4 = p4 in graph[p3]
    return p1_to_p2 and p1_to_p3 and p2_to_p4 and p3_to_p4


def get_corners(p1: Point, p3: Point) -> Tuple[Point, Point, Point, Point]:
    dist = p3[0] - p1[0] + 1
    dist = 2 * dist - 1
    p2 = (p1[0], p1[1] + dist - 1)
    p4 = (p3[0], p3[1] + dist - 1)
    return p1, p2, p3, p4

# Returns a list of tuples representing horizontal lines in the graph
def find_horizontal_lines(graph) -> List[Tuple[Point, Point]]:
    return [(p, q) for p, connections in graph.items() for q in connections if p[0] == q[0] and p[1] < q[1]]


def find_vertical_lines(graph) -> List[Tuple[Point, Point]]:
    return [(p, q) for p, connections in graph.items() for q in connections if p[1] == q[1] and p[0] < q[0]]


def print_board(visited):
    RESET = "\x1b[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    num_rows = len(data)
    num_cols = len(data[0]) if num_rows > 0 else 0
    for r in range(num_rows):
        for c in range(len(data[r])):
            if (r, c) in visited:
                print(RED + data[r][c] + RESET, end="")
            else:
                print(data[r][c], end="")
        print()

# ********************************************************

reader = InputReader(15)
data = reader.get_start_parameters()
graph = create_graph()

vertical_lines = find_vertical_lines(graph)
squares = [get_corners(p1, p2) for p1, p2 in vertical_lines]
squares = [s for s in squares if is_square(*s)]
print(len(squares))

print_board(squares[0])
