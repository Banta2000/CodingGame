import sys
import os
import math
from typing import Any, Tuple, List

Game = dict[str, Any]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Tuple[float, float]:
    if HOME_PC:
        side = 98.95
        diameter = 0.215
    else:
        side, diameter = [float(i) for i in input().split()]

    if print_input:
        myPrint(f"{side=}")
        myPrint(f"{diameter=}")

    return side, diameter


def get_minimum_square(side: float, diameter: float) -> float:
    r = side // diameter
    return r * diameter


def get_number_doughnut_wasteful(side: float, diameter: float) -> int:
    min_side = get_minimum_square(side, diameter)
    res = min_side / diameter
    return round(res * res)


def get_waste_on_sides(side: float, diameter: float) -> float:
    min_side = get_minimum_square(side, diameter)
    min_area = min_side * min_side
    return side * side - min_area


def get_waste_in_area(side: float, diameter: float) -> float:
    doughnut_area = (diameter / 2) * (diameter / 2) * math.pi
    doughnut_waste = diameter * diameter - doughnut_area
    num_doughnuts_wasteful = get_number_doughnut_wasteful(side, diameter)
    in_area_waste = num_doughnuts_wasteful * doughnut_waste
    return in_area_waste


# ********************************************************
HOME_PC = True
side, diameter = get_start_parameters(print_input=False)
num_wasteful_doughnuts = get_number_doughnut_wasteful(side, diameter)

num_frugal_doughnuts = 0
while side >= diameter:
    num_frugal_doughnuts += get_number_doughnut_wasteful(side, diameter)
    waste_in_area = get_waste_in_area(side, diameter)
    waste_on_sides = get_waste_on_sides(side, diameter)
    dough = waste_in_area + waste_on_sides
    side = math.sqrt(dough)

print(num_frugal_doughnuts - num_wasteful_doughnuts)
