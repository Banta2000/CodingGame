import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        arr = [4, 1, 8, 3, 7, 5, 6, 2]
        data = {4: "R", 1: "P", 8: "P", 3: "R", 7: "C", 5: "S", 6: "L", 2: "L"}
    else:
        n = int(input())
        data = {}
        arr = []
        for _ in range(n):
            inputs = input().split()
            numplayer = int(inputs[0])
            signplayer = inputs[1]
            data[numplayer] = signplayer
            arr.append(numplayer)

    if print_input:
        myPrint(data)

    return data, arr


# Define winning conditions in a dictionary
WINNING_CONDITIONS = {"R": ["S", "L"], "P": ["R", "S"], "C": ["P", "L"], "L": ["P", "S"], "S": ["R", "C"]}


def get_winner(p1_sign: str, p2_sign: str) -> str:
    if p1_sign == p2_sign:
        return "DRAW"
    elif p2_sign in WINNING_CONDITIONS[p1_sign]:
        return "Player 1"
    else:
        return "Player 2"


def do_one_round(
    arr: list[int], data: dict[int, str], history: dict[int, list[int]]
) -> tuple[list[int], dict[int, list[int]]]:
    new_arr = []
    for i in range(0, len(arr), 2):
        p1_num, p2_num = arr[i], arr[i + 1]
        p1_sign, p2_sign = data[p1_num], data[p2_num]
        res = get_winner(p1_sign, p2_sign)

        if res == "Player 1":
            winner, looser = p1_num, p2_num
        elif res == "Player 2":
            winner, looser = p2_num, p1_num
        else:  # DRAW
            winner, looser = min(p1_num, p2_num), max(p1_num, p2_num)

        new_arr.append(winner)
        history[winner].append(looser)

    return new_arr, history


# ********************************************************

data, arr = get_start_parameters(print_input=True)
history = {k: [] for k in data}
while len(arr) > 1:
    arr, history = do_one_round(arr, data, history)

winner = arr[0]
history = history[winner]
history = " ".join(map(str, history))
print(winner)
print(history)
