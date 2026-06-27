from typing import List, Tuple, Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2D:
    """
    2D Vector. Immutable and hashable, suitable for use as dictionary keys.
    Supports arithmetic operator overloading for vector math.
    """

    row: int
    col: int

    # ===== MAGIC METHODS (dunder methods) =====
    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.row + other.row, self.col + other.col)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.row - other.row, self.col - other.col)

    def __mul__(self, scalar: int) -> "Vector2D":
        return Vector2D(self.row * scalar, self.col * scalar)

    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.row, -self.col)

    def __iter__(self) -> Iterator[int]:
        yield self.row
        yield self.col

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.row
        elif index == 1:
            return self.col
        else:
            raise IndexError("Vector2D index out of range")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"

    # ===== PROPERTIES =====
    @property
    def x(self) -> int:
        return self.col

    @property
    def y(self) -> int:
        return self.row

    # ===== DISTANCE CALCULATIONS =====
    def manhattan_distance(self, other: "Vector2D") -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def euclidean_distance_squared(self, other: "Vector2D") -> int:
        dr = self.row - other.row
        dc = self.col - other.col
        return dr * dr + dc * dc

    def euclidean_distance(self, other: "Vector2D") -> float:
        return self.euclidean_distance_squared(other) ** 0.5

    # ===== NEIGHBOR AND ADJACENCY =====
    def neighbors_4(self) -> List["Vector2D"]:
        directions = [Vector2D(-1, 0), Vector2D(1, 0), Vector2D(0, -1), Vector2D(0, 1)]
        return [self + d for d in directions]

    def neighbors_8(self) -> List["Vector2D"]:
        directions = [
            Vector2D(-1, -1),
            Vector2D(-1, 0),
            Vector2D(-1, 1),
            Vector2D(0, -1),
            Vector2D(0, 1),
            Vector2D(1, -1),
            Vector2D(1, 0),
            Vector2D(1, 1),
        ]
        return [self + d for d in directions]

    def up(self) -> "Vector2D":
        return Vector2D(self.row - 1, self.col)

    def down(self) -> "Vector2D":
        return Vector2D(self.row + 1, self.col)

    def left(self) -> "Vector2D":
        return Vector2D(self.row, self.col - 1)

    def right(self) -> "Vector2D":
        return Vector2D(self.row, self.col + 1)

    # ===== TRANSFORMATIONS =====
    def rotate_90_cw(self) -> "Vector2D":
        return Vector2D(self.col, -self.row)

    def rotate_90_ccw(self) -> "Vector2D":
        return Vector2D(-self.col, self.row)

    def move(self, direction: "Vector2D", steps: int = 1) -> "Vector2D":
        return self + (direction * steps)

    # ===== CONVERSION =====
    def to_tuple(self) -> Tuple[int, int]:
        return (self.row, self.col)

    @classmethod
    def from_tuple(cls, t: Tuple[int, int]) -> "Vector2D":
        return cls(t[0], t[1])

    @staticmethod
    def origin() -> "Vector2D":
        return Vector2D(0, 0)
