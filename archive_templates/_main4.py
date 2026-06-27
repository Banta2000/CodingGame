import os
from typing import Any, Tuple, List
from cgutils import Board, Point2D


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

        return


Point = Tuple[int, int]
Board = dict[Point, Any]


# ********************************************************

reader = InputReader(1)
data = reader.get_start_parameters()
