import sys
import os
from typing import Any, Tuple
from dataclasses import dataclass
from collections import deque

Game = dict[str, Any]
Point = Tuple[int, int]
Board = dict[Point, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Robot Dataclass
@dataclass
class Robot:
    pos: Tuple = (0, 0)
    dir: str = "N"

    # Turn right
    def turn(self):
        if self.dir == "N":
            self.dir = "E"
        elif self.dir == "E":
            self.dir = "S"
        elif self.dir == "S":
            self.dir = "W"
        elif self.dir == "W":
            self.dir = "N"

    # Move to the point in front of the robot
    def move(self):
        self.pos = self.look_ahead()

    # Return the point in front of the robot
    def look_ahead(self):
        if self.dir == "N":
            return (self.pos[0] - 1, self.pos[1])
        elif self.dir == "E":
            return (self.pos[0], self.pos[1] + 1)
        elif self.dir == "S":
            return (self.pos[0] + 1, self.pos[1])
        elif self.dir == "W":
            return (self.pos[0], self.pos[1] - 1)

    # Check first if obstacle is in front; if so, turn right; then move
    def advance(self, board: Board):
        ahead = self.look_ahead()
        while board[ahead] == "#":
            self.turn()
            ahead = self.look_ahead()
        self.move()

    def __hash__(self):
        return hash((self.pos, self.dir))

    def __eq__(self, other):
        if isinstance(other, Robot):
            return self.pos == other.pos and self.dir == other.dir
        return False


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
                print(RED + board[p] + RESETCOL, end="")
            elif p in board:
                print(board[p], end="")
            else:
                print(" ", end="")
        print()
    print()


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        # w = 12
        # h = 6
        # n = 987
        # board = ["...#........", "...........#", "............", "............", "..#O........", "..........#."]

        w = 12
        h = 8
        n = 1234321
        board = [
            "....#.......",
            "........#...",
            "...........#",
            "...#O.......",
            "...#........",
            ".......#....",
            "...........#",
            "....#.......",
        ]

        # w = 16
        # h = 10
        # n = 12321123212397
        # board = [
        #     "...#...###......",
        #     "...............#",
        #     ".#..............",
        #     "...........#....",
        #     "................",
        #     "................",
        #     "..#O............",
        #     ".......####.....",
        #     "#...............",
        #     "###############.",
        # ]

        w = 6
        h = 5
        n = 15
        board = ["######", "##...#", "#.O#.#", "#....#", "######"]

        w = 5
        h = 5
        n = 4
        board = ["#####", "#...#", "#.#.#", "#...#", "##O##"]

    else:
        w, h = [int(i) for i in input().split()]
        n = int(input())
        board = [input() for _ in range(h)]

    if print_input:
        myPrint("w:", w)
        myPrint("h:", h)
        myPrint("n:", n)
        myPrint("board:", board)

    res = {}
    for r in range(h):
        for c in range(w):
            p = r, c
            res[p] = board[r][c]
            if board[r][c] == "O":
                res[p] = "O"
                start = p
    player = Robot(start)
    return res, player, n


def explore_board(board, p: Robot):
    visited = {}
    steps = 0
    while True:
        if p in visited:
            break
        new_p = Robot(p.pos, p.dir)
        visited[new_p] = steps
        p.advance(board)
        steps += 1

    # Invert the cache dict from {Robot: steps} to {steps: Robot}
    how_many_to_delete = visited[p]
    res = {v: k for k, v in visited.items()}
    for i in range(how_many_to_delete):
        del res[i]
    return res


# ********************************************************

board, player, n = get_start_parameters(print_input=True)

if n < 100000:
    for _ in range(n):
        player.advance(board)
else:
    cache = explore_board(board, player)
    steps = n % len(cache)
    player = cache[steps]

print(player.pos[1], player.pos[0])
