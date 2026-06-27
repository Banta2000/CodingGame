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
        n = int(self.input())
        data = [[int(j) for j in self.input().split()] for _ in range(n)]
        return data


def count_digits_to_next_potenz(n: int) -> int:
    """Count digits from n to the next power of ten."""
    digits = len(str(n))
    next_potenz = 10**digits
    count = (next_potenz - n) * digits
    return count


def count_digits_between_two_potenzen(a: int, b: int) -> int:
    """Count digits between two numbers. a=55, b=48420, counts digitts from 100 to 9999"""
    a_digits = len(str(a))
    b_digits = len(str(b))
    if a_digits == b_digits or a_digits + 1 == b_digits:
        return 0
    counter = 0
    for i in range(a_digits + 1, b_digits):
        anzahl_zahlen = 10**i - 10 ** (i - 1)
        counter += anzahl_zahlen * i
    return counter


def count_digits_after_potenz(num: int) -> int:
    """Count digits from last potenz up to digit."""
    digits = len(str(num))
    if digits == 1:
        return num
    last_potenz = 10 ** (digits - 1)
    count = (num - last_potenz + 1) * digits
    return count


def count_digits_between_two_numbers_slow(a: int, b: int):
    sum_counter = {}
    counter = 0
    for i in range(a, b + 1):
        counter += len(str(i))
        sum_counter[i] = counter
    return counter


def count_digits_between_two_numbers_fast(a: int, b: int):
    if a == b:
        return len(str(a))
    a_digits = len(str(a))
    b_digits = len(str(b))

    counter = 0

    # Both numbers have the same number of digits
    if a_digits == b_digits:
        counter += (b - a + 1) * a_digits
        return counter

    counter += count_digits_to_next_potenz(a)
    counter += count_digits_between_two_potenzen(a, b)
    counter += count_digits_after_potenz(b)
    return counter


def binary_search(fun, target, low, high):
    # Binary search, find the lowest x where fun(x) >= target
    while low < high:
        mid = (low + high) // 2
        if fun(mid) < target:
            low = mid + 1
        else:
            high = mid
    return low


def do_one_case(low, high):
    # r1 = count_digits_between_two_numbers_slow(low, high)
    total_digits = count_digits_between_two_numbers_fast(low, high)
    target = total_digits // 2

    estimated_cut = binary_search(lambda x: count_digits_between_two_numbers_fast(low, x), target, low, high)
    digits_at_cut = count_digits_between_two_numbers_fast(low, estimated_cut)
    if digits_at_cut == target:
        r = estimated_cut
    else:
        r = estimated_cut - 1
    print(r)


# ********************************************************

reader = InputReader(2)
data = reader.get_start_parameters()

for low, high in data:
    do_one_case(low, high)
