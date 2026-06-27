import os
from typing import Any, Tuple, List
from cgutils import Board, Point2D
from cgutils.coding_game_helper import CodingGameHelper


def read_input(CGH: CodingGameHelper) -> Tuple[int, int, list[str]]:
    num_nodes = int(CGH.input())
    virus_location = int(CGH.input())
    num_links = int(CGH.input())
    links_lines = [CGH.input() for _ in range(num_links)]
    return virus_location, num_nodes, links_lines


def parse(links: list[str]) -> dict[int, list[int]]:
    res = dict()
    for line in links:
        a, b = [int(x) for x in line.split(" ")]
        if a not in res:
            res[a] = []
        if b not in res:
            res[b] = []
        res[a].append(b)
        res[b].append(a)
    return res


def bfs(grap: dict, curr: int, exclude: int) -> int:
    if curr == exclude:
        return 100000000000
    stack = [curr]
    visited = set()
    while stack:
        curr = stack.pop(0)
        for neighbor in graph[curr]:
            if neighbor == exclude or neighbor in visited:
                continue
            visited.add(neighbor)
            stack.append(neighbor)
    return len(visited)


# ********************************************************

for case_nr in range(1, 5):
    CGH = CodingGameHelper(case_nr, __file__)
    virus_location, num_nodes, links_lines = read_input(CGH)
    graph = parse(links_lines)
    min_infected = num_nodes
    response = None
    for exclude_node in range(num_nodes):
        res = bfs(graph, virus_location, exclude_node)
        if res < min_infected:
            min_infected = res
            response = exclude_node
    CGH.add_output_line(response)
    CGH.assert_output()
