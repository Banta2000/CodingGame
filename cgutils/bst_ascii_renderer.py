from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bstnode import BSTNode


Layout = dict["BSTNode", tuple[int, int]]
Canvas = list[list[str]]


def collect_nodes(root: "BSTNode") -> list["BSTNode"]:
    """Return all nodes in the subtree rooted at root."""
    nodes = []

    def visit(node: "BSTNode | None") -> None:
        if node is None:
            return

        nodes.append(node)
        visit(node.left)
        visit(node.right)

    visit(root)
    return nodes


def build_layout(root: "BSTNode") -> Layout:
    """Return the display row and column for each node."""
    layout: Layout = {}
    next_col = 0

    def visit(node: "BSTNode | None", depth: int) -> None:
        nonlocal next_col
        if node is None:
            return

        visit(node.left, depth + 1)
        layout[node] = (depth, next_col)
        next_col += 1
        visit(node.right, depth + 1)

    visit(root, 0)
    return layout


def get_level_height(vertical_spacing: int) -> int:
    """Return the number of canvas rows used per tree level."""
    return vertical_spacing * 2 + 2


def get_node_y(depth: int, vertical_spacing: int) -> int:
    """Return the canvas row for a node at the given depth."""
    return depth * get_level_height(vertical_spacing)


def get_node_x(col: int, cell_width: int) -> int:
    """Return the anchor column for a node at the given layout column."""
    return col * cell_width + cell_width - 1


def create_canvas(width: int, height: int) -> Canvas:
    """Return an empty character canvas."""
    return [[" " for _ in range(width)] for _ in range(height)]


def draw_label(canvas: Canvas, text: str, y: int, anchor_x: int) -> None:
    """Draw a right-aligned node label ending at anchor_x."""
    start_x = anchor_x - len(text) + 1
    for idx, char in enumerate(text):
        canvas[y][start_x + idx] = char


def draw_edge(
    canvas: Canvas,
    parent: "BSTNode",
    child: "BSTNode",
    layout: Layout,
    cell_width: int,
    vertical_spacing: int,
) -> None:
    """Draw one parent-child connector."""
    parent_depth, parent_col = layout[parent]
    child_depth, child_col = layout[child]
    parent_x = get_node_x(parent_col, cell_width)
    child_x = get_node_x(child_col, cell_width)
    parent_y = get_node_y(parent_depth, vertical_spacing)
    child_y = get_node_y(child_depth, vertical_spacing)
    connector_y = parent_y + vertical_spacing + 1

    for y in range(parent_y + 1, connector_y):
        canvas[y][parent_x] = "|"

    for x in range(min(parent_x, child_x), max(parent_x, child_x) + 1):
        canvas[connector_y][x] = "-"
    canvas[connector_y][parent_x] = "+"
    canvas[connector_y][child_x] = "+"

    for y in range(connector_y + 1, child_y):
        canvas[y][child_x] = "|"


def canvas_to_text(canvas: Canvas) -> str:
    """Convert the character canvas into printable lines."""
    return "\n".join("".join(row).rstrip() for row in canvas)


def render_bst_ascii(root: "BSTNode", vertical_spacing: int = 0) -> str:
    """Return an ASCII rendering of the subtree rooted at root."""
    if vertical_spacing < 0:
        raise ValueError("vertical_spacing must be non-negative")

    nodes = collect_nodes(root)
    layout = build_layout(root)
    max_depth = max(row for row, _ in layout.values())
    max_col = max(col for _, col in layout.values())
    cell_width = max(len(str(node.value)) for node in nodes) + 1
    canvas_width = (max_col + 1) * cell_width
    canvas_height = get_node_y(max_depth, vertical_spacing) + 1
    canvas = create_canvas(canvas_width, canvas_height)

    for node in nodes:
        row, col = layout[node]
        draw_label(canvas, str(node.value), get_node_y(row, vertical_spacing), get_node_x(col, cell_width))

    for node in nodes:
        if node.left is not None:
            draw_edge(canvas, node, node.left, layout, cell_width, vertical_spacing)
        if node.right is not None:
            draw_edge(canvas, node, node.right, layout, cell_width, vertical_spacing)

    return canvas_to_text(canvas)
