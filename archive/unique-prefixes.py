import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> List:
    if HOME_PC:
        words = ['find', 'the', 'shortest', 'unique', 'prefix']
    else:
        n = int(input())
        words = [input() for _ in range(n)]

    if print_input:
        myPrint(words)

    return words


def is_unique(word: str, LU: set, s_len: int) -> str:
    prim_word = word[:s_len]
    db = [x for x in LU if x != word]
    db = [x[:s_len] for x in db]
    return not prim_word in db


def find_unique_prefix(word: str, LU: set) -> str:
    for i in range(len(word)):
        if is_unique(word, LU, i):
            return word[:i]
    return word

# ********************************************************

words = get_start_parameters(print_input=True)

# words = ["alphabet", "book", "carpet", "cadmium", "cadeau", "alpine"]
# words = ['A', 'AA', 'AAA']
LU = set(words)
res = [find_unique_prefix(x, LU) for x in words]
for word in res: print(word)
