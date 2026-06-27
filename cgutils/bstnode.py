class BSTNode:
    """Represents one node in a binary search tree of integers."""

    def __init__(self, value: int):
        """Create a node with a value and no children."""
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def attach_left(self, child: "BSTNode | None"):
        """Attach child as the left node and keep the parent link in sync."""
        self.left = child
        if child is not None:
            child.parent = self

    def attach_right(self, child: "BSTNode | None"):
        """Attach child as the right node and keep the parent link in sync."""
        self.right = child
        if child is not None:
            child.parent = self

    def __repr__(self):
        """Return a string representation of the node and its children."""
        left = self.left.value if self.left else "None"
        right = self.right.value if self.right else "None"
        return f"BSTNode(value={self.value}, left={left}, right={right})"

    def insert(self, value: int):
        """Insert a value into the subtree rooted at this node."""
        if value < self.value:
            if self.left is None:
                self.attach_left(BSTNode(value))
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.attach_right(BSTNode(value))
            else:
                self.right.insert(value)

    def traverse(self, mode: str) -> list[int]:
        """Return the subtree values in inorder, preorder, or postorder."""
        left = self.left.traverse(mode) if self.left else []
        right = self.right.traverse(mode) if self.right else []
        if mode == "inorder":
            return left + [self.value] + right
        elif mode == "preorder":
            return [self.value] + left + right
        elif mode == "postorder":
            return left + right + [self.value]
        else:
            raise ValueError(f"Unknown traversal mode: {mode}")

    def explore_by_level(self, collector: dict[int, list[int]] | None = None, level: int = 0) -> dict[int, list[int]]:
        """Group subtree values by depth from left to right."""
        if collector is None:
            collector = {}
        if level not in collector:
            collector[level] = []
        collector[level].append(self.value)
        if self.left is not None:
            self.left.explore_by_level(collector, level + 1)
        if self.right is not None:
            self.right.explore_by_level(collector, level + 1)
        return collector

    def get_level(self, target: int) -> int:
        """Return the depth of target from this node, or -1 if not found."""
        if self.value == target:
            return 0

        left_value = self.left.get_level(target) if self.left is not None else -1
        right_value = self.right.get_level(target) if self.right is not None else -1

        if left_value != -1 and right_value != -1:
            raise ValueError(
                f"Target value {target} found in both left and right subtrees, " "which should not happen in a BST."
            )

        if left_value != -1:
            return left_value + 1
        
        if right_value != -1:
            return right_value + 1

        return -1

    def to_ascii(self, vertical_spacing: int = 0) -> str:
        """Return an ASCII rendering of the subtree rooted at this node."""
        from .bst_ascii_renderer import render_bst_ascii

        return render_bst_ascii(self, vertical_spacing=vertical_spacing)
