import sys
import os
from typing import Any, Tuple, List
import math

HOME_PC: bool = os.getenv("HOME_PC") == "True"


class Point:
    def __init__(self, id: int, x: int, y: int) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.neighbours = []

    def __repr__(self) -> str:
        # return f"P:{self.id} ({self.x}, {self.y})"
        return f"P{self.id}"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Point") -> "Point":
        if not isinstance(other, Point):
            return NotImplemented
        return Point(None, self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        if not isinstance(other, Point):
            return NotImplemented
        return Point(None, self.x - other.x, self.y - other.y)

    def angle(self):
        if self.x == 0 and self.y == 0:
            return 0
        angle = math.atan2(self.y, self.x)
        if angle == math.pi:
            angle = 0
        elif angle < 0:
            angle = math.pi - abs(angle)
        return angle


def get_start_parameters() -> dict[int, Point]:
    if HOME_PC:
        #  Example
        k = 3
        n = 3
        p = 1
        raw_points = [
            (200, 200),
            (400, 300),
            (400, 100),
        ]

        # Parallelogram
        k = 4
        n = 10
        p = 0
        raw_points = [(200, 200), (400, 190), (400, 100), (200, 90)]

        # 10 Random Points
        # k = 10
        # n = 30
        # p = 5
        # raw_points = [
        #     (654, 114),
        #     (25, 281),
        #     (250, 228),
        #     (142, 104),
        #     (692, 558),
        #     (89, 432),
        #     (32, 30),
        #     (95, 223),
        #     (238, 517),
        #     (616, 27),
        # ]

        # raw_points = [
        #     (8, 6),
        #     (13, 7),
        #     (11, 10),
        #     (8, 11),
        #     (5, 10),
        #     (4, 8),
        #     (3, 6),
        #     (4, 4),
        #     (6, 2),
        #     (8, 2),
        #     (10, 2),
        #     (12, 4),
        #     (15, 6),
        # ]

    else:
        k = int(input())
        n = int(input())
        p = int(input())
        raw_points = []
        for i in range(k):
            x, y = [int(j) for j in input().split()]
            raw_points.append((x, y))

    Points = {}
    for i, coord in enumerate(raw_points):
        Points[i] = Point(i, *raw_points[i])
    return n, p, Points


def build_graph(Points: dict[int, Point]) -> None:
    for a in Points.values():
        for b in Points.values():
            if a == b:
                continue
            c = b - a
            a.neighbours.append((b, c.angle()))

    for p in Points.values():
        p.neighbours.sort(key=lambda x: x[1], reverse=True)
        p.neighbours = [x[0] for x in p.neighbours]


def next_pivot(coming_from: Point, current: Point) -> Point:
    # find the id of coming_from in current.neighbours
    for i, p in enumerate(current.neighbours):
        if p == coming_from:
            break
    i = (i + 1) % len(current.neighbours)
    return current.neighbours[i]


# ********************************************************

num_rounds, start_point_idx, Points = get_start_parameters()
build_graph(Points)
result_counter = {p.id: 0 for p in Points.values()}
sequence = []

curr_pivot = Points[start_point_idx]
future_pivot = curr_pivot.neighbours[0]
result_counter[curr_pivot.id] += 1
sequence.append((curr_pivot.id, future_pivot.id))
use_shortcut = True

i = 0
while i < num_rounds:
    # print(i)
    old_pivot = curr_pivot
    curr_pivot = future_pivot
    future_pivot = next_pivot(old_pivot, curr_pivot)
    state_transition = (curr_pivot.id, future_pivot.id)
    if state_transition in sequence and use_shortcut:
        cycle_length = i + 1
        remaining_full_cycles = (num_rounds // cycle_length) - 1
        for k, v in result_counter.items():
            result_counter[k] += v * remaining_full_cycles
        i += cycle_length * remaining_full_cycles
        shorten_calc = False
    result_counter[curr_pivot.id] += 1
    sequence.append(state_transition)
    i += 1


print(curr_pivot.id)
for k, v in result_counter.items():
    print(v)

# for entry in sequence:
# print(entry[0], entry[1])

# print(" ".join(str(x) for x in sequence))


# # 5

# 0  # 10
# 1  # 10
# 2  # 0
# 3  # 15
# 4  # 10
# 5  # 11
# 6  # 10
# 7  # 15
# 8  # 10
# 9  # 10


# 2
# 3
# 3
# 3
# 2
