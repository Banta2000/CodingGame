import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "True"


def get_start_parameters():
    if HOME_PC:
        num_kids = 3
        candy = "7 1 3 10 12 10"
        # num_kids = 3
        # candy = [7, 1, 3, 10, 12, 10]
    else:
        n, num_kids = [int(i) for i in input().split()]
        candy = input()

    candy = [int(i) for i in candy.split(" ")]
    candy.sort()

    if len(candy) < num_kids:
        print("ERROR: NOT ENOUGH KIDS")

    return num_kids, candy


# ********************************************************

num_kids, candy = get_start_parameters()

possible_res = []
for i in range(len(candy) - num_kids + 1):
    j = i + (num_kids - 1)
    possible_res.append(candy[j] - candy[i])

print(min(possible_res))
