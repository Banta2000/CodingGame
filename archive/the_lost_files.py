import sys
import os
from typing import Any, Tuple
from collections import deque

Graph = dict[int, list[int]]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters() -> Graph:
    def _create_graph(links: list[tuple[int, int]]) -> dict[int, list[int]]:
        graph = {}
        for n_1, n_2 in links:
            if n_1 not in graph:
                graph[n_1] = set()
            if n_2 not in graph:
                graph[n_2] = set()
            graph[n_1].add(n_2)
            graph[n_2].add(n_1)
        return graph

    if HOME_PC:
        links = [
            (4, 10),
            (7, 2),
            (2, 1),
            (4, 1),
            (8, 10),
            (3, 9),
            (6, 3),
            (8, 0),
            (7, 4),
            (5, 10),
            (9, 6),
            (7, 0),
            (8, 5),
        ]

        links = [
            (15, 39),
            (4, 73),
            (29, 41),
            (84, 50),
            (52, 79),
            (29, 59),
            (51, 34),
            (71, 58),
            (11, 71),
            (75, 83),
            (15, 7),
            (33, 22),
            (7, 21),
            (34, 5),
            (44, 40),
            (9, 3),
            (5, 23),
            (84, 45),
            (38, 2),
            (36, 41),
            (35, 21),
            (17, 9),
            (77, 78),
            (85, 70),
            (61, 79),
            (60, 25),
            (24, 14),
            (28, 39),
            (65, 33),
            (56, 64),
            (73, 80),
            (48, 26),
            (37, 69),
            (4, 11),
            (80, 76),
            (44, 1),
            (32, 66),
            (61, 44),
            (82, 12),
            (30, 38),
            (85, 1),
            (20, 30),
            (32, 13),
            (19, 22),
            (16, 69),
            (74, 31),
            (17, 61),
            (67, 10),
            (51, 74),
            (67, 46),
            (57, 8),
            (55, 53),
            (47, 49),
            (20, 62),
            (68, 26),
            (45, 6),
            (12, 3),
            (11, 47),
            (67, 85),
            (79, 59),
            (16, 55),
            (32, 72),
            (62, 6),
            (77, 52),
            (71, 18),
            (2, 37),
            (50, 53),
            (68, 46),
            (41, 68),
            (18, 54),
            (48, 0),
            (25, 78),
            (49, 72),
            (57, 30),
            (84, 14),
            (15, 24),
            (8, 76),
            (28, 24),
            (75, 20),
            (10, 82),
            (65, 27),
            (60, 40),
            (66, 35),
            (58, 70),
            (52, 63),
            (36, 85),
            (17, 81),
            (8, 23),
            (56, 42),
            (66, 83),
            (43, 81),
            (60, 42),
            (14, 54),
            (15, 19),
            (80, 63),
            (71, 27),
            (64, 85),
            (48, 43),
            (68, 0),
            (65, 13),
            (31, 54),
        ]

    else:
        e = int(input())
        links = []
        for _ in range(e):
            n_1, n_2 = [int(j) for j in input().split()]
            links.append((n_1, n_2))

    graph = _create_graph(links)
    return graph


# Returns number of continents in the graph
def find_continents(graph: Graph) -> int:
    # Returns list of subgraphs, each with a dictionary of nodes and their neighbors
    def _separate_graphs(graph: Graph) -> list[Graph]:
        def _find_nodes_in_grah_like_start_node(graph: Graph, start_node: int) -> set[int]:
            stack = [start_node]
            visited = set()
            while stack:
                node = stack.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            return visited

        result = []
        remaining_nodes = set(graph.keys())
        while remaining_nodes:
            start_node = remaining_nodes.pop()
            connected_nodes = _find_nodes_in_grah_like_start_node(graph, start_node)
            subgraph = {node: graph[node] for node in connected_nodes}
            result.append(subgraph)
            remaining_nodes -= connected_nodes

        return result

    return len(_separate_graphs(graph))


# Outputs graph in a way that can be visualized
def print_graph_edges(graph: Graph) -> None:
    edges = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if (node, neighbor) in edges or (neighbor, node) in edges:
                continue
            edges.add((node, neighbor))
    for node_1, node_2 in edges:
        myPrint(f"{node_1} {node_2}")
    myPrint()


def identify_triangles_peak(graph: Graph) -> list[tuple[int, int, int]]:
    result = []
    for node, neighbors in graph.items():
        if len(neighbors) == 2:
            neighbor_1, neighbor_2 = neighbors
            if neighbor_1 in graph[neighbor_2] and neighbor_2 in graph[neighbor_1]:
                print("Triangle Peak", node)


# Returns True if node is the peak of a triangle (2 neighbours that are connected)
def is_triangle_peak(graph: Graph, node: int) -> bool:
    neighbors = graph[node]
    if len(neighbors) == 2:
        neighbor_1, neighbor_2 = neighbors
        if neighbor_1 in graph[neighbor_2] and neighbor_2 in graph[neighbor_1]:
            return True
    return False


# Removes a single pass through
def clean_single_pass_through(graph: Graph, node):
    n1, n2 = graph[node]
    graph[n1].remove(node)
    graph[n2].remove(node)
    graph[n1].add(n2)
    graph[n2].add(n1)
    graph.pop(node)


# Removes all pass throughs are removed
def clean_all_pass_throughs(graph: Graph):
    if not graph:
        return

    while True:
        for node, neighbors in list(graph.items()):
            if len(neighbors) == 2 and not is_triangle_peak(graph, node):
                clean_single_pass_through(graph, node)
                myPrint("Pass through", node)
                break
        else:
            break


# Removes all triangles on edges, returns number of removed triangles
def clean_all_peripherial_triangles(graph: Graph) -> int:
    if not graph:
        return 0

    count_triangles = 0
    while True:
        for node, neighbours in list(graph.items()):
            if is_triangle_peak(graph, node) and len(neighbours) == 2:
                count_triangles += 1
                n1, n2 = neighbours
                clean_single_pass_through(graph, node)
                myPrint("Peripheral", node, n1, n2)
                break
        else:
            break
    return count_triangles


# Removes all triangles that can be collapsed
def clean_all_collapsable_triangles(graph: Graph) -> int:
    if not graph:
        return 0

    count_triangles = 0
    while find_collapsable_triangle(graph):
        triangle = find_collapsable_triangle(graph)
        collapse_polygon(graph, triangle)
        myPrint("Collapsed", triangle)
        count_triangles += 1

    return count_triangles


# Removes all loose ends
def clean_loose_ends(graph: Graph):
    if not graph:
        return 0

    while True:
        for node, neighbors in list(graph.items()):
            if len(neighbors) <= 1:
                graph.pop(node)
                if not neighbors:
                    break
                neighbour = list(neighbors)[0]
                graph[neighbour].remove(node)
                myPrint("Loose End", node)
                break
        else:
            break


def common_neighbours(graph: Graph, nodes: list) -> bool:
    all_neighbours = [neighbor for node in nodes for neighbor in graph[node]]
    all_neighbours = [x for x in all_neighbours if x not in nodes]
    # if len(all_neighbours) == len(set(all_neighbours)) then no common neighbours
    return not len(all_neighbours) == len(set(all_neighbours))


# Returns the nodes that are connected to each other but have no common neighbours
def find_collapsable_triangle(graph: Graph):
    for n1 in graph.keys():
        for n2 in graph[n1]:
            for n3 in graph[n2]:
                if n1 == n2 or n1 == n3 or n2 == n3:
                    continue

                # Check if all nodes are connected to each other
                c1 = n1 in graph[n2] and n1 in graph[n3]
                c2 = n2 in graph[n1] and n2 in graph[n3]
                c3 = n3 in graph[n1] and n3 in graph[n2]
                if not c1 or not c2 or not c3:
                    continue

                # Check if that no node shares common neighbours with the other nodes
                if common_neighbours(graph, [n1, n2, n3]):
                    continue

                return n1, n2, n3
    return None


# Returns the nodes that are connected to each other but have no common neighbours
def find_collapsable_square(graph: Graph):
    for n1 in graph.keys():
        for n2 in graph[n1]:
            for n3 in graph[n2]:
                for n4 in graph[n3]:
                    if n1 == n2 or n1 == n3 or n1 == n4 or n2 == n3 or n2 == n4 or n3 == n4:
                        continue
                    c1 = n1 in graph[n2] and n1 not in graph[n3] and n1 in graph[n4]
                    c2 = n2 in graph[n3] and n2 not in graph[n4] and n2 in graph[n1]
                    c3 = n3 in graph[n4] and n3 not in graph[n1] and n3 in graph[n2]
                    c4 = n4 in graph[n1] and n4 not in graph[n2] and n4 in graph[n3]
                    if not c1 or not c2 or not c3 or not c4:
                        continue

                    if common_neighbours(graph, [n1, n2, n3, n4]):
                        continue

                    return [n1, n2, n3, n4]
    return None


# Collapses a polygon into a single node
def collapse_polygon(graph: Graph, delete_nodes: list[int]):
    new_neighbours = set()
    for node in delete_nodes:
        new_neighbours = new_neighbours.union(graph[node])
        graph.pop(node)
    for node in delete_nodes:
        new_neighbours.remove(node)
    new_node = 1000 + len(graph)

    graph[new_node] = new_neighbours
    for neighbour in new_neighbours:
        for delete_node in delete_nodes:
            if delete_node in graph[neighbour]:
                graph[neighbour].remove(delete_node)
        graph[neighbour].add(new_node)


# Removes all squares that can be collapsed
def clean_all_collapsable_squares(graph: Graph) -> int:
    if not graph:
        return 0

    count_squares = 0
    while find_collapsable_square(graph):
        square = find_collapsable_square(graph)
        collapse_polygon(graph, square)
        count_squares += 1

    return count_squares


def find_and_remove_kite(graph: Graph):
    if not graph:
        return 0

    for n1 in graph.keys():
        for n2 in graph[n1]:
            for n3 in graph[n2]:
                for n4 in graph[n3]:
                    if n1 == n2 or n1 == n3 or n1 == n4 or n2 == n3 or n2 == n4 or n3 == n4:
                        continue
                    c1 = n1 in graph[n2] and n1 in graph[n3] and n1 in graph[n4]
                    c2 = n2 in graph[n1] and n2 in graph[n3]
                    c3 = n3 in graph[n1] and n3 in graph[n2] and n3 in graph[n4]
                    c4 = n4 in graph[n1] and n4 in graph[n3]
                    if not c1 or not c2 or not c3 or not c4:
                        continue

                    if len(graph[n1]) != 3:
                        continue

                    myPrint("Kite", n1, n2, n3, n4)
                    graph.pop(n1)
                    graph[n2].remove(n1)
                    graph[n3].remove(n1)
                    graph[n4].remove(n1)
                    return 2
    return 0


# ********************************************************

main_graph = get_start_parameters()
print_graph_edges(main_graph)
continents = find_continents(main_graph)

tiles_removed = 0
while main_graph:
    clean_all_pass_throughs(main_graph)
    tiles_removed += clean_all_peripherial_triangles(main_graph)
    tiles_removed += clean_all_collapsable_triangles(main_graph)
    tiles_removed += clean_all_collapsable_squares(main_graph)
    tiles_removed += find_and_remove_kite(main_graph)

    clean_loose_ends(main_graph)
    print_graph_edges(main_graph)
    True


print(continents, tiles_removed)


# ************************************************************
