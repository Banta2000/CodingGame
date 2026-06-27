import sys
import os
import random
from typing import Any, Tuple, TypeAlias


Point: TypeAlias = Tuple[int, int]
PointSet: TypeAlias = set[Point]
Path: TypeAlias = list[Point]
Board: TypeAlias = dict[Point, Any]


HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_input() -> dict[str, Any]:
    def _config1():
        GS = {}
        GS["tree_treatment_duration"] = 3
        GS["tree_fire_duration"] = 2
        GS["tree_value"] = 1
        GS["house_treatment_duration"] = 5
        GS["house_fire_duration"] = 3
        GS["house_value"] = 60
        GS["width"] = 50
        GS["height"] = 40
        GS["start"] = (13, 16)
        GS["board"] = [
            "##################################################",
            "#################..............###################",
            "###########........................###############",
            "##########............................############",
            "#########...............XXXXXXX.........##########",
            "#######...............XXXXXXXXXX........##########",
            "######................XXXXXXXXXX.........#########",
            "#####.................XXXXXXXXXX.........#########",
            "####..................XXXXXXXXXX.........#########",
            "###....................XXXXXXXX..........#########",
            "##.......................................#########",
            "##.........................................#######",
            "##..........................................######",
            "#............................................#####",
            "#.............................................####",
            "#.............................................####",
            "##.............................................###",
            "####...........................................###",
            "#######........................................###",
            "###############................................###",
            "####################...........................###",
            "########............####.......................###",
            "####....................####...................###",
            "##..........................###................###",
            "#..............................................###",
            "#..............................................###",
            "#.............................................####",
            "#.............................................####",
            "##...............................XXXXXXX......####",
            "##.....XXXXXX...................XXXXXXXXX.....####",
            "##....XXXXXXXXX.................XXXXXXXXX.....####",
            "###...XXXXXXXXX.................XXXXXXXXX....#####",
            "####..XXXXXXXXX.................XXXXXXXXX....#####",
            "#####..XXXXXXX...................XXXXXXX....######",
            "#####.......................................######",
            "######.....................................#######",
            "########...................................#######",
            "#########.................................########",
            "###########..............................#########",
            "##################################################",
        ]
        return GS

    def _config2():
        GS = {}
        GS["tree_treatment_duration"] = 3
        GS["tree_fire_duration"] = 2
        GS["tree_value"] = 1
        GS["house_treatment_duration"] = 5
        GS["house_fire_duration"] = 3
        GS["house_value"] = 6100
        GS["width"] = 49
        GS["height"] = 49
        GS["start"] = (24, 24)
        GS["board"] = [
            "#################################################",
            "#...X.#....#.....#..#...X..#..X..#...#....###.#.#",
            "##..#.X#...#..#.##......##.#.##.....##......#...#",
            "#....####.....#....X...#..#............#....#...#",
            "#.###..#..........#................##.###.X#....#",
            "#.#..#....##.##...#....##..X....X.X...###.X...#.#",
            "#.##...#......#........X...#.........#.X#.......#",
            "#X..##..#.......#.#..##..###..###......#......#.#",
            "#.#....##..X...###.....###...####..#.......##..X#",
            "#.#...#......#.###..X..#...X###..X....#..#.....X#",
            "#...........#...#....#......#...#...#.###.......#",
            "#.....#.#....#............#..##......#.#..##....#",
            "##.#....X.#.#........#X.##...#.X..#.....##...#.##",
            "##..#..#.....#.#...#.##X.#..##.X#..X.#.##..#....#",
            "#..##...X............#.####..#...........#....#.#",
            "#..###.......##...........#......###..#.#XX#.#..#",
            "#X.##.###......#.X...###X####.##.....#.X#.......#",
            "#..##.#...###..#....X.#.#.#...#.#...X.#...#..#..#",
            "#............#....#...#.................#.......#",
            "##.#................#.#..X............#.####...X#",
            "#.....#...................#......#.#.......X.####",
            "#......#.#.......X#...#........#..#..X.....#....#",
            "##.....#..#.#.#.#............#X##.....#.........#",
            "#......#..........###X.........#..#....##...#.#.#",
            "#....#..#.##.#...#.#.X.X.#.....#..##.#......#...#",
            "#..#.X..#....#.....#.....X#..#......#.....#...#.#",
            "###......#..X##.#.........#...#...####.#..#.#.#.#",
            "#.....#.....##.#.....##....#..##..###...#.#.....#",
            "#.....##.#.....##.##.#......X#............#...#.#",
            "#....##..#......#.....#...........#...X.........#",
            "#...X#......#....###...#.##...........#..X##....#",
            "##.....#........#......X.#.....#..#.##.......#..#",
            "##.......##.................#.##X...........X.#.#",
            "##.....##.#..X......#..#.#........#........#...##",
            "##.....##..#.....#.#.#.#...#........##.........##",
            "#..X....#..##..###X..##....##..#..#X.##.#.#..X..#",
            "#......X...#...#.#...#.##....#..###.X....#...####",
            "#...X........#...X#......#...#.......#...#...X..#",
            "#.....#.......#X....##.....##...#.....#.##..##..#",
            "#.X#.#.......#.......####...#.#.##.#..X..#.#....#",
            "#.#...........#.#.#X.#.##..#.#..#..#.....#..##..#",
            "##...##.#.....#...#..#..#.#.X.#....X......#.#...#",
            "###....##....#.X....#...X......#...##...........#",
            "#..#..##..#.......#...#.X#...X...######XX.#.#.#.#",
            "#..#.....#..##....#.....#X##......##............#",
            "#X#.......X###....#...##.....#.....#..X..#X#....#",
            "#............#.#........#X.........#X...#..#....#",
            "#..#..........#......#...#...##......#...X.#...X#",
            "#################################################",
        ]
        return GS

    def _config3():
        GS = {}
        GS["tree_treatment_duration"] = 7
        GS["tree_fire_duration"] = 2
        GS["tree_value"] = 40
        GS["house_treatment_duration"] = 7
        GS["house_fire_duration"] = 10
        GS["house_value"] = 1000
        GS["width"] = 20
        GS["height"] = 20
        GS["start"] = (3, 6)
        GS["board"] = [
            "####################",
            "#######.############",
            "#####...############",
            "####....############",
            "###.....############",
            "##.......#####...###",
            "##................##",
            "#..................#",
            "#........#######...#",
            "#..................#",
            "#..............XX..#",
            "#.......###....XX..#",
            "#......######......#",
            "#......######.....##",
            "##.....#######...###",
            "##.....#############",
            "###....#############",
            "####...#############",
            "#####..#############",
            "####################",
        ]
        return GS

    def _config4():
        GS = {}
        GS["tree_treatment_duration"] = 3
        GS["tree_fire_duration"] = 2
        GS["tree_value"] = 100
        GS["house_treatment_duration"] = 2
        GS["house_fire_duration"] = 2
        GS["house_value"] = 3700
        GS["width"] = 10
        GS["height"] = 10
        GS["start"] = (3, 3)
        GS["board"] = [
            "##########",
            "#........#",
            "#........#",
            "#........#",
            "#........#",
            "#.....X..#",
            "#........#",
            "#........#",
            "#........#",
            "##########",
        ]
        return GS

    if HOME_PC:
        GS = _config4()

    else:
        GS = {}
        GS["tree_treatment_duration"], GS["tree_fire_duration"], GS["tree_value"] = [int(i) for i in input().split()]
        GS["house_treatment_duration"], GS["house_fire_duration"], GS["house_value"] = [int(i) for i in input().split()]
        width, height = [int(i) for i in input().split()]
        GS["width"], GS["height"] = width, height
        GS["start"] = tuple([int(i) for i in input().split()])
        GS["board"] = [input() for _ in range(height)]

    myDict = {}
    for row in range(GS["height"]):
        for col in range(GS["width"]):
            char = GS["board"][row][col]
            if char != "#":
                if char == ".":
                    myDict[(row, col)] = "T"
                if char == "X":
                    myDict[(row, col)] = "H"
    GS["board"] = myDict
    GS["start"] = (GS["start"][1], GS["start"][0])

    fire_start = GS["start"]
    GS["board"][fire_start] = GS["tree_fire_duration"]
    return GS


def get_update(GS: dict[str, Any]) -> dict[str, Any]:
    if HOME_PC:
        GS["cooldown"] = 0 if ready_for_new_input(GS["board"]) else 1
    else:
        GS["cooldown"] = int(input())  # number of turns remaining before you can cut a new cell
        for _ in range(GS["height"]):
            for j in input().split():
                # fire_progress: state of the fire in this cell (-2: safe, -1: no fire, 0<=.<fireDuration: fire, fireDuration: burnt)
                fire_progress = int(j)
                # myPrint(fire_progress)
    return GS


def print_board(board: Board) -> None:
    GREEN = "\033[92m"
    RESETCOL = "\x1b[0m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    max_row = max([row for row, _ in board])
    max_col = max([col for _, col in board])
    #     PURPLE = "\033[95m"
    #     OKCYAN = "\033[96m"

    #     ENDC = "\033[0m"
    #     BOLD = "\033[1m"
    # UNDERLINE = "\033[4m"
    for row in range(max_row + 1):
        for col in range(max_col + 1):
            if (row, col) in board:
                # Tree
                if board[(row, col)] == "T":
                    print(GREEN + "T" + RESETCOL, end="")

                # House
                if board[(row, col)] == "H":
                    print(YELLOW + "H" + RESETCOL, end="")

                # Burnt
                if board[(row, col)] == "X":
                    print(RED + "X" + RESETCOL, end="")

                # Fire
                if isinstance(board[(row, col)], int) and board[(row, col)] > 0:
                    print(RED + str(board[(row, col)]) + RESETCOL, end="")

                # Cutting
                if isinstance(board[(row, col)], int) and board[(row, col)] < 0:
                    print(BLUE + str(-board[(row, col)]) + RESETCOL, end="")

                # Border
                if board[(row, col)] == "B":
                    print("B", end="")
            else:
                print(" ", end="")
        print()


def visualize_path(board: Board, path: Path) -> None:
    new_board = board.copy()
    for point in path:
        new_board[point] = "B"
    print_board(new_board)


# In place advancement of the map; burns trees and houses; cuts trees
def advance_map(board: Board) -> None:
    new_board = board.copy()
    for point, v in new_board.items():
        r, c = point

        # Advance fire
        if isinstance(v, int) and v > 0:
            v -= 1
            board[point] = v
            if v == 0:
                board[point] = "X"
                for new_point in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:  # adjacent points
                    if new_point in board:
                        if new_board[new_point] == "T":
                            board[new_point] = GS["tree_fire_duration"]
                        if new_board[new_point] == "H":
                            board[new_point] = GS["house_fire_duration"]

        # Advance cutting
        if isinstance(v, int) and v < 0:
            v += 1
            if v != 0:
                board[point] = v
            else:
                del board[point]
    return


def find_border_points(board: Board) -> PointSet:
    border_points = set()
    for point, v in board.items():
        r, c = point
        neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for neighbour in neighbours:
            if neighbour not in board:
                border_points.add(point)
    return border_points


# Returns a dictionary of paths from start_point to border_points {(start, end): path}
def compute_paths_to_borderpoints(
    board: dict[str, Any], start_point: Point, border_points: PointSet
) -> dict[Point, Path]:

    result = {}
    visited = PointSet()
    stack = [(start_point, [])]
    while stack:
        current_point, current_path = stack.pop(0)
        if current_point in visited:
            continue
        visited.add(current_point)
        current_path = current_path.copy()
        current_path.append(current_point)
        if current_point in border_points:
            key = start_point, current_point
            result[key] = current_path
        r, c = current_point
        neighbours = [
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1),
            (r + 1, c + 1),
            (r + 1, c - 1),
            (r - 1, c + 1),
            (r - 1, c - 1),
        ]
        for neighbour in neighbours:
            if neighbour in board and neighbour not in visited:
                stack.append((neighbour, current_path))
    return result


# For a given starting point, runs a spreading simulation, returns all paths to border points that can be reached
def get_reachable_paths_to_border_points(
    original_board: Board, start_point: Point, border_points: PointSet
) -> list[Path]:
    def _find_reachable_points(board: Board, start_point: Point) -> dict[Point, Point]:
        board = original_board.copy()
        board[start_point] = -GS["tree_treatment_duration"]

        log_file = {}  # {target_point: origin_point}

        while True:
            cells_on_fire = [point for point, v in board.items() if isinstance(v, int) and v > 0]
            if not cells_on_fire:
                break

            # Spread fire
            for point in cells_on_fire:
                row, col = point
                board[point] -= 1

                if board[point] == 0:
                    board[point] = "X"
                    neighbours = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
                    neighbours = [n for n in neighbours if n in board]

                    for neighbour in neighbours:  # adjacent points
                        if board[neighbour] == "T":
                            board[neighbour] = GS["tree_fire_duration"]
                        if board[neighbour] == "H":
                            board[neighbour] = GS["house_fire_duration"]

            # Spread cutting
            cells_on_cutting = [point for point, v in board.items() if isinstance(v, int) and v < 0]
            for point in cells_on_cutting:
                row, col = point
                board[point] += 1

                #  Spread cutting
                if board[point] == 0:
                    del board[point]
                    neighbours = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
                    neighbours = [n for n in neighbours if n in board]

                    for neighbour in neighbours:
                        if board[neighbour] == "T":
                            board[neighbour] = -GS["tree_treatment_duration"]
                            log_file[neighbour] = point
                        if board[neighbour] == "H":
                            board[neighbour] = -GS["house_treatment_duration"]
                            log_file[neighbour] = point

        return log_file

    def recreate_paths_to_border_points(log_file: dict[Point, Point], border_points: PointSet) -> list[Path]:
        def _recreate_single_path(graph: dict[Point, Point], end_point: Point) -> Path:
            path = [end_point]
            current_point = end_point
            while current_point in graph:
                path.append(graph[current_point])
                current_point = graph[current_point]
            path.reverse()
            return path

        visited_points = set(list(log_file.keys()) + list(log_file.values()))
        visited_border_points = visited_points.intersection(border_points)

        paths = []
        for target_point in visited_border_points:
            path = _recreate_single_path(log_file, target_point)
            paths.append(path)
        return paths

    log_file = _find_reachable_points(original_board, start_point)
    paths = recreate_paths_to_border_points(log_file, border_points)

    return paths


# Removes the path from the map; burns down the map; returns the value of what's remaining
def path_value(GS, path: Path) -> int:
    # Remove the path
    new_board = GS["board"].copy()
    for point in path:
        del new_board[point]

    # Burn down the board
    start_point = GS["start"]
    stack = [start_point]
    while stack:
        current_point = stack.pop(0)
        if current_point not in new_board:
            continue
        del new_board[current_point]

        r, c = current_point
        neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for neighbour in neighbours:
            if neighbour in new_board:
                stack.append(neighbour)

    # Compute value of what's left
    value = 0
    for point, v in new_board.items():
        if v == "T":
            value += GS["tree_value"]
        if v == "H":
            value += GS["house_value"]

    return value


# Compute all the paths for a start point; return the best one
def compute_best_best_path_for_start_point(board: Board, start_point: Point, border_points: PointSet) -> Path:
    paths = compute_paths_to_borderpoints(board, start_point, border_points)
    sorted_paths = sorted(paths.items(), key=lambda x: path_value(GS, x[1]) / len(x[1]) / len(x[1]), reverse=True)
    best_path = sorted_paths[0][1]
    return best_path


# Return False if we are still cutting a cell; return True if we are ready to cut a new cell
def ready_for_new_input(board: Board):
    board_values = list(board.values())
    board_values_negative = [x for x in board_values if isinstance(x, int) and x < 0]
    return board_values_negative == []


# Runs a simulation of cutting down a path with fire; returns True if the path is valid; returns False if the path is invalid
def simulate(board: Board, fire_start: Point, original_path: Path) -> bool:
    new_board = board.copy()
    new_board[fire_start] = GS["tree_fire_duration"]
    path = original_path.copy()
    while True:
        if len(path) == 0:
            return True
        if ready_for_new_input(new_board):
            next_cut_pos = path.pop(0)
            if new_board[next_cut_pos] == "X":
                return False
            if new_board[next_cut_pos] == "T":
                new_board[next_cut_pos] = -GS["tree_treatment_duration"]
            if new_board[next_cut_pos] == "H":
                new_board[next_cut_pos] = -GS["house_treatment_duration"]
        advance_map(new_board)


# ********************************************************

GS = get_input()

border_points = find_border_points(GS["board"])

# start_point = (1, 6)
# best_path = get_reachable_paths_to_border_points(GS["board"], start_point, border_points)


# # Pick a number of random starting points
border_points_selection = set()
while len(border_points_selection) != 10:
    border_points_selection.add(random.choice(list(border_points)))


# # Collect all paths for this selection of starting points
possible_paths = []
for start_point in border_points_selection:
    res = get_reachable_paths_to_border_points(GS["board"], start_point, border_points)
    possible_paths.extend(res)

possible_paths.sort(key=lambda path: path_value(GS, path), reverse=True)
best_path = possible_paths[0]


myPrint("Best Path", best_path)
# visualize_path(GS["board"], best_path)

# best_path = [(1, 6), (2, 6), (3, 6), (3, 7), (3, 8)]

while True:
    GS = get_update(GS)
    if GS["cooldown"] == 0 and len(best_path) > 0:
        next_cut_pos = best_path.pop(0)

        print(next_cut_pos[1], next_cut_pos[0])

        if HOME_PC:
            if GS["board"][next_cut_pos] == "T":
                GS["board"][next_cut_pos] = -GS["tree_treatment_duration"]
            if GS["board"][next_cut_pos] == "H":
                GS["board"][next_cut_pos] = -GS["house_treatment_duration"]

    else:
        print("WAIT")

    if HOME_PC:
        advance_map(GS["board"])
        print_board(GS["board"])
        input()
