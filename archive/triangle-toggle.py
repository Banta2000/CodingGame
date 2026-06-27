from typing import List
from cgutils import Point2D

SAMPLES: dict = {
    "data2": [12, 10, "expanded", 1, "2 5 5 2 5 8"],
    "data3": [20, 20, "expanded", 2, "10 8 17 8 10 1", "10 18 3 11 17 11"],
}


class Triangle:
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
        # Check if a point is inside the triangle using barycentric coordinates
        x1, y1 = self.p1.col, self.p1.row
        x2, y2 = self.p2.col, self.p2.row
        x3, y3 = self.p3.col, self.p3.row
        x, y = p_target.col, p_target.row

        # Compute vectors
        denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if DEBUG:
            print(f"Denominator: {denominator}")  # Debugging line
        if denominator == 0:
            return False
        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        c = 1 - a - b
        if DEBUG:
            print(f"Point: {p_target}, a: {a}, b: {b}, c: {c}")
            print(0 <= a <= 1)
            print(0 <= b <= 1)
            print(0 <= c <= 1)
        return -0.01 <= a <= 1.01 and -0.01 <= b <= 1.01 and -0.01 <= c <= 1.01

    def flip_board(self, board):
        for p in board:
            if self.is_inside(p):
                board[p] = not board[p]
        return board


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        height, width, style, how_many_triangles, *str_triangles = data
        triangles = []
        for triangle in str_triangles:
            # Expect coordinates as y1 x1 y2 x2 y3 x3 (row, col) pairs
            y1, x1, y2, x2, y3, x3 = [int(x) for x in triangle.split()]
            # Point2D(row, col) = (y, x)
            p1, p2, p3 = Point2D(x1, y1), Point2D(x2, y2), Point2D(x3, y3)
            triangle = Triangle(p1, p2, p3)
            triangles.append(triangle)

        board = {}
        for r in range(height):
            for c in range(width):
                p = Point2D(r, c)
                board[p] = True
        return board, triangles, style

    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
        return parse(data)
    # Read from stdin
    height, width = [int(i) for i in input().split()]
    style = input().strip()
    how_many_triangles = int(input())
    tris: List[str] = []
    for _ in range(how_many_triangles):
        # Accept either "y x y x y x" or "x y x y x y"; normalize to y x order
        vals = [int(j) for j in input().split()]
        if len(vals) != 6:
            raise ValueError("Each triangle line must have 6 integers")
        a, b, c, d, e, f = vals
        # Heuristic: if any odd index seems like a row (<= height) and even like col (<= width), try (y x ...)
        # But to keep deterministic, assume input is "y x y x y x" as in samples.
        tris.append(f"{a} {b} {c} {d} {e} {f}")
    return parse([height, width, style, how_many_triangles, *tris])


def print_board(board, style):
    num_rows = max(p.row for p in board) + 1
    num_cols = max(p.col for p in board) + 1
    separator = " " if style == "expanded" else ""
    for r in range(num_rows):
        line = []
        for c in range(num_cols):
            p = Point2D(r, c)
            if p in board:
                line.append("*" if board[p] else " ")
        print(separator.join(line))


# ********************************************************

DEBUG = False

board, triangles, style = get_start_parameters("data3")

for triangle in triangles:
    board = triangle.flip_board(board)

print_board(board, style)
