import sys
import os
from typing import Any, Tuple
import itertools
from collections import defaultdict


HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_input() -> dict[str, Any]:
    GS = {}
    if HOME_PC:
        GS["x"] = 3  # each digit goes up to
        GS["n"] = 2  # length of the number
    else:
        GS["x"] = int(input())
        GS["n"] = int(input())
        for k, v in GS.items():
            myPrint(f"{k} = {v}")
    return GS


def number_generator(n: int, x: int):
    for digits in itertools.product(range(x), repeat=n):
        yield "".join(map(str, digits))


def build_graph(GS: dict[str, Any]) -> dict:
    n = GS["n"]
    x = GS["x"]
    graph = defaultdict(list)

    for number in number_generator(n, x):
        prefix = number[1:]
        graph[number] = [prefix + str(i) for i in range(x)]

    return graph


def dfs(graph: dict, start: str = "", visited: list = None) -> bool:
    if visited is None:
        visited = []

    if start == "":
        start = list(graph.keys())[0]

    if start in visited:
        return False

    visited.append(start)

    # if answer == "":
    #     updated_answer = start
    # else:
    #     updated_answer = answer + start[-1]

    if len(visited) == len(graph):
        print_result(visited)
        return True

    for neighbor in graph[start]:
        if dfs(graph, neighbor, visited):
            return True

    visited.pop()
    return False


def print_result(path: list) -> None:
    answer = path.pop(0)
    for node in path:
        answer += node[-1]
    print(answer)


# ********************************************************

GS = get_input()
graph = build_graph(GS)

dfs(graph)
