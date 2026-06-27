import os
from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper


def read_input(CGH: CodingGameHelper):
    height = int(CGH.input())
    increments = [CGH.input() for _ in range(height)]
    prizes = [int(CGH.input()) for _ in range(height + 1)]
    res = []
    for line in increments:
        line = [int(char) for char in line]
        res.append(line)
    return res, prizes


def create_max_prices(board):
    res = [board[0]]
    for i, line in enumerate(board[1:]):
        new_line = []
        for j, char in enumerate(line):
            if j == 0:
                new_line.append(res[-1][0] + char)
                continue
            if j == len(line) - 1:
                new_line.append(res[-1][-1] + char)
                continue
            new_line.append(max(res[-1][j - 1], res[-1][j]) + char)
        res.append(new_line)
    return res[-1]


# ********************************************************

CGH = CodingGameHelper(4, __file__)
board, prices = read_input(CGH)
end_values = create_max_prices(board)

result = [end_values[0] * prices[0]]
for i, price in enumerate(prices[1:-1]):
    a = end_values[i]
    b = end_values[i + 1]
    result.append(max(a, b) * price)
result.append(end_values[-1] * prices[-1])
CGH.add_output_line(max(result))
CGH.assert_output()

# print(board)
# CGH.add_output_line(XXXXX)
# CGH.assert_output()


#     0           0
#    1 2         1 2
#   0 1 2       1 3 4
#  0 1 2 0     1 4 6 4
# 1 2 0 1 2   2 6 6 7 6


#            ●
#            0↘
#          1   2↘
#        0   1  ↙2
#      0   1   2↘  0
#    1   2   0   1↘  2
#    |   |   |   | ● |
# 900│600│300│500│700│800
