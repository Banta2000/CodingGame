import sys
import os
from typing import Any, Tuple, List
from math import sqrt

Coord = Tuple[int, int, int]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Tuple[Coord, Coord]:
    if HOME_PC:
        ship='133i - 6 j -8k'
        wormhole='4i +8j -44 k'
    else:
        ship = input()
        wormhole = input()

    if print_input:
        myPrint(f"{ship=}")
        myPrint(f"{wormhole=}")

    ship, wormhole = parse_ship(ship), parse_ship(wormhole)
    return ship, wormhole


# Returns a tuple of 3 integers representing the ship's coordinates (i, j, k)
def parse_ship(ship: str) -> Tuple[int, int, int]:
    ship = ship.replace(" ", "")
    tmp = ""
    res = {}
    for char in ship:
        if char in ["i", "j", "k"]:
            if tmp == "" or tmp == "-" or tmp == "+":
                tmp += "1"
            res[char] = int(tmp)
            tmp = ""
        else:
            tmp += char
    for x in ["i", "j", "k"]:
        if x not in res:
            res[x] = 0
    return (res["i"], res["j"], res["k"])


# Returns the distance between two coordinates
def get_distance(a: Coord, b: Coord) -> int:
    dist = sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
    return round(dist, 2)


# Converts the distance tupple into a printable version
def get_printable_direction(v: Coord) -> str:
    def get_ind_number(num):
        if num == 0:
            return ""
        if num == 1:
            return "+"
        if num == -1:
            return "-"
        if num > 0:
            return "+" + str(num)
        if num < 0:
            return str(num)

    a, b, c = [get_ind_number(x) for x in v]
    v2 = a + "i", b + "j", c + "k"
    v3 = [b for a, b in zip(v, v2) if a != 0]
    v3 = "".join(v3)
    if v3[0] == "+":
        v3 = v3[1:]
    return v3


def remove_common_denominator(v: Coord) -> Coord:
    a, b, c = v
    min_ = min([abs(x) for x in [a, b, c] if x != 0])
    for i in range(2, min_ + 1):
        if a % i == 0 and b % i == 0 and c % i == 0:
            return remove_common_denominator((a // i, b // i, c // i))
    return (a, b, c)


# Returns the direction from a to b
def get_direction(a: Coord, b: Coord) -> Coord:
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


# ********************************************************

ship, wormhole = get_start_parameters(print_input=True)
dist = get_distance(ship, wormhole)
dir = get_direction(ship, wormhole)
dir = remove_common_denominator(dir)
dir = get_printable_direction(dir)
print(f"Direction: {dir}")
print(f"Distance: {dist}")
