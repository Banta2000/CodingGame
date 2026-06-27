import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Game:
    if HOME_PC:
        n = "11123159995399999"
        n = "19"
    else:
        n = input()

    n = int(n)
    if print_input:
        myPrint(n)
    return n


def is_growing_number(n: int) -> bool:
    n = str(n)
    for i in range(1, len(n)):
        if n[i] < n[i - 1]:
            return False
    return True


def next_growing_number(n: int) -> int:
    has_reset = False
    n = list(str(n))
    for i in range(1, len(n)):
        if has_reset:
            n[i] = n[i - 1]
        else:
            if n[i] >= n[i - 1]:
                continue
            n[i] = n[i - 1]
            has_reset = True
    return int("".join(n))


# ********************************************************

num = get_start_parameters(print_input=True)
num += 1
r = next_growing_number(num)
print(r)
