import sys
import os
from typing import Any, Tuple, List, Dict
import math


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Convert degrees to radians
def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180


# Get Start Parameters
def get_start_parameters(
    print_input: bool = False,
) -> Tuple[str, str, Dict[str, Dict[str, Any]], Dict[str, List[Tuple[str, float]]]]:
    if HOME_PC:
        start_code = "EINS"
        end_code = "GALH"
        locations = {
            "ABDU": {
                "name": "Abel Durand",
                "lat": degrees_to_radians(47.22019661),
                "lon": degrees_to_radians(-1.60337553),
            },
            "ABLA": {
                "name": "Avenue Blanche",
                "lat": degrees_to_radians(47.22973509),
                "lon": degrees_to_radians(-1.5893799),
            },
            "ACHA": {
                "name": "Angle Chaillou",
                "lat": degrees_to_radians(47.26979248),
                "lon": degrees_to_radians(-1.57206627),
            },
        }
        graph = {
            "ABDU": [("ABLA", 20288.99962910568)],
            "ABLA": [("ABDU", 20288.99962910568), ("ACHA", 20063.083601138624)],
            "ACHA": [("ABLA", 20063.083601138624)],
        }
    else:
        start_code = input()[9:]
        end_code = input()[9:]
        locations = {}
        n = int(input())
        for _ in range(n):
            code, name, _, lat, lon, _, _, _, _ = input()[9:].split(",")
            name = name[1:-1]
            locations[code] = {
                "name": name,
                "lat": degrees_to_radians(float(lat)),
                "lon": degrees_to_radians(float(lon)),
            }
        m = int(input())
        graph = {}
        for i in range(m):
            route = input()
            loc_a_code, loc_b_code = route.replace("StopArea:", "").split(" ")
            loc_a = locations[loc_a_code]
            loc_b = locations[loc_b_code]
            x = (loc_b["lon"] - loc_a["lon"]) * math.cos((loc_a["lat"] + loc_b["lat"]) / 2)
            y = loc_b["lat"] - loc_a["lat"]
            d = math.sqrt(x * x + y * y) * 6371
            graph[loc_a_code] = graph.get(loc_a_code, []) + [(loc_b_code, d)]

    if print_input:
        myPrint(f"{start_code=}")
        myPrint(f"{end_code=}")
        for k, v in locations.items():
            myPrint(f"{k=}, {v=}")

    return start_code, end_code, locations, graph


# Dijkstra's algorithm to find the shortest path from start to end using the distances graph
def find_shortest_path(
    start_code: str, end_code: str, locations: Dict[str, Dict[str, Any]], graph: Dict[str, List[Tuple[str, float]]]
) -> List[str]:
    visited = set()
    distances = {start_code: 0}
    previous = {start_code: None}
    current = start_code

    while current != end_code:
        visited.add(current)
        for neighbor, distance in graph[current]:
            if neighbor not in visited:
                new_distance = distances[current] + distance
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
        unvisited = [code for code in distances if code not in visited]
        if not unvisited:
            return []
        current = min(unvisited, key=distances.get)

    path = []
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path


# ********************************************************

HOME_PC: bool = True
start_code, end_code, locations, graph = get_start_parameters(print_input=False)
path = find_shortest_path(start_code, end_code, locations, graph)
if path:
    for loc in path:
        print(locations[loc]["name"])
else:
    print("IMPOSSIBLE")
