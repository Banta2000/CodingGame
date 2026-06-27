import sys
import os
from typing import Any, Tuple
import random

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
        full_end = 12
        data = [(6, 10), (0, 4), (7, 8), (3, 7), (8, 12)]

    else:
        full_end = int(input())
        n = int(input())
        data = []
        for _ in range(n):
            st, ed = [int(j) for j in input().split()]
            data.append((st, ed))

    if print_input:
        myPrint(f"full_end = {full_end}")
        myPrint(f"data = {data}")

    data.sort(key=lambda x: x[0])
    return data, full_end


def simplify_intervals(data: list[Tuple[int, int]]) -> list[Tuple[int, int]]:
    result = [data[0]]
    for s, e in data[1:]:
        if s > result[-1][1]:
            result.append((s, e))
        else:
            s_old, e_old = result.pop()
            new_entry = (s_old, max(e_old, e))
            result.append(new_entry)
    return result


def find_intervals_between(data, full_end):
    result = []
    s_old, e_old = data[0]

    if s_old > 0:
        result.append((0, s_old))

    for s_new, e_new in data[1:]:
        result.append((e_old, s_new))
        s_old, e_old = s_new, e_new

    if e_old < full_end:
        result.append((e_old, full_end))
    return result


# ********************************************************

data, full_end = get_start_parameters(print_input=True)
data = simplify_intervals(data)
res = find_intervals_between(data, full_end)

if res == []:
    print("All painted")
else:
    for s, e in res:
        print(s, e)
