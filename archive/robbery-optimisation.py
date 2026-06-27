import os
from typing import Any, Tuple


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
        num_lines = int(self.input())
        lines = [int(self.input()) for _ in range(num_lines)]
        return lines


def max_robbery_amount(houses: list[int]) -> int:
    """Calculate maximum money that can be robbed without robbing adjacent houses."""
    if not houses:
        return 0
    if len(houses) == 1:
        return max(houses[0], 0)
    if len(houses) == 2:
        return max(houses[0], houses[1], 0)

    # Space-optimized DP: only track last two values
    prev2 = max(houses[0], 0)  # max money up to house i-2
    prev1 = max(houses[1], prev2)  # max money up to house i-1

    for i in range(2, len(houses)):
        current_house_value = max(houses[i], 0)  # Can't rob negative amounts
        current_max = max(current_house_value + prev2, prev1)
        prev2, prev1 = prev1, current_max

    return prev1


# ********************************************************

reader = InputReader(14)
data = reader.get_start_parameters()
result = max_robbery_amount(data)
print(result)
