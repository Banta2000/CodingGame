from cgutils.coding_game_helper import CodingGameHelper
from cgutils.bstnode import BSTNode


def read_input(CGH: CodingGameHelper) -> list[BSTNode]:
    n = int(CGH.input())
    lines = []
    for i in range(n):
        line = [int(j) for j in CGH.input().split()]
        lines.append(line)
    nodes = []

    # Create all the nodes first
    for line in lines:
        node = BSTNode(line[0])
        nodes.append(node)

    # Attach nodes to each other
    for curr_idx, line in enumerate(lines):
        curr = nodes[curr_idx]
        left, right = line[1], line[2]
        if left != -1:
            curr.attach_left(nodes[left])
        if right != -1:
            curr.attach_right(nodes[right])

    return nodes


# ********************************************************

CGH = CodingGameHelper(3, __file__)
nodes = read_input(CGH)
res = nodes[0].to_ascii(vertical_spacing=1)
for line in res.splitlines():
    CGH.add_output_line(line)
CGH.assert_output(verbose=True)
