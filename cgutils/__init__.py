"""Convenience imports for cgutils.

Usage:
    from cgutils import Point2D, Board, UnionSolver, Triangle, BinarySearch
"""

from .union_solver import UnionSolver
from .binary_search import BinarySearch

__all__ = [
    "UnionSolver",
    "BinarySearch",
    "binary_search",
]
