import os
import logging
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"

logging.basicConfig(level=logging.INFO)


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node = None
        self.right: Node = None
        self.parent: Node = None

    def __repr__(self) -> str:
        return f"Node({self.value})"

    def insert_left(self, value: int) -> None:
        self.left = Node(value)
        self.left.parent = self

    def insert_right(self, value: int) -> None:
        self.right = Node(value)
        self.right.parent = self

    def insert(self, value: int) -> None:
        if value < self.value:
            if self.left is None:
                self.insert_left(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.insert_right(value)
            else:
                self.right.insert(value)


def explore_tree(node: Node) -> List[str]:
    result: List[str] = []
    if node.left:
        result.append("L")
        result.extend(explore_tree(node.left))
    if node.right:
        result.append("R")
        result.extend(explore_tree(node.right))
    result.append("B")
    return result


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        data = ["5 9 8 1 7", "6 10 9 8 5", "5 2 7 3 10", "7 9 4 2 10"]
    else:
        n, k = [int(i) for i in input().split()]
        data = [input() for _ in range(n)]

    data = [line.split() for line in data]
    data = [[int(i) for i in line] for line in data]
    return data


def main():
    trees = get_start_parameters()
    solutions = set()
    for tree in trees:
        logging.info(f"Processing tree: {tree}")
        root = Node(tree[0])
        for i in range(1, len(tree)):
            root.insert(tree[i])
        res = "".join(explore_tree(root))
        solutions.add(res)
    logging.info(f"Unique solutions: {solutions}")
    print(len(solutions))


if __name__ == "__main__":
    main()
