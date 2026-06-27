import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "true"

LETTERS = {
    "A": "0x1818243C42420000",
    "B": "0x7844784444780000",
    "C": "0x3844808044380000",
    "D": "0x7844444444780000",
    "E": "0x7C407840407C0000",
    "F": "0x7C40784040400000",
    "G": "0x3844809C44380000",
    "H": "0x42427E4242420000",
    "I": "0x3E080808083E0000",
    "J": "0x1C04040444380000",
    "K": "0x4448507048440000",
    "L": "0x40404040407E0000",
    "M": "0x4163554941410000",
    "N": "0x4262524A46420000",
    "O": "0x1C222222221C0000",
    "P": "0x7844784040400000",
    "Q": "0x1C222222221C0200",
    "R": "0x7844785048440000",
    "S": "0x1C22100C221C0000",
    "T": "0x7F08080808080000",
    "U": "0x42424242423C0000",
    "V": "0x8142422424180000",
    "W": "0x4141495563410000",
    "X": "0x4224181824420000",
    "Y": "0x4122140808080000",
    "Z": "0x7E040810207E0000",
}


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> str:
    if HOME_PC:
        word = "ABC"
    else:
        word = input()
    if print_input:
        myPrint(f"{word=}")
    return word


# Transform the binary string into a readable of strings
def prettify(l: list) -> list:
    return ["".join(" " if x == "0" else "X" for x in line) for line in l]

def transform_letter(letter: str) -> List[str]:
    binary_value = bin(int(LETTERS[letter], 16))[2:].zfill(64)
    lines = [binary_value[i : i + 8] for i in range(0, 64, 8)]
    lines = prettify(lines)
    return lines


def flatten(l: List[List[str]]) -> List[str]:
    res = []
    for line_num in range(8):
        tmpline = ""
        for letter in l:
            tmpline += letter[line_num]
        res.append(tmpline)
    return res

def remove_empty_characters(s: str) -> str:
    return s.rstrip()

# ********************************************************

word = get_start_parameters(print_input=False)
word = [transform_letter(c) for c in word]
word = flatten(word)
word = [remove_empty_characters(line) for line in word]
word = [line for line in word if line]
for line in word:
    print(line)
