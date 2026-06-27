# https://www.codingame.com/ide/puzzle/paper-labyrinth
import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_input() -> dict[str, Any]:
    GS = {}
    if HOME_PC:
        GS["s"] = (0, 6)
        GS["r"] = (5, 0)
        GS["w"], GS["h"] = 7, 7
        GS["map"] = ["7654cde", "abbc52a", "292450c", "2f24a0e", "bdc17bf", "382267d", "bd99139"]

        # GS["s"] = (0, 0)
        # GS["r"] = (5, 0)
        # GS["w"] = 6
        # GS["h"] = 1
        # GS["map"] = ["75555d"]

    else:
        GS["s"] = tuple([int(i) for i in input().split()])
        GS["r"] = tuple([int(i) for i in input().split()])
        GS["w"], GS["h"] = [int(i) for i in input().split()]
        data = []
        for i in range(GS["h"]):
            data.append(input())
        GS["map"] = data

    GS["s"] = (GS["s"][1], GS["s"][0])
    GS["r"] = (GS["r"][1], GS["r"][0])
    return GS


def decode_number(n: str) -> list[int]:
    lookup = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "a": 10,
        "b": 11,
        "c": 12,
        "d": 13,
        "e": 14,
        "f": 15,
    }
    n = lookup[n]
    return [int(i) for i in bin(n)[2:].zfill(4)]


def recompute_map(GS: dict[str, Any]) -> None:
    new_map = {}
    for r, line in enumerate(GS["map"]):
        for c, char in enumerate(line):
            this_cell_pos = (r, c)
            new_map[this_cell_pos] = []
            walls = decode_number(char)
            # [Right, Top, Left, Down]
            neighbour_pos_list = [(r, c + 1), (r - 1, c), (r, c - 1), (r + 1, c)]
            for wall, neighbour_pos in zip(walls, neighbour_pos_list):
                if not wall:
                    new_map[this_cell_pos].append(neighbour_pos)
    GS["map"] = new_map


def bfs(graph: dict[Tuple[int, int], list[Tuple[int, int]]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    visited = set()
    queue = [(start, 0)]
    while queue:
        current, distance = queue.pop(0)
        if current == end:
            return distance
        if current in visited:
            continue
        visited.add(current)
        for neighbour in graph[current]:
            if neighbour not in visited:
                queue.append((neighbour, distance + 1))
    return -1


# ********************************************************

GS = get_input()
recompute_map(GS)

# for k, v in GS.items():
# myPrint(f"{k}: {v}")

way_1 = bfs(GS["map"], GS["s"], GS["r"])
way_2 = bfs(GS["map"], GS["r"], GS["s"])
print(way_1, way_2)
