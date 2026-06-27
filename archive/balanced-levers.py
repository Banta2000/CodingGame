from __future__ import annotations

from typing import cast

from cgutils.coding_game_helper import CodingGameHelper


ChildId = int | None
BlueprintNode = list[int | None]
Blueprint = list[BlueprintNode]
Nodes = dict[int, "Node"]
Weights = list[int]
Spans = list[float]


def read_input(CGH: CodingGameHelper) -> tuple[float, int, Weights]:
    lim = float(CGH.input())
    n = int(CGH.input())
    vals = [int(i) for i in CGH.input().split()]
    return lim, n, vals


def select_blueprints(num_leaves: int) -> list[Blueprint]:
    # returns a collection of tree blueprints
    # every blueprint is a list of nodes, where each node is a list of [node_id, left_child_id, right_child_id]
    # generates all full binary tree topologies with exactly num_leaves leaves (Catalan(num_leaves-1) shapes)
    def gen(n: int) -> list[Blueprint]:
        if n == 1:
            return [[[0, None, None]]]
        results: list[Blueprint] = []
        for k in range(1, n):
            for l_conf in gen(k):
                for r_conf in gen(n - k):
                    lo, ro = 1, 1 + len(l_conf)
                    conf: Blueprint = [[0, lo, ro]]
                    for nid, l, r in l_conf:
                        left_child = None if l is None else l + lo
                        right_child = None if r is None else r + lo
                        conf.append([cast(int, nid) + lo, left_child, right_child])
                    for nid, l, r in r_conf:
                        left_child = None if l is None else l + ro
                        right_child = None if r is None else r + ro
                        conf.append([cast(int, nid) + ro, left_child, right_child])
                    results.append(conf)
        return results

    return gen(num_leaves)


class Node:
    def __init__(self, id: int):
        self.id = id
        self.val: int | None = None
        self.parent: Node | None = None
        self.left: Node | None = None
        self.left_len: float | None = None
        self.right: Node | None = None
        self.right_len: float | None = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        l = "None" if self.left is None else self.left.id
        r = "None" if self.right is None else self.right.id
        parent = "None" if self.parent is None else self.parent.id
        left_len = "None" if self.left_len is None else self.left_len
        right_len = "None" if self.right_len is None else self.right_len
        s = f"id: {self.id:>2} | val: {str(self.val):>6} | left: {str(l):>4} | right: {str(r):>4} | parent: {str(parent):>4} | left_len: {str(left_len):>6} | right_len: {str(right_len):>6}"
        return s


def build_tree_structure(conf: Blueprint) -> Nodes:
    num_nodes = max(cast(int, node[0]) for node in conf) + 1
    nodes: Nodes = {node_id: Node(node_id) for node_id in range(num_nodes)}
    for node, node_left, node_right in conf:
        node = cast(int, node)
        node = nodes[node]
        node_left = None if node_left is None else nodes[node_left]
        node_right = None if node_right is None else nodes[node_right]
        if node_left is not None:
            node.left = node_left
            node_left.parent = node
        if node_right is not None:
            node.right = node_right
            node_right.parent = node
    return nodes


def assign_leaf_values(nodes: Nodes, values: Weights) -> Nodes:
    i = 0
    for node in nodes.values():
        if node.left is None and node.right is None:
            node.val = values[i]
            i += 1

    if i != len(values):
        print("Not all leaf nodes received a value")
    return nodes


def compute_subtree_weights_and_lengths(nodes: Nodes) -> Nodes:
    for node in reversed(nodes.values()):
        if node.val is not None:
            node.left_len = 0
            node.right_len = 0

        if node.val is None:
            assert node.left is not None and node.right is not None
            assert node.left.val is not None and node.right.val is not None
            node.val = node.left.val + node.right.val
            node.left_len = 1 / node.val * node.right.val
            node.right_len = 1 / node.val * node.left.val
    return nodes


def explore_node_width(node: Node, pos: float) -> tuple[float, float]:
    if node.left is None:
        return pos, pos
    assert node.right is not None
    assert node.left_len is not None and node.right_len is not None
    left_min, left_max = explore_node_width(node.left, pos - node.left_len)
    right_min, right_max = explore_node_width(node.right, pos + node.right_len)
    return min(left_min, right_min), max(left_max, right_max)


def compute_tree_span(nodes: Nodes) -> float:
    # Takes a configured tree and computes its span.
    left, right = explore_node_width(nodes[0], 0)
    return right - left


def build_tree(blueprint: Blueprint, values: Weights) -> Nodes:
    # Builds a tree, assigns leaf values, and computes beam lengths.
    nodes = build_tree_structure(blueprint)
    nodes = assign_leaf_values(nodes, values)
    nodes = compute_subtree_weights_and_lengths(nodes)
    return nodes


def build_permutations(available: Weights, path: Weights | None = None) -> list[Weights]:
    if path is None:
        path = []
    if len(available) == 0:
        return [path]
    result: list[Weights] = []
    for i, num in enumerate(available):
        new_path = path + [num]
        new_available = available[:i] + available[i + 1 :]
        result += build_permutations(new_available, new_path)
    return result


def compute_spans_for_blueprint(blueprint: Blueprint, values: Weights) -> Spans:
    # Builds all value permutations and computes their spans for one blueprint.
    spans: Spans = []
    for permutation in build_permutations(values):
        tree = build_tree(blueprint, permutation)
        span = compute_tree_span(tree)
        spans.append(span)
    return spans


# ********************************************************


for i in range(1, 16):

    CGH = CodingGameHelper(i, __file__)
    max_span, n, values = read_input(CGH)
    blueprints = select_blueprints(n)

    possible_results = []
    for blueprint in blueprints:
        possible_results += compute_spans_for_blueprint(blueprint, values)

    possible_results = [span for span in possible_results if span <= max_span]
    if len(possible_results) == 0:
        end_result = -1
    else:
        end_result = max(possible_results)
        end_result = f"{round(end_result, 4):.4f}"
    CGH.add_output_line(end_result)
    CGH.assert_output(verbose=False)
