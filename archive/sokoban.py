import os
from typing import Any, Optional, Tuple, List, TypeAlias
from collections import deque


Point: TypeAlias = Tuple[int, int]
Board: TypeAlias = dict[Point, Any]
GameState: TypeAlias = Tuple[Point, ...]


class Game:
    def __init__(self, room_lines: list[str]):
        self.room_lines = room_lines
        self.board, self.end_state = self._parse_board(room_lines)
        self.box_count = len(self.end_state)
        self.corners = self.get_corners()
        self.numRows = max(p[0] for p in self.board) + 1
        self.numCols = max(p[1] for p in self.board) + 1

    # Parse the board lines and return a dict of (row, col) -> char and a set of end states
    def _parse_board(self, room_lines: list[str]):
        board = {}
        end_states = set()
        for r, line in enumerate(room_lines):
            for c, char in enumerate(line):
                p = (r, c)
                board[p] = char
                if char == "*":
                    end_states.add(p)
        return board, end_states

    def print(self, state: GameState):
        player, *boxes_list = state
        boxes = set(boxes_list)
        RESET = "\x1b[0m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        for r in range(self.numRows):
            for c in range(self.numCols):
                p = (r, c)
                char = self.board[(r, c)]
                if p == player:
                    char = f"{GREEN}P{RESET}"
                elif p in boxes:
                    char = f"{RED}B{RESET}"
                elif char == "#":
                    char = f"{BLUE}{char}{RESET}"
                print(char, end="")
            print()
        print()

    # Returns the set of corners of the board that are blocked by walls and where boxes can get stuck
    def get_corners(self):
        board = self.board
        result = set()
        for p, val in self.board.items():
            r, c = p
            u, d, l, r = (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)
            c1 = u in board and l in board and board[u] == "#" and board[l] == "#"
            c2 = u in board and r in board and board[u] == "#" and board[r] == "#"
            c3 = d in board and l in board and board[d] == "#" and board[l] == "#"
            c4 = d in board and r in board and board[d] == "#" and board[r] == "#"
            if val != "." and (c1 or c2 or c3 or c4):
                result.add(p)
        return result

    # Checks if the current gamestate is final
    def is_finale(self, state: GameState) -> bool:
        return set(state[1:]) == self.end_state


def load_gameconfig(nr: int) -> list[str]:
    room = []
    if nr == 0:
        width, height, box_count = [int(i) for i in input().split()]
        room = [input() for _ in range(height)]
    elif nr == 1:
        room = ["..####", "..#..#", "###.*#", "#..*.#", "#.#..#", "#..*.#", "##...#", ".#####"]
    elif nr == 2:
        room = ["######.", "#....#.", "#.#*.##", "#.....#", "###**.#", "..#...#", "..#####"]
    elif nr == 3:
        room = [
            "..####..",
            "..#..#..",
            ".##..#..",
            "##.*.###",
            "#..*.*.#",
            "#..*...#",
            "##.#.###",
            ".#...#..",
            ".#####..",
        ]
    return room


# Load the gamestate from file or from web
def load_gamestate(game: Game, nr: int) -> GameState:
    player: Point = (0, 0)
    boxes: list[Point] = []
    if nr == 0:
        x, y = [int(i) for i in input().split()]
        player = (y, x)
        for i in range(game.box_count):
            box_x, box_y = [int(j) for j in input().split()]
            boxes.append((box_y, box_x))
    elif nr == 1:
        # player = (4, 3)
        player = (4, 3)
        boxes = [(3, 3), (5, 2), (5, 3)]
    elif nr == 2:
        player = (4, 4)
        boxes = [(3, 3), (3, 4), (4, 3)]
    elif nr == 3:
        player = (6, 4)
        boxes = [(4, 2), (4, 4), (5, 3), (5, 5)]
    return (player, *sorted(boxes))


# Returns ["U", "D", "L", "R"] depending on the possible moves
def get_move_options(game: Game, state: GameState):
    board = game.board
    player, *boxes_list = state
    boxes = set(boxes_list)
    r, c = player
    options = [
        [(r - 1, c), (r - 2, c), "U"],
        [(r + 1, c), (r + 2, c), "D"],
        [(r, c - 1), (r, c - 2), "L"],
        [(r, c + 1), (r, c + 2), "R"],
    ]

    result = []
    for n1, n2, direction in options:
        # Check that the target pos is inside the room
        if n1 not in board or board[n1] == "#":
            continue

        # If the target pos is empty
        if n1 not in boxes:
            result.append(direction)
            continue

        # If there is a box
        if n1 in boxes and n2 in board and board[n2] != "#" and n2 not in boxes:
            result.append(direction)
            continue

    return result


# Returns the new game state based on the move ("U") and the current gamestate
def compute_new_end_state(game: Game, state: GameState, move: str) -> GameState:
    board = game.board
    player, *boxes_list = state
    boxes = set(boxes_list)
    r, c = player
    deltas = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    delta = deltas[move]

    new_player = (r + delta[0], c + delta[1])
    new_boxes = []
    if new_player in boxes:
        new_box = (r + 2 * delta[0], c + 2 * delta[1])
        for b in boxes:
            if b == new_player:
                new_boxes.append(new_box)
            else:
                new_boxes.append(b)
    else:
        new_boxes = boxes
    return (new_player, *sorted(new_boxes))


# Checks that a state is valid: a) no box is in a corner
def is_valid_state(game: Game, state: GameState) -> bool:
    _, *boxes_list = state
    boxes = set(boxes_list)
    for box in boxes:
        if box in game.corners:
            return False
    return True


# Moves boxes around until they end in the endstate
def bfs(game: Game, state: GameState) -> Optional[list[str]]:
    queue = [state]
    CACHE[state] = state
    while queue:
        state = queue.pop(0)

        if game.is_finale(state):
            return reconstruct_path(state)  # build path here, return moves

        for option in get_move_options(game, state):
            new_state = compute_new_end_state(game, state, option)
            if new_state not in CACHE and is_valid_state(game, new_state):
                CACHE[new_state] = state
                queue.append(new_state)

    return None


def move_from_a_to_b_state(a: GameState, b: GameState):
    p1 = a[0]
    p2 = b[0]
    if p1[0] == p2[0]:
        if p1[1] < p2[1]:
            return "R"
        else:
            return "L"
    else:
        if p1[0] < p2[0]:
            return "D"
        else:
            return "U"


def reconstruct_path(curr: GameState):
    path = [curr]
    while CACHE[curr] is not curr:
        curr = CACHE[curr]
        path.append(curr)

    # Reverse the path
    path = path[::-1]
    return [move_from_a_to_b_state(a, b) for a, b in zip(path, path[1:])]


def print_info(game: Game, state: GameState):
    print(game.room_lines, state)
    # print(f"Board Lines: {game.room_lines}\nPlayer: {state[0]}\nBoxes: {state[1:]}\nEnd states: {game.end_states}")


def make_state(player: Point, boxes: list[Point]) -> GameState:
    return (player, *sorted(boxes))


# ********************************************************
case_nr = 1

CACHE: dict = {}
room_lines = load_gameconfig(case_nr)
game = Game(room_lines)
gs = load_gamestate(game, case_nr)

# print_info(game, gs)
game.print(gs)

path = bfs(game, gs)
print(path)

while path:
    print(path.pop(0))
    _ = load_gamestate(game, case_nr)
