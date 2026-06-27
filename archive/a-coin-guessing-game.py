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
        [num_coins, num_throws] = [int(x) for x in self.input().split()]
        lines = [self.input() for _ in range(num_throws)]
        lines = [line.split() for line in lines]
        lines = [[int(x) for x in line] for line in lines]
        return num_coins, lines


def build_map(num_coins: int):
    """Each coin has a value from 1 to 2*num_coins"""
    max_coin_value = 2 * num_coins
    odd_coins = {x for x in range(1, max_coin_value + 1) if x % 2 == 1}
    even_coins = {x for x in range(1, max_coin_value + 1) if x % 2 == 0}

    # Each coin can initially pair with any coin of opposite parity
    possible_pairings = {}
    for coin_value in range(1, max_coin_value + 1):
        if coin_value % 2 == 0:
            possible_pairings[coin_value] = odd_coins.copy()
        else:
            possible_pairings[coin_value] = even_coins.copy()
    return possible_pairings


def evaluate_throw(throw: List[int]):
    """Process a throw to eliminate impossible pairings based on sum constraint."""
    odd = [x for x in throw if x % 2 == 1]
    even = [x for x in throw if x % 2 == 0]
    for num in odd:
        mapper[num] = mapper[num] - set(even)
    for num in even:
        mapper[num] = mapper[num] - set(odd)


def find_next_candidate():
    for k, v in mapper.items():
        if k not in solved and len(v) == 1:
            return k
    return None


# ********************************************************

reader = InputReader(8)
num_coins, throws = reader.get_start_parameters()
mapper = build_map(num_coins)
for throw in throws:
    evaluate_throw(throw)

solved = set()

while True:
    a = find_next_candidate()
    if a is None:
        break
    b = list(mapper[a])[0]
    solved.add(a)
    solved.add(b)
    for k, v in mapper.items():
        if a == k or b == k:
            continue
        if a in v:
            v.remove(a)
        if b in v:
            v.remove(b)

# for k, v in mapper.items():
# print(k, v)

res = [v for k, v in mapper.items() if k % 2 == 1]
res = [list(x)[0] for x in res]
res = " ".join([str(x) for x in res])
print(res)
