import os
from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper


def read_input(CGH: CodingGameHelper) -> list[int]:
    n = int(CGH.input())
    lst = [int(CGH.input()) for _ in range(n)]
    return lst


# ********************************************************


for case_nr in range(1, 6):
    CGH = CodingGameHelper(3, __file__)
    lst = read_input(CGH)

    LU = {}
    for num in lst:
        # collect all previous options
        options_before = [v for k, v in LU.items() if k < num]
        options_before = max(options_before) if options_before else 0
        LU[num] = options_before + 1

    max_lu = max(LU.values())
    CGH.add_output_line(max_lu)
    CGH.assert_output()
