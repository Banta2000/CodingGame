import sys
import os
from typing import Any, Tuple, Dict, Set
from collections import defaultdict

HOME_PC: bool = os.getenv("HOME_PC") == "true"
Game = Dict[int, Set[int]]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters() -> Game:
    if HOME_PC:
        npeople = 100
        links = [
            [10, 82],
            [33, 29],
            [83, 21],
            [17, 12],
            [28, 3],
            [33, 49],
            [86, 23],
            [2, 23],
            [60, 88],
            [57, 91],
            [79, 75],
            [20, 14],
            [90, 76],
            [83, 44],
            [1, 53],
            [0, 15],
            [57, 0],
            [36, 21],
            [84, 6],
            [86, 32],
            [66, 61],
            [33, 48],
            [17, 95],
            [20, 66],
            [76, 4],
            [28, 54],
            [95, 28],
            [96, 51],
            [96, 2],
            [24, 16],
            [61, 54],
            [82, 35],
            [40, 68],
            [21, 24],
            [76, 66],
            [34, 24],
            [0, 94],
            [87, 47],
            [78, 18],
            [18, 47],
            [84, 85],
            [91, 4],
            [4, 83],
            [89, 39],
            [8, 19],
            [35, 79],
            [60, 92],
            [53, 87],
            [22, 4],
            [57, 60],
        ]
    else:
        npeople = int(input())
        nlinks = int(input())
        links = [list(map(int, input().split())) for _ in range(nlinks)]

    graph = {x: set() for x in range(npeople)}
    for l1, l2 in links:
        graph[l1].add(l2)
        graph[l2].add(l1)
    return graph


# Returns all members of a cluster connected to start_node
def get_cluster_members(graph: Game, start_node: int) -> Set[int]:
    stack = [start_node]
    visited = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                stack.append(neighbour)
    return visited


graph = get_start_parameters()
result = defaultdict(int)
while graph:
    start_node = next(iter(graph))
    cluster_members = get_cluster_members(graph, start_node)
    result[len(cluster_members)] += 1
    for node in cluster_members:
        del graph[node]

sorted_result = sorted(result.items(), key=lambda x: x[0], reverse=True)
for cluster_size, cluster_count in sorted_result:
    print(cluster_size, cluster_count)
