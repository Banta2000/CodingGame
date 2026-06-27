HOME_PC = True

from blunderepisode2data import *
from typing import Any, Tuple, List
from dataclasses import dataclass
from collections import defaultdict
from collections import deque
from typing import Optional

Board = dict[int, Any]


@dataclass(frozen=True)
class Room:
    id: int
    value: int
    incoming: List[Any]
    outgoing: List[Any]


def get_start_parameters(start_data=None):
    def _parse(data):
        res: Board = {}
        reverse_lookup = defaultdict(list)

        for line in data:
            room_nr, money, door1, door2 = line.strip().split(" ")
            room_nr = int(room_nr)
            money = int(money)
            outgoing = [int(x) for x in (door1, door2) if x != "E"]
            res[room_nr] = Room(id=room_nr, value=money, incoming=[], outgoing=outgoing)
            for door in outgoing:
                reverse_lookup[door].append(room_nr)

        for room in res.values():
            for v in reverse_lookup[room.id]:
                if v != room.id:
                    room.incoming.append(v)
        return res

    if HOME_PC:
        if not isinstance(start_data, str):
            raise ValueError("start_data must be a string key for demo_data")
        data = demo_data[start_data]
    else:
        n = int(input())
        data = [input() for _ in range(n)]

    data = _parse(data)
    return data


def get_best_value_path(curr: int, visited: Optional[set] = None):
    global NUM_VISITED
    global TRIGGERED

    if visited is None:
        visited = {curr}
        NUM_VISITED = 0
        TRIGGERED = False

    NUM_VISITED += 1
    if NUM_VISITED > DEPTH_LIMIT:
        TRIGGERED = True
        return -1

    if len(BOARD[curr].outgoing) == 0:
        return sum([BOARD[n].value for n in visited])

    best_val = 0
    for n in BOARD[curr].outgoing:
        if n not in visited:
            visited.add(n)
            r = get_best_value_path(n, visited)
            best_val = max(best_val, r)
            visited.remove(n)
    return best_val


def identify_nodes_with_n_exits(board: Board, n: int) -> List[int]:
    # Returns a list of room ID's that have exactly n exits to -1
    res = []
    for room in board.values():
        if room.outgoing.count(-1) == n:
            res.append(room.id)
    return res


def get_next_exit_only_node(board: Board) -> int:
    # Returns the next exit only node, else return -1
    for room in board.values():
        if len(room.outgoing) == 0:
            return room.id
    return -1


def get_next_parent(board: Board) -> int:
    # Returns a node (parent) which is close to the border
    while True:
        exit_node = get_next_exit_only_node(board)
        if exit_node == -1:
            return -1
        if len(board[exit_node].incoming) > 0:
            return board[exit_node].incoming[0]


def find_cluster(board: Board, start: int):
    # Uses DFS to find all nodes connnected to the start node
    visited = set([start])
    stack = [start]
    while stack:
        curr = stack.pop()
        curr = board[curr]
        for n in curr.outgoing:
            if n not in visited:
                visited.add(n)
                stack.append(n)
    return visited


def pluck_node(board: Board, old_node_id: int):
    # Calculates the best value for the node; cuts the children; and replaces the node
    new_value = get_best_value_path(old_node_id)

    # If we managed to find correct value, continue, else return, node not ready for plucking
    if TRIGGERED:
        return

    old_parent_ids = BOARD[old_node_id].incoming

    # For each child, detach the parent
    for child in BOARD[old_node_id].outgoing:
        BOARD[child].incoming.remove(old_node_id)

    # Create a new node with the best value and the same parents but no children
    new_node = Room(id=old_node_id, value=new_value, incoming=old_parent_ids, outgoing=[])

    # Replace the old node in the board
    board[old_node_id] = new_node

    # print("Plucked", old_node_id)


def output_printable_formate(board: Board):
    # Converts the board to a printable format
    # for _, room in board.items():
    for i in range(60):
        room = board[i]
        for to_room in room.outgoing:
            print(f"{room.id} {to_room}")


def build_plucking_order(board: Board) -> list[int]:
    # Rerturns dict with the distance to the start for each node, uses BFS
    distance_to_start = {}
    queue = deque([(0, 0)])  # (room_id, distance)
    visited = set([0])

    while queue:
        room_id, distance = queue.popleft()
        distance_to_start[room_id] = distance
        for neighbor in board[room_id].outgoing:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
                visited.add(neighbor)

    rooms = list(distance_to_start.keys())
    plucking_order = sorted(rooms, key=lambda x: distance_to_start[x], reverse=True)
    return plucking_order


# ********************************************************

NUM_VISITED = 0
DEPTH_LIMIT = 100
TRIGGERED = False
BOARD = get_start_parameters("data3")
# output_printable_formate(BOARD)

for _ in range(50):
    PLUCKING_ORDER = build_plucking_order(BOARD)
    for node in PLUCKING_ORDER:
        pluck_node(BOARD, node)

PLUCKING_ORDER = build_plucking_order(BOARD)

print(BOARD[0].value)

# output_printable_formate(BOARD)

# print(BOARD[0].value)
