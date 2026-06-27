import sys
import os
from typing import Any, Tuple
from dataclasses import dataclass


HOME_PC: bool = os.getenv("HOME_PC") == "true"


@dataclass
class Point:
    label: str
    coord: list[int]


PointList = list[Point]


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_initial_GS() -> PointList:
    points = []
    if HOME_PC:
        points.append(Point(label="a", coord=[4, 7]))
        points.append(Point(label="e", coord=[5, 6]))
        points.append(Point(label="G", coord=[5, 2]))
        points.append(Point(label="r", coord=[4, 4]))
        points.append(Point(label="t", coord=[3, 10]))
        points.append(Point(label="!", coord=[0, 9]))

    else:
        count, _ = [int(i) for i in input().split()]
        for _ in range(count):
            label, *coord = input().split()
            coord = [int(i) for i in coord]
            points.append(Point(label, coord))

    # for line in points:
    # myPrint(line)
    return points


# Returs distance between two points
def distance(p1: Point, p2: Point) -> float:
    return sum((c1 - c2) ** 2 for c1, c2 in zip(p1.coord, p2.coord)) ** 0.5


# Returns point in list of point that is closest to refrerence point
def find_closest_point(points: PointList, reference: Point) -> Point:
    closest_point = min(points, key=lambda p: distance(p, reference))
    return closest_point


# Returns and removes point from list of points that is closest to refrerence point
def find_and_remove_closest_point(points: PointList, reference: Point) -> Point:
    closest_point = find_closest_point(points, reference)
    points.remove(closest_point)
    return closest_point


# Returns True if two points are in different quadrants
def is_different_quadrants(p1: Point, p2: Point) -> bool:
    return any(c1 * c2 < 0 for c1, c2 in zip(p1.coord, p2.coord))


# ********************************************************

points = get_initial_GS()
current = Point("_", [0 for _ in range(len(points[0].coord))])

res = ""
while points:
    last = current
    current = find_and_remove_closest_point(points, last)
    if is_different_quadrants(last, current):
        res += " "
    res += current.label

print(res)
