from typing import List
from .point2d import Point2D


class Triangle:
    """Minimal Triangle matching triangle-toggle behavior.

    - Stores three Point2D vertices (sorted by row, then col).
    - is_inside uses barycentric coordinates with a small tolerance.
    """

    def __init__(self, p1: Point2D, p2: Point2D, p3: Point2D):
        points = [p1, p2, p3]
        points.sort(key=lambda p: (p.row, p.col))
        self.p1 = points[0]
        self.p2 = points[1]
        self.p3 = points[2]

    def __repr__(self) -> str:
        return f"Triangle({self.p1}, {self.p2}, {self.p3})"

    def vertices(self) -> List[Point2D]:
        return [self.p1, self.p2, self.p3]

    def is_inside(self, p_target: Point2D) -> bool:
        # Returns if a given point is inside the triangle
        x1, y1 = self.p1.col, self.p1.row
        x2, y2 = self.p2.col, self.p2.row
        x3, y3 = self.p3.col, self.p3.row
        x, y = p_target.col, p_target.row

        denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if denominator == 0:
            return False
        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        c = 1 - a - b
        return -0.01 <= a <= 1.01 and -0.01 <= b <= 1.01 and -0.01 <= c <= 1.01
