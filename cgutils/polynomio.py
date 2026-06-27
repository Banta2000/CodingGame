from dataclasses import dataclass
from typing import Tuple

Point = Tuple[int, int]
PointSet = frozenset[Point]


@dataclass(frozen=True)
class Polynomio:
    """
    A polynomio is a shape made from occupied cells on a 2D integer grid.

    This class stores the shape as a set of grid points and provides common
    geometric operations such as translation-normalization, rotation, mirroring,
    and canonicalization. The main idea is that two shapes should count as the
    same even if one has been shifted, rotated, or reflected.

    By converting each equivalent variant into a normalized representation and
    choosing a consistent minimum form, the class makes it easy to compare,
    hash, and reuse grid-based puzzle pieces across different problems.
    """

    points: PointSet

    def __post_init__(self):
        object.__setattr__(self, "points", frozenset(self.points))

    def centered(self) -> "Polynomio":
        """Translate the shape so that its top-left point is at (0, 0)."""
        minRow = min(p[0] for p in self.points)
        minCol = min(p[1] for p in self.points)
        translated_points = frozenset((r - minRow, c - minCol) for (r, c) in self.points)
        return Polynomio(translated_points)

    def rotated(self) -> "Polynomio":
        """Rotate the shape 90 degrees clockwise around the origin."""
        rotated_points = frozenset((c, -r) for (r, c) in self.points)
        return Polynomio(rotated_points)

    def mirrored(self) -> "Polynomio":
        """Mirror the shape horizontally."""
        mirrored_points = frozenset((r, -c) for (r, c) in self.points)
        return Polynomio(mirrored_points)

    def normalized(self) -> "Polynomio":
        """Return the canonical form across all rotations and mirror variants."""
        transformations = []
        current = self
        for _ in range(4):
            transformations.append(current.centered())
            transformations.append(current.mirrored().centered())
            current = current.rotated()
        return min(transformations, key=lambda s: sorted(s.points))

    def print(self):
        """Print the shape as a small text grid for debugging."""
        minRow = min(p[0] for p in self.points)
        maxRow = max(p[0] for p in self.points)
        minCol = min(p[1] for p in self.points)
        maxCol = max(p[1] for p in self.points)
        for r in range(minRow, maxRow + 1):
            for c in range(minCol, maxCol + 1):
                p = (r, c)
                c = "#" if p in self.points else "."
                print(c, end="")
            print()
        print()
