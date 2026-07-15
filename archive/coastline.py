from typing import NamedTuple
import math
from cgutils.coding_game_helper import CodingGameHelper

class Point(NamedTuple):
    x: float
    y: float

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

def read_input() -> list[list]:
    """Reads all test cases from the provided input helper."""
    n_str = CGH.input()
    if not n_str:
        return []
    
    n = int(n_str)
    cases = []
    for _ in range(n):
        parts = [int(x) for x in CGH.input().split() if x]
        if not parts:
            continue
        # Format: [p_count, radius, x1, y1, ... xp, yp]
        radius = parts[1]
        coords = parts[2:]
        points = [Point(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]
        cases.append([radius] + points)
    return cases

def get_coverage_interval(p: Point, r: int) -> tuple[float, float] | None:
    """Calculates the x-range on the coast where a transmitter can cover point p."""
    if abs(p.y) > r:
        return None
    dx = math.sqrt(r**2 - p.y**2)
    return (p.x - dx, p.x + dx)

def solve_minimum_transmitters(case_data: list) -> int:
    """
    Finds the minimum number of coastline transmitters using the Hitting Set Greedy algorithm.
    Time Complexity: O(N log N)
    """
    radius = case_data[0]
    points = case_data[1:]
    
    intervals = []
    for p in points:
        interval = get_coverage_interval(p, radius)
        if interval is None:
            return -1
        intervals.append(interval)

    # Fundamental Greedy Strategy: Sort by right endpoint.
    # Picking the rightmost point of an interval covers it and maximizes the chance of covering future ones.
    intervals.sort(key=lambda x: x[1])

    count = 0
    last_transmitter_x = -float('inf')

    for start, end in intervals:
        if start > last_transmitter_x + 1e-9:
            count += 1
            last_transmitter_x = end
            
    return count

# ********************************************************

CGH = CodingGameHelper(1, __file__)
all_cases = read_input()

for case in all_cases:
    result = solve_minimum_transmitters(case)
    CGH.print(str(result))

