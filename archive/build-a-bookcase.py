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
        height = int(self.input())
        width = int(self.input())
        number_of_shelves = int(self.input())
        return height, width, number_of_shelves


Point = Tuple[int, int]
Board = dict[Point, Any]


def print_roof(width: int) -> None:
    half_width = width // 2
    if width % 2 == 0:
        s = "/" * half_width + "\\" * half_width
    else:
        s = "/" * half_width + "^" + "\\" * half_width
    print(s)


def get_shelves(height: int, number_of_shelves: int) -> List:
    height = height - 1
    average_shelf_height = height // number_of_shelves
    number_of_bigger_shelves = height % number_of_shelves
    number_of_normal_shelves = number_of_shelves - number_of_bigger_shelves
    shelves = [average_shelf_height for _ in range(number_of_normal_shelves)]
    shelves += [average_shelf_height + 1 for _ in range(number_of_bigger_shelves)]
    return shelves


def print_one_shelf(height: int, widht: int) -> None:
    for _ in range(height - 1):
        print("|" + " " * (widht - 2) + "|")
    print("|" + "_" * (widht - 2) + "|")


# ********************************************************

reader = InputReader(1)
height, width, number_of_shelves = reader.get_start_parameters()
print_roof(width)
shelves = get_shelves(height, number_of_shelves)
for shelf_height in shelves:
    print_one_shelf(shelf_height, width)
