from typing import Any, Tuple, List
from cgutils import Board, Point2D
from cgutils.coding_game_helper import CodingGameHelper


Point = Tuple[int, int]
Board = dict[Point, Any]


def read_input() -> list[str]:
    # IMPLEMENT HERE THE READING ALGO, USE CGH.input() to read the input
    lines = [....CGH.input()]
    return lines


# ********************************************************

CGH = CodingGameHelper(1, __file__)
lines = read_input()
print(lines)

CGH.print(XXXXX)
CGH.assert_output()


# for case_nr in range(1, 4):
# CGH.print prints the line and also adds it to the queue for assert_output
# At the end, simply remove all CGH. from the code and it should work without the need to import CGH utils
