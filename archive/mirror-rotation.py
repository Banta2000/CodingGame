from typing import Any, Tuple, List
from cgutils import Board, Point2D
from typing import Union
from dataclasses import dataclass, field
from typing import Any, List, Optional
from enum import Enum


class Direction(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


# Map directions to Point2D deltas (row, col)
DIR_TO_VEC: dict[Direction, Point2D] = {
    Direction.N: Point2D(-1, 0),
    Direction.E: Point2D(0, 1),
    Direction.S: Point2D(1, 0),
    Direction.W: Point2D(0, -1),
}

SAMPLES: dict = {
    "data2": [[r"/\.T", r"....", r"....", r".\./", r"\..L"], "N"],
    "data6": [
        [
            r"/../###",
            r"..././#",
            r"......#",
            r"...L./#",
            r".....##",
            r"./././/",
            r"...T./#",
            r".....//",
            r"./.../.",
            r"/./####",
        ],
        "E",
    ],
}


@dataclass
class Node:
    id: Point2D
    val: Any
    neighbors: List[Point2D]


def get_start_parameters(start_data: Union[str, None] = None):
    if start_data and start_data in SAMPLES:
        data, initial_dir_token = SAMPLES[start_data]
    else:
        l, w = [int(i) for i in input().split()]
        data = [input() for _ in range(w)]
        initial_dir_token = input()

    board = Board()
    board.load_data(data)
    # Convert direction token to Direction enum
    try:
        initial_dir = Direction(initial_dir_token)
    except ValueError as exc:
        raise ValueError(f"Invalid initial direction: {initial_dir_token}") from exc
    return board, initial_dir


def complete_node(
    node: Node,
    board: Board,
    graph: dict[Tuple[int, int], Node],
    start_node: bool,
    initial_dir: Direction | None = None,
):
    def _find_next_node_in_direction(start: Point2D, delta: Point2D) -> Optional[Point2D]:
        p = start + delta
        while p in board.board:
            if board.board[p] == "#":
                return None
            if board.board[p] in ["\\", "/", "T"]:
                return p
            p += delta
        return None

    directions: List[Point2D] = []
    if start_node:
        if initial_dir is None:
            directions = []
        else:
            directions = [DIR_TO_VEC[initial_dir]]
    else:
        # Explore in fixed order: E, S, W, N (matches previous logic)
        directions = [
            DIR_TO_VEC[Direction.E],
            DIR_TO_VEC[Direction.S],
            DIR_TO_VEC[Direction.W],
            DIR_TO_VEC[Direction.N],
        ]
    neighbours = [_find_next_node_in_direction(node.id, p) for p in directions]
    neighbours = [x for x in neighbours if x != None]
    node.neighbors = neighbours


def build_graph(board: Board, initial_dir: Direction) -> dict[Point2D, Node]:
    graph = {}
    node_pos = board.find("\\") + board.find("/") + board.find("T") + board.find("L")
    start_node = board.find("L")[0]
    for pos in node_pos:
        graph[pos] = Node(id=pos, val=board[pos], neighbors=[])
    for node in graph.values():
        if node.id == start_node:
            complete_node(node, board, graph, start_node=True, initial_dir=initial_dir)
        else:
            complete_node(node, board, graph, start_node=False, initial_dir=None)
    return graph


def find_all_paths(
    board: Board,
    graph: dict[Point2D, Node],
    curr_pos: Point2D,
    target_pos: Point2D,
    visited: Optional[List[Point2D]] = None,
):
    result = []
    if visited == None:
        visited = []

    if curr_pos == target_pos:
        return [visited]

    if len(visited) >= 2:
        previous = visited[-2]
    else:
        previous = Point2D(-99, -99)

    curr = graph[curr_pos]
    for n_pos in curr.neighbors:
        if n_pos not in visited:
            # The three points cannot be in a row or col
            if previous.row != n_pos.row and previous.col != n_pos.col:
                result += find_all_paths(board, graph, n_pos, target_pos, visited + [n_pos])
    return result


def convert_path_to_slashes(path: List[Point2D]) -> List[str]:
    """Convert a path of points to a list of strings with slashes."""
    result = []
    for i in range(1, len(path) - 1):
        a = path[i - 1]
        b = path[i + 1]
        delta = b - a
        if delta.row < 0 and delta.col < 0:
            result.append("\\")
        elif delta.row < 0 and delta.col > 0:
            result.append("/")
        elif delta.row > 0 and delta.col < 0:
            result.append("/")
        elif delta.row > 0 and delta.col > 0:
            result.append("\\")
    return result


def find_flips_for_path(path: List[Point2D], board):
    node_positions = path[1:-1]
    real_path = [board.board[pos] for pos in node_positions]
    flipped_path = convert_path_to_slashes(path)
    result = []
    for i in range(len(node_positions)):
        if real_path[i] != flipped_path[i]:
            result.append(node_positions[i])
    result.sort(key=lambda p: (p.row, p.col))
    return result


# ********************************************************

board, initial_dir = get_start_parameters("data6")
# board.print()
graph = build_graph(board, initial_dir)
start = board.find("L")[0]
target = board.find("T")[0]
all_paths = find_all_paths(board, graph, start, target, [start])

result_flips_per_path = []
for path in all_paths:
    result_flips_per_path.append(find_flips_for_path(path, board))

result_flips_per_path.sort(key=lambda x: len(x))
final_result = result_flips_per_path[0]
for pos in final_result:
    print(pos.col, pos.row)
