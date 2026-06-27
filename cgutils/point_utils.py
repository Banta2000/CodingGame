from typing import List, NamedTuple


# Points are named tuples. They are exactly the same like a normal tuple, but come
# with fields, so that I can do p.row instead of p[0]. In order to get that,
# I have to define any point as p = Point(row, col) instead of p = (row, col).
# Normally a named tuple prints more verbose, but I have overriden the __repr__.

# Again, I can use a normal tuple if I want.


class Point(NamedTuple):
    row: int
    col: int

    def __repr__(self):
        return f"({self.row}, {self.col})"


# ===== NAMED DIRECTIONS =====


def up(p: Point) -> Point:
    return Point(p.row - 1, p.col)


def down(p: Point) -> Point:
    return Point(p.row + 1, p.col)


def left(p: Point) -> Point:
    return Point(p.row, p.col - 1)


def right(p: Point) -> Point:
    return Point(p.row, p.col + 1)


# ===== NEIGHBORS =====


def neighbors_4(p: Point) -> List[Point]:
    """4-directional neighbors (up, down, left, right)."""
    return [up(p), down(p), left(p), right(p)]


def neighbors_8(p: Point) -> List[Point]:
    """8-directional neighbors (including diagonals)."""
    r, c = p.row, p.col
    return [
        Point(r - 1, c - 1),
        Point(r - 1, c),
        Point(r - 1, c + 1),
        Point(r, c - 1),
        Point(r, c + 1),
        Point(r + 1, c - 1),
        Point(r + 1, c),
        Point(r + 1, c + 1),
    ]


# ===== TRANSFORMATIONS =====


def rotate_90_cw(p: Point) -> Point:
    """Rotate 90 degrees clockwise around origin."""
    return Point(p.col, -p.row)


def rotate_90_ccw(p: Point) -> Point:
    """Rotate 90 degrees counter-clockwise around origin."""
    return Point(-p.col, p.row)


def move(p: Point, direction: Point, steps: int = 1) -> Point:
    return Point(p.row + direction[0] * steps, p.col + direction[1] * steps)
