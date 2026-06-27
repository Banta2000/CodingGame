import os
from cgutils.coding_game_helper import CodingGameHelper
from cgutils.bstnode import BSTNode


def read_input(CGH: CodingGameHelper) -> list[int]:
    n = int(CGH.input())
    return [int(i) for i in CGH.input().split()]


# ********************************************************

CGH = CodingGameHelper(1, __file__)
lines = read_input(CGH)
root = BSTNode(lines[0])
for val in lines[1:]:
    root.insert(val)

preorder = root.traverse("preorder")
CGH.add_output_line(" ".join(str(i) for i in preorder))

inorder = root.traverse("inorder")
CGH.add_output_line(" ".join(str(i) for i in inorder))

postorder = root.traverse("postorder")
CGH.add_output_line(" ".join(str(i) for i in postorder))

collector = root.explore_by_level()
res = []
max_level = max(collector.keys())
for level in range(max_level + 1):
    res += collector[level]
CGH.add_output_line(" ".join(str(i) for i in res))

CGH.assert_output()
