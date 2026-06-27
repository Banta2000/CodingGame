from typing import Callable, Any


class BinarySearch:
    """A reusable binary search class for finding values in monotonic functions."""

    def __init__(self, func: Callable[[int], Any], low: int, high: int):
        """
        Initialize binary search with a function and search range.

        Args:
            func: The monotonic function to search on
            low: Lower bound of search range (inclusive)
            high: Upper bound of search range (inclusive)
        """
        self.func = func
        self.low = low
        self.high = high

    def find_first_ge(self, target: Any) -> int:
        """Find the lowest x where func(x) >= target."""
        low, high = self.low, self.high + 1
        while low < high:
            mid = (low + high) // 2
            if self.func(mid) < target:
                low = mid + 1
            else:
                high = mid
        return low

    def find_last_le(self, target: Any) -> int:
        """Find the highest x where func(x) <= target."""
        low, high = self.low, self.high + 1
        while low < high:
            mid = (low + high) // 2
            if self.func(mid) <= target:
                low = mid + 1
            else:
                high = mid
        return low - 1

    def find_exact(self, target: Any) -> int:
        """Find x where func(x) == target, or -1 if not found."""
        pos = self.find_first_ge(target)
        if pos <= self.high and self.func(pos) == target:
            return pos
        return -1

    def find_first_gt(self, target: Any) -> int:
        """Find the lowest x where func(x) > target."""
        low, high = self.low, self.high + 1
        while low < high:
            mid = (low + high) // 2
            if self.func(mid) <= target:
                low = mid + 1
            else:
                high = mid
        return low

    def find_last_lt(self, target: Any) -> int:
        """Find the highest x where func(x) < target."""
        low, high = self.low, self.high + 1
        while low < high:
            mid = (low + high) // 2
            if self.func(mid) < target:
                low = mid + 1
            else:
                high = mid
        return low - 1
