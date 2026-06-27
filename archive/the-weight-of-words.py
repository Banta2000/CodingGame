import sys
import os
from typing import Any, Tuple

Data = list[str]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        steps = 3
        data = ["YDOS", "CEAE"]
    else:
        steps = int(input())
        h = int(input())
        w = int(input())
        data = [input() for _ in range(h)]

    if print_input:
        myPrint(f"steps = {steps}")
        myPrint(f"data = {data}")

    data = [[x for x in line] for line in data]

    return steps, data


def val_letter(letter: str) -> int:
    return ord(letter)


def val_word(word: str) -> int:
    return sum(val_letter(letter) for letter in word)


def rotate_word(word: str, steps: int) -> str:
    steps = steps % len(word)
    new_start = word[-steps:]
    new_end = word[:-steps]
    return new_start + new_end


def extract_col(data: Data, col: int) -> str:
    return "".join(row[col] for row in data)


def assign_col(data: Data, col: int, s: str):
    for i, letter in enumerate(s):
        data[i][col] = letter


def extract_row(data: Data, row: int) -> str:
    return data[row]


def assign_row(data: Data, row: int, s: str):
    data[row] = s


def one_rotation(data: Data):
    for col in range(len(data[0])):
        col_word = extract_col(data, col)
        num_rotation = val_word(col_word)
        new_word = rotate_word(col_word, num_rotation)
        assign_col(data, col, new_word)

    for row in range(len(data)):
        row_word = extract_row(data, row)
        num_rotation = val_word(row_word)
        new_word = rotate_word(row_word, num_rotation)
        assign_row(data, row, new_word)

    return data


# ********************************************************

steps, data = get_start_parameters(print_input=False)

for _ in range(steps):
    data = one_rotation(data)

data = ["".join(word) for word in data]
for line in data:
    print(line)
