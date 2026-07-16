from collections import deque
from typing import Tuple
from cgutils.point_utils import Point
from cgutils.coding_game_helper import CodingGameHelper

PointSet = set[Point]
Link = Tuple[Point, Point]
LinkSet = set[Link]
ORIGIN = Point(0, 0)
DIR_TO_DELTA = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}
DELTA_TO_DIR = {delta: direction for direction, delta in DIR_TO_DELTA.items()}


def read_input() -> str:
    line = CGH.input()
    return line


def print_board(visited: set[Point]):
    min_row = min(p.row for p in visited) - 2
    max_row = max(p.row for p in visited) + 2
    min_col = min(p.col for p in visited) - 2
    max_col = max(p.col for p in visited) + 2

    for r in range(min_row, max_row + 1):
        row_str = ""
        for c in range(min_col, max_col + 1):
            if Point(r, c) in visited:
                row_str += "X"
            else:
                row_str += "."
        print(row_str)


def canonical_link(p1: Point, p2: Point) -> Tuple[Point, Point]:
    """Return a canonical representation of the link between two points."""
    if p1.row < p2.row or (p1.row == p2.row and p1.col < p2.col):
        return (p1, p2)
    else:
        return (p2, p1)


def trace_route(line: str) -> Tuple[PointSet, LinkSet, Point]:
    visited_points = set()
    visited_links = set()

    p1 = ORIGIN
    p2 = ORIGIN

    visited_points.add(p1)
    for s in line:
        dr, dc = DIR_TO_DELTA[s]
        p2 = Point(p1.row + dr, p1.col + dc)
        visited_points.add(p2)
        visited_links.add(canonical_link(p1, p2))
        p1 = p2
    return visited_points, visited_links, p2


def get_neighbors(p: Point) -> list[Point]:
    return [Point(p.row + dr, p.col + dc) for dr, dc in DIR_TO_DELTA.values()]


def shortest_path_length_to_origin(start: Point, blocked_links: LinkSet) -> Tuple[int, dict[Point, Point | None]]:
    queue = deque([start])
    reverse_lookup: dict[Point, Point | None] = {}
    p1 = start
    reverse_lookup[p1] = None
    while queue:
        p1 = queue.popleft()
        options = get_neighbors(p1)

        if p1 == ORIGIN:
            break

        for p2 in options:
            l = canonical_link(p1, p2)
            if l not in blocked_links and p2 not in reverse_lookup:
                queue.append(p2)
                reverse_lookup[p2] = p1

    path = []
    curr = ORIGIN
    while curr in reverse_lookup:
        path.append(curr)
        curr = reverse_lookup[curr]

    return len(path) - 1, reverse_lookup


def collect_paths_of_fixed_length(
    p1: Point,
    path: list[Point],
    remaining_steps: int,
    blocked_links: LinkSet,
    solutions: list[list[Point]],
) -> None:
    options = get_neighbors(p1)

    if remaining_steps == 0 and p1 == ORIGIN:
        solutions.append(path)
        return

    if remaining_steps == 0:
        return

    for p2 in options:
        if p2 in path:
            continue

        l = canonical_link(p1, p2)
        if l in blocked_links:
            continue

        collect_paths_of_fixed_length(
            p2,
            path + [p2],
            remaining_steps - 1,
            blocked_links,
            solutions,
        )


def get_direction_between_points(p1: Point, p2: Point) -> str:
    delta = (p2.row - p1.row, p2.col - p1.col)
    return DELTA_TO_DIR.get(delta, "")


def path_as_string(path: list[Point]) -> str:
    res = ""
    for i in range(len(path) - 1):
        p1, p2 = path[i], path[i + 1]
        res += get_direction_between_points(p1, p2)
    return res


# ********************************************************

CGH = CodingGameHelper(13, __file__)
line = read_input()
visited_points, visited_links, end_point = trace_route(line)

valid_solutions: list[list[Point]] = []

# print_board(visited_points)

path_length, _reverse_lookup = shortest_path_length_to_origin(end_point, visited_links)

collect_paths_of_fixed_length(
    end_point,
    [end_point],
    path_length,
    visited_links,
    valid_solutions,
)

end_sol = [path_as_string(sol) for sol in valid_solutions]
end_sol = sorted(end_sol)
for line in end_sol:
    CGH.print(line)
CGH.assert_output()
