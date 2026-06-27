import sys
import os
from typing import Any, Tuple, List
from enum import Enum, auto

Game = dict[str, Any]
Point = Tuple[int, int]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


class Dir(Enum):
    UP = auto()
    UP_RIGHT = auto()
    RIGHT = auto()
    DOWN_RIGHT = auto()
    DOWN = auto()
    DOWN_LEFT = auto()
    LEFT = auto()
    UP_LEFT = auto()


DOMINO_CONFIG = {
    "|": {
        Dir.UP_RIGHT: [Dir.LEFT],
        Dir.RIGHT: [Dir.LEFT],
        Dir.DOWN_RIGHT: [Dir.LEFT],
        Dir.DOWN_LEFT: [Dir.RIGHT],
        Dir.LEFT: [Dir.RIGHT],
        Dir.UP_LEFT: [Dir.RIGHT],
    },
    "-": {
        Dir.UP_LEFT: [Dir.DOWN],
        Dir.UP: [Dir.DOWN],
        Dir.UP_RIGHT: [Dir.DOWN],
        Dir.DOWN_RIGHT: [Dir.UP],
        Dir.DOWN: [Dir.UP],
        Dir.DOWN_LEFT: [Dir.UP],
    },
    ".": {},
    "/": {
        Dir.LEFT: [Dir.RIGHT, Dir.DOWN_RIGHT, Dir.DOWN],
        Dir.UP_LEFT: [Dir.RIGHT, Dir.DOWN_RIGHT, Dir.DOWN],
        Dir.UP: [Dir.RIGHT, Dir.DOWN_RIGHT, Dir.DOWN],
        Dir.RIGHT: [Dir.LEFT, Dir.UP_LEFT, Dir.UP],
        Dir.DOWN_RIGHT: [Dir.LEFT, Dir.UP_LEFT, Dir.UP],
        Dir.DOWN: [Dir.LEFT, Dir.UP_LEFT, Dir.UP],
    },
    "\\": {
        Dir.UP: [Dir.LEFT, Dir.DOWN_LEFT, Dir.DOWN],
        Dir.UP_RIGHT: [Dir.LEFT, Dir.DOWN_LEFT, Dir.DOWN],
        Dir.RIGHT: [Dir.LEFT, Dir.DOWN_LEFT, Dir.DOWN],
        Dir.DOWN: [Dir.RIGHT, Dir.UP_RIGHT, Dir.UP],
        Dir.DOWN_LEFT: [Dir.RIGHT, Dir.UP_RIGHT, Dir.UP],
        Dir.LEFT: [Dir.RIGHT, Dir.UP_RIGHT, Dir.UP],
    },
}


class Domino:
    def __init__(self, char: str, pos: Point) -> None:
        self.char: str = char
        self.pos: Point = pos
        self.config = DOMINO_CONFIG[char]

    def __str__(self):
        return f"{self.char}"

    def __repr__(self):
        return f"{self.char}"

    # Returns boolean if Domino can be pushed from a (neighbouring) point
    def can_be_pushed(self, incoming_pos: Point) -> bool:
        incoming_dir = compute_direction(incoming_pos, self.pos)
        return incoming_dir in self.config

    def push(self, incoming_pos: Dir) -> list[Dir]:
        if self.char == ".":
            return []
        incoming_dir = compute_direction(incoming_pos, self.pos)
        if incoming_dir in self.config:
            self.char = "."
            return self.config[incoming_dir]
        else:
            return []


Board = dict[Point, Domino]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Print a dictionary board made of points and chars
def print_board(board: Board, visited=None) -> None:
    if visited is None:
        visited = set()
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"
    num_rows = max(k[0] for k in board.keys()) + 1
    num_cols = max(k[1] for k in board.keys()) + 1

    for r in range(num_rows):
        for c in range(num_cols):
            p = r, c
            if p in visited:
                print(RED + board[p].char + RESETCOL, end="")
            elif p in board:
                print(board[p], end="")
            else:
                print(" ", end="")
        print()
    print()


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Game:
    def _parse(data):
        board = {}
        for r, line in enumerate(data):
            for c, ch in enumerate(line):
                board[r, c] = Domino(ch, (r, c))
        return board

    if HOME_PC:
        # board = ["| / | /", "- . | -", "| | . \\", "| | | \\"]
        board = ["| \\ | /", ". - | -", ". - . -", ". / | \\"]
    else:
        n = int(input())
        board = [input() for i in range(n)]

    if print_input:
        myPrint(f"{board=}")

    board = [line.strip().split(" ") for line in board]

    board = _parse(board)
    return board


# Returns a Dir enum describing the direction from PoV of reference
def compute_direction(incoming: Point, reference: Point):
    LU = {
        (-1, -1): Dir.UP_LEFT,
        (-1, 0): Dir.UP,
        (-1, 1): Dir.UP_RIGHT,
        (0, -1): Dir.LEFT,
        (0, 1): Dir.RIGHT,
        (1, -1): Dir.DOWN_LEFT,
        (1, 0): Dir.DOWN,
        (1, 1): Dir.DOWN_RIGHT,
    }
    r1, c1 = incoming
    r2, c2 = reference
    delta = r1 - r2, c1 - c2
    if delta not in LU:
        print("ERROR")
    res = LU[delta]
    return res


# Returns a position based on the reference point and the given direction
def compute_pos(reference: Point, dir: Dir):
    LU = {
        Dir.UP_LEFT: (-1, -1),
        Dir.UP: (-1, 0),
        Dir.UP_RIGHT: (-1, 1),
        Dir.LEFT: (0, -1),
        Dir.RIGHT: (0, 1),
        Dir.DOWN_LEFT: (1, -1),
        Dir.DOWN: (1, 0),
        Dir.DOWN_RIGHT: (1, 1),
    }
    delta = LU[dir]
    r, c = reference[0] + delta[0], reference[1] + delta[1]
    return r, c


def bfs():
    start_domino = board.get((0, 0))

    # Determine the correct initial push based on the domino type
    initial_push_map = {
        "|": (0, -1),  # Push from LEFT
        "-": (-1, 0),  # Push from UP
        "/": (-1, -1),  # Push from UP_LEFT
    }
    from_pos = initial_push_map.get(start_domino.char)
    to_pos = (0, 0)

    stack = [(from_pos, to_pos)]
    while stack:
        from_pos, to_pos = stack.pop(0)
        curr = board[to_pos]
        resulting_directions = curr.push(from_pos)
        neighbours = [compute_pos(to_pos, x) for x in resulting_directions]
        neighbours = [x for x in neighbours if x in board]
        for n in neighbours:
            stack.append((to_pos, n))

        # Good practice: check if the target has already fallen before processing
        # if to_pos not in board or board[to_pos].char == ".":
        # continue


# ********************************************************

board = get_start_parameters(print_input=True)

bfs()
# print_board(board)

res = [v for k, v in board.items() if v.char != "."]
print(len(res))
