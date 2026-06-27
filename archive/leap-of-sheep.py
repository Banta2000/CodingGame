from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper


Point = Tuple[int, int]
Board = dict[Point, Any]


def read_input():
    _ = int(CGH.input())
    heights = [int(i) for i in CGH.input().split()]
    return heights


# ********************************************************

CGH = CodingGameHelper(3, __file__)
lines = read_input()
best = 0
for i in range(1, len(lines) - 1):
    m1 = min(lines[:i])
    m2 = lines[i]
    m3 = min(lines[i + 1:])
    if m1 >= m2 or m3 >= m2:
        continue
    best = max(best, (m2 - m1) + (m2 - m3))
CGH.print(best)
CGH.assert_output()
