import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_start_parameters() -> Game:
    if HOME_PC:
        nodes = {
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
        }
        gateways = [0, 18, 28]
        graph = [
            (28, 36),
            (0, 2),
            (3, 34),
            (29, 21),
            (37, 35),
            (28, 32),
            (0, 10),
            (37, 2),
            (4, 5),
            (13, 14),
            (34, 35),
            (27, 19),
            (28, 34),
            (30, 31),
            (18, 26),
            (0, 9),
            (7, 8),
            (18, 24),
            (18, 23),
            (0, 5),
            (16, 17),
            (29, 30),
            (10, 11),
            (0, 12),
            (15, 16),
            (0, 11),
            (0, 17),
            (18, 22),
            (23, 24),
            (0, 7),
            (35, 23),
            (22, 23),
            (1, 2),
            (0, 13),
            (18, 27),
            (25, 26),
            (32, 33),
            (28, 31),
            (24, 25),
            (28, 35),
            (21, 22),
            (4, 33),
            (28, 29),
            (36, 22),
            (18, 25),
            (37, 23),
            (18, 21),
            (5, 6),
            (19, 20),
            (0, 14),
            (35, 36),
            (9, 10),
            (0, 6),
            (20, 21),
            (0, 3),
            (33, 34),
            (14, 15),
            (28, 33),
            (11, 12),
            (12, 13),
            (17, 1),
            (18, 19),
            (36, 29),
            (0, 4),
            (0, 15),
            (0, 1),
            (18, 20),
            (2, 3),
            (0, 16),
            (8, 9),
            (0, 8),
            (26, 27),
            (28, 30),
            (3, 4),
            (31, 32),
            (6, 7),
            (37, 1),
            (37, 24),
            (35, 2),
        ]

    else:
        # n: number of nodes, including the gateways
        # l: number of links
        # e: number of exit gateways
        n, l, e = [int(i) for i in input().split()]
        graph = []
        for i in range(l):
            # n1: N1 and N2 defines a link between these nodes
            n1, n2 = [int(j) for j in input().split()]
            graph.append((n1, n2))

        nodes = set()
        for n1, n2 in graph:
            nodes.add(n1)
            nodes.add(n2)

        gateways = []
        for i in range(e):
            ei = int(input())  # the index of a gateway node
            gateways.append(ei)

    G = {"nodes": nodes, "gateways": gateways, "graph": graph}
    return G


# Return list of neighbour nodes of a node [2, 3, 4]
def get_neighbours(graph: list[int, int], node: int) -> list[int]:
    neighbours = []
    for n1, n2 in graph:
        if n1 == node:
            neighbours.append(n2)
        elif n2 == node:
            neighbours.append(n1)
    return neighbours


# Returns list of paths [start_node, 4, 2, ..., end_node] that are all shortest lengths
def find_all_shortest_paths(G: Game, start_node: int, end_node: int) -> None:
    graph = G["graph"]
    path = [start_node]
    stack = [path]
    solution_found = False
    result_collection = []
    while stack:
        path = stack.pop(0)
        curr = path[-1]
        if solution_found and len(path) > len(result_collection[0]):
            break
        if len(path) > 20:
            break
        if curr == end_node:
            solution_found = True
            result_collection.append(path)
        for neighbour in get_neighbours(graph, curr):
            if neighbour in path:
                continue
            new_path = list(path)
            new_path.append(neighbour)
            stack.append(new_path)
    return result_collection


# Examines all paths for the most common link and returns it (2, 3)
def choose_link_to_delete(list_of_shortest_paths: list[int, int]):
    links_list = []
    for path in list_of_shortest_paths:
        # Convert pah = list of nodes into list of links
        links = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        links_list.extend(links)
    most_common_link = max(set(links_list), key=links_list.count)
    return most_common_link


# Only keep the shortest paths in the list
def clean_list_of_shortest_paths(list_of_shortest_paths: list[list[int]]) -> list[list[int]]:
    # Sort the list by length of paths
    list_of_shortest_paths.sort(key=len)
    shortest_length = len(list_of_shortest_paths[0])
    list_of_shortest_paths = [path for path in list_of_shortest_paths if len(path) == shortest_length]
    return list_of_shortest_paths


# Check both directions of the link and delete the link from the graph
def delete_link_from_graph(G: Game, link: Tuple[int, int]) -> None:
    if link in G["graph"]:
        G["graph"].remove(link)
    else:
        G["graph"].remove((link[1], link[0]))


# Returns list of gateways that are still in the graph
def get_updated_list_of_gateways(G: Game) -> list[int]:
    result = []
    for gateway in G["gateways"]:
        # Find if the gateway still has links connected to it
        links_connecting_to_gateway = [link for link in G["graph"] if gateway in link]
        if links_connecting_to_gateway:
            result.append(gateway)
    return result


# ********************************************************

G = get_start_parameters()

links_to_delete = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (35, 37),
    (28, 35),
    (28, 34),
    (28, 33),
    (28, 32),
    (28, 31),
    (28, 30),
    (28, 29),
    (28, 36),
    (18, 23),
    (18, 22),
    (18, 21),
]
# for x in links_to_delete:
    # delete_link_from_graph(G, x)


while True:
    # bot_position = int(input())
    bot_position = 29
    myPrint("Bot Position", bot_position)

    list_of_shortest_paths = []
    gateways = get_updated_list_of_gateways(G)

    for end_point in gateways:
        list_of_shortest_paths.extend(find_all_shortest_paths(G, bot_position, end_point))
    myPrint("Before cleaning", list_of_shortest_paths)
    list_of_shortest_paths = clean_list_of_shortest_paths(list_of_shortest_paths)

    myPrint("Shortest paths")
    for line in list_of_shortest_paths:
        myPrint(line)

    link_to_delete = choose_link_to_delete(list_of_shortest_paths)

    delete_link_from_graph(G, link_to_delete)
    print(link_to_delete[0], link_to_delete[1])
