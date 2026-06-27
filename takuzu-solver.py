import os
from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper


def read_input(CGH: CodingGameHelper) -> list[str]:
    n = int(CGH.input())
    lines = [CGH.input() for _ in range(n)]
    return lines


# ********************************************************

CGH = CodingGameHelper(1, __file__)
lines = read_input(CGH)
print(lines)

# CGH.add_output_line(XXXXX)
# CGH.assert_output()


# for case_nr in range(1, 4):
