import sys
import os
from typing import Any, Tuple
from enum import Enum
from collections import deque
from dataclasses import dataclass

Game = dict[str, Any]
POS = Tuple[int, int]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


class Direction(Enum):
    TOP = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4


@dataclass
class Agent:
    pos: POS
    dir: Direction


def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Logic Tiles: DIRECTION.TOP -> DIRECTION.DOWN   and  ASCII Tiles: (0,1) -> "-"
def load_assets():
    logic_tiles = [
        {},
        {Direction.TOP: Direction.DOWN, Direction.LEFT: Direction.DOWN, Direction.RIGHT: Direction.DOWN},
        {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT},
        {Direction.TOP: Direction.DOWN},
        {Direction.TOP: Direction.LEFT, Direction.RIGHT: Direction.DOWN},
        {Direction.TOP: Direction.RIGHT, Direction.LEFT: Direction.DOWN},
        {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT},
        {Direction.TOP: Direction.DOWN, Direction.RIGHT: Direction.DOWN},
        {Direction.LEFT: Direction.DOWN, Direction.RIGHT: Direction.DOWN},
        {Direction.TOP: Direction.DOWN, Direction.LEFT: Direction.DOWN},
        {Direction.TOP: Direction.LEFT},
        {Direction.TOP: Direction.RIGHT},
        {Direction.RIGHT: Direction.DOWN},
        {Direction.LEFT: Direction.DOWN},
    ]

    ascii_tiles = [
        [".....", ".....", ".....", ".....", "....."],
        ["..│..", "..│..", "──┼──", "..│..", "..│.."],
        [".....", ".....", "─────", ".....", "....."],
        ["..│..", "..│..", "..│..", "..│..", "..│.."],
        ["..│..", ".┌┘..", "─┘.┌─", "..┌┘.", "..│.."],
        ["..│..", "..└┐.", "─┐.└─", ".└┐..", "..│.."],
        ["..│..", "..│..", "──┴──", ".....", "....."],
        ["..│..", "..│..", "..├──", "..│..", "..│.."],
        [".....", ".....", "──┬──", "..│..", "..│.."],
        ["..│..", "..│..", "──┤..", "..│..", "..│.."],
        ["..│..", "..│..", "──┘..", ".....", "....."],
        ["..│..", "..│..", "..└──", ".....", "....."],
        [".....", ".....", "..┌──", "..│..", "..│.."],
        [".....", ".....", "──┐..", "..│..", "..│.."],
    ]
    ascii_tiles = [convert_2dmatrix_to_dict(tile) for tile in ascii_tiles]

    rotation_lookup = [
        [],
        [["WAIT", 1], ["WAIT", 1], ["WAIT", 1], ["WAIT", 1]],
        [["LEFT", 3], ["WAIT", 2], ["RIGHT", 3], ["DOUBLE", 2]],
        [["LEFT", 2], ["WAIT", 3], ["RIGHT", 2], ["DOUBLE", 3]],
        [["LEFT", 5], ["WAIT", 4], ["RIGHT", 5], ["DOUBLE", 4]],
        [["LEFT", 4], ["WAIT", 5], ["RIGHT", 4], ["DOUBLE", 5]],
        [["LEFT", 9], ["WAIT", 6], ["RIGHT", 7], ["DOUBLE", 8]],
        [["LEFT", 6], ["WAIT", 7], ["RIGHT", 8], ["DOUBLE", 9]],
        [["LEFT", 7], ["WAIT", 8], ["RIGHT", 9], ["DOUBLE", 6]],
        [["LEFT", 8], ["WAIT", 9], ["RIGHT", 6], ["DOUBLE", 7]],
        [["LEFT", 13], ["WAIT", 10], ["RIGHT", 11], ["DOUBLE", 12]],
        [["LEFT", 10], ["WAIT", 11], ["RIGHT", 12], ["DOUBLE", 13]],
        [["LEFT", 11], ["WAIT", 12], ["RIGHT", 13], ["DOUBLE", 10]],
        [["LEFT", 12], ["WAIT", 13], ["RIGHT", 10], ["DOUBLE", 11]],
    ]

    flip_direction_lookup = {
        Direction.TOP: Direction.DOWN,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWN: Direction.TOP,
    }

    DIR_CHANGES = {Direction.TOP: (0, -1), Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0), Direction.DOWN: (0, 1)}

    return logic_tiles, ascii_tiles, rotation_lookup, flip_direction_lookup, DIR_CHANGES


# Load the initial parameters
def get_start_parameters():
    if HOME_PC:
        w = scenario["w"]
        h = scenario["h"]
        ex = scenario["ex"]
        board = scenario["board"]
    else:
        w, h = [int(i) for i in input().split()]
        myPrint("w, h", [w, h])
        board = [input() for _ in range(h)]
        myPrint(board)
        board = [[int(x) for x in line.split(" ")] for line in board]
        ex = int(input())
        myPrint("ex", ex)
    ex = (ex, h - 1)
    board = convert_2dmatrix_to_dict(board)
    return board, ex


# Collection of scenarios to choose from
def load_scenario():
    # complex_underground = [
    #     [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 8, 3, 3, 5, 2, 2, 8, 2, 3, 13],
    #     [0, 0, 11, 5, 13, 0, 3, 0, 0, 3, 0, 0, 2],
    #     [0, 10, 10, 0, 3, 0, 2, 0, 11, 4, 10, 0, 2],
    #     [0, 3, 0, 0, 2, 0, 2, 0, 2, 0, 3, 0, 3],
    #     [0, 2, 0, 12, 10, 10, 1, 2, 10, 0, 3, 12, 10],
    #     [12, 6, 0, 2, 0, 3, 2, 12, 3, 3, 10, 4, 13],
    #     [11, 1, 2, 6, 2, 6, 6, 6, 2, 3, 2, 6, 10],
    # ]

    # sewer = [[0, 3, 0, 0, 0, 0, 0, 0], [0, 11, 2, 2, 2, 2, 13, 0], [0, 0, 0, 0, 0, 0, 3, 0], [0, 12, 2, 2, 2, 2, 10, 0]]

    # secret_pathways = [
    #     [0, 0, 0, 0, 0, 3],
    #     [8, 2, 2, 2, 2, 10],
    #     [3, 0, 0, 0, 12, 13],
    #     [11, 2, 2, 2, 1, 10],
    #     [2, 13, 0, 0, 3, 0],
    #     [0, 7, 2, 2, 4, 13],
    #     [0, 3, 0, 12, 4, 10],
    #     [0, 11, 2, 5, 10, 0],
    # ]

    # labyrinth = [
    #     [3, 12, 8, 6, 2, 2, 8, 2, 9, 0, 0, 0, 0],
    #     [11, 5, 10, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0],
    #     [0, 11, 2, 2, 2, 2, 6, 2, 1, 2, 2, 13, 0],
    #     [0, 0, 0, 0, 0, 12, 8, 2, 1, 2, 2, 9, 0],
    #     [0, 0, 12, 2, 2, 1, 4, 2, 10, 0, 0, 11, 13],
    #     [0, 0, 3, 0, 0, 7, 9, 0, 0, 0, 0, 0, 3],
    #     [0, 0, 11, 2, 2, 10, 11, 2, 2, 2, 2, 2, 9],
    #     [0, 12, 8, 2, 2, 2, 2, 8, 2, 2, 2, 2, 10],
    #     [0, 11, 4, 2, 2, 2, 2, 10, 12, 13, 12, 13, 0],
    #     [0, 0, 3, 12, 8, 8, 13, 12, 4, 5, 5, 10, 0],
    # ]

    # mausoleum = [
    #     [0, 0, 0, 0, 3, 0, 0, 0, 0],
    #     [0, 12, 2, 2, 10, 12, 2, 13, 0],
    #     [12, 10, 0, 0, 0, 11, 2, 9, 0],
    #     [11, 2, 2, 2, 2, 2, 13, 3, 0],
    #     [0, 12, 8, 8, 8, 13, 3, 3, 0],
    #     [12, 4, 5, 1, 10, 3, 3, 3, 0],
    #     [3, 7, 1, 4, 13, 7, 5, 6, 13],
    #     [11, 10, 3, 7, 10, 11, 4, 8, 4],
    #     [0, 12, 6, 10, 12, 2, 6, 10, 3],
    #     [12, 1, 2, 2, 10, 12, 8, 8, 10],
    #     [7, 10, 0, 0, 0, 7, 1, 4, 2],
    #     [3, 0, 0, 12, 13, 7, 9, 3, 0],
    #     [11, 2, 2, 5, 6, 4, 5, 10, 0],
    #     [0, 0, 12, 5, 13, 3, 3, 0, 0],
    #     [0, 0, 11, 10, 3, 11, 10, 0, 0],
    # ]
    # w, h = 13, 10 Mausoleum

    # broken_mausoleum = [
    #     [-3, 12, 8, 6, 3, 2, 7, 2, 7, 0, 0, 0, 0],
    #     [11, 5, 13, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0],
    #     [0, 11, 2, 2, 3, 3, 8, 2, -9, 2, 3, 13, 0],
    #     [0, 0, 0, 0, 0, 12, 8, 3, 1, 3, 2, 7, 0],
    #     [0, 0, 11, 2, 3, 1, 5, 2, 10, 0, 0, 11, 13],
    #     [0, 0, 3, 0, 0, 6, 8, 0, 0, 0, 0, 0, 2],
    #     [0, 0, 11, 3, 3, 10, 11, 2, 3, 2, 3, 2, 8],
    #     [0, 12, 6, 3, 2, 3, 3, 6, 3, 3, 2, 3, 12],
    #     [0, 11, 4, 2, 3, 2, 2, 11, 12, 13, 13, 13, 0],
    #     [0, 0, -3, 12, 7, 8, 13, 13, 4, 5, 4, 10, 0],
    # ]

    # broken_well = [[0, 0, -3, 0, 0], [0, 0, 2, 0, 0], [0, 0, -3, 0, 0]]

    # broken_sewer = [
    #     [0, -3, 0, 0, 0, 0, 0, 0],
    #     [0, 12, 3, 3, 2, 3, 12, 0],
    #     [0, 0, 0, 0, 0, 0, 2, 0],
    #     [0, -12, 3, 2, 2, 3, 13, 0],
    # ]

    # underground_complex = [
    #     [0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 8, 3, 3, 5, 2, 2, 8, 2, 3, 13],
    #     [0, 0, 11, 5, 13, 0, 3, 0, 0, 3, 0, 0, 2],
    #     [0, 10, 10, 0, 3, 0, 2, 0, 11, 4, 10, 0, 2],
    #     [0, 3, 0, 0, 2, 0, 2, 0, 2, 0, 3, 0, 3],
    #     [0, 2, 0, 12, 10, 10, 1, 2, 10, 0, 3, 12, 10],
    #     [12, 6, 0, 2, 0, 3, 2, 12, 3, 3, 10, 4, -13],
    #     [11, -1, 2, -6, 2, -6, 6, -6, 2, 3, 2, -6, -10],
    # ]

    # ROCKS 1
    # board = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, -3, 0],
    #     [0, 7, -2, 3, -2, 3, -2, 3, 11, 0],
    #     [0, -7, -2, 2, 2, 2, 2, 2, 2, -2],
    #     [0, 6, -2, 2, 2, 2, 2, 2, 2, -2],
    #     [0, -7, -2, 2, 2, 2, 2, 2, 2, -2],
    #     [0, 8, -2, 2, 2, 2, 2, 2, 2, -2],
    #     [0, -7, -2, 2, 2, 2, 2, 2, 2, -2],
    #     [0, -3, 0, 0, 0, 0, 0, 0, 0, 0],
    # ]
    # rocks = {1: [Agent((9, 2), Direction.RIGHT)]}
    # start_pos = (8, 0)
    # enter_dir = Direction.TOP
    # w, h = 10, 8
    # ex = 1

    # ROCKS 2
    # board = [
    #     [0, -3, 0, -3, 0, -3, 0, -3, -3, 0],
    #     [0, 7, -2, 3, -2, 2, -2, 3, 11, 0],
    #     [0, -7, -2, -2, -2, -2, 2, -2, 2, -2],
    #     [0, 6, -2, -2, -2, -2, -2, 2, -2, -2],
    #     [0, -7, -2, -2, -2, -2, 2, -2, 2, -2],
    #     [0, 8, -2, -2, -2, -2, -2, 2, -2, -2],
    #     [0, -7, -2, -2, -2, -2, 2, -2, 2, -2],
    #     [0, -3, 0, 0, 0, 0, 0, 0, 0, 0],
    # ]
    # w, h = 10, 8
    # ex = 1
    # start_pos = (8, 0)
    # enter_dir = Direction.TOP
    # rocks = {
    #     1: [Agent((9, 2), Direction.RIGHT), Agent((8, 0), Direction.TOP)],
    #     2: [Agent((9, 3), Direction.RIGHT)],
    #     3: [Agent((9, 4), Direction.RIGHT)],
    # }

    # AVOIDING ROCKS

    board = [
        [0, 3, 0, 0, -3, 0, -3, 0, -7, 2, -2],
        [0, 11, 3, 13, 3, 0, -3, 0, 3, 0, 0],
        [0, 12, 2, 12, -11, -13, -3, 0, -7, 2, -2],
        [0, 3, 0, 0, -12, -10, -3, 0, 3, 0, 0],
        [0, 2, 0, 0, -11, -8, -10, 0, -7, 2, -2],
        [0, 11, 3, -1, -2, -10, 0, 0, 3, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, -7, -2, -2],
        [0, 0, 0, 1, -2, -2, -2, -2, -10, 0, 0],
        [0, 12, 3, 12, 0, 0, 0, 0, 0, 0, 0],
        [0, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    rocks = {}

    w, h = 11, 10
    ex = 1
    start_pos = (1, 0)
    enter_dir = Direction.TOP
    # *************************************

    scenario = {
        "board": board,
        "start_pos": start_pos,
        "enter_dir": enter_dir,
        "w": w,
        "h": h,
        "ex": ex,
        "rocks": rocks,
    }

    return scenario


# [[1, 2, 3],[4, 5, 6]] -> {(0, 0): 1, (1, 0): 2, (2, 0): 3, }
def convert_2dmatrix_to_dict(matrix):
    res = {}
    for row, line in enumerate(matrix):
        for col, char in enumerate(line):
            res[(col, row)] = char
    return res


# Offsets the tile by input_point (move every point by input_point * 5)
def shift_tile(tile, point):
    tile_size = 5
    x_offset = point[0] * tile_size
    y_offset = point[1] * tile_size
    res = {}
    for key, value in tile.items():
        res[(key[0] + x_offset, key[1] + y_offset)] = value
    return res


# Prints a dictionary of points
def print_board(board: dict[tuple[int, int], str]) -> None:
    if HOME_PC:
        RESETCOL = "\x1b[0m"
        BLUE = "\033[94m"
        RED = "\033[91m"
    else:
        RESETCOL = ""
        BLUE = ""
        RED = ""

    # Build the board for printing
    visual_board = {}
    for point, tile in board.items():
        if tile < 0:
            tile = abs(tile)
        visual_board |= shift_tile(ascii_tiles[tile], point)

    min_x = min([x for x, _ in visual_board.keys()])
    min_y = min([x for x, _ in visual_board.keys()])

    max_x = max([x for x, _ in visual_board.keys()]) + 1
    max_y = max([y for _, y in visual_board.keys()]) + 1

    myPrint(" ", end="")
    for x in range(min_x, max_x // 5):
        myPrint("     ", end="")
        myPrint(x, end="")
    myPrint()

    for y in range(min_y, max_y):
        if y % 5 == 0:
            myPrint()

        if (y - 2) % 5 == 0:
            myPrint(y // 5, " ", end="")
        else:
            myPrint("   ", end="")

        for x in range(min_x, max_x):
            if x % 5 == 0:
                myPrint(" ", end="")
            if (x // 5, y // 5) == player.pos:
                myPrint(BLUE + visual_board[(x, y)] + RESETCOL, end="")
            elif (x // 5, y // 5) in [rock.pos for rock in rocks]:
                myPrint(RED + visual_board[(x, y)] + RESETCOL, end="")
            else:
                myPrint(visual_board[(x, y)], end="")
        myPrint()


# Returns player and rocks
def get_inputs(i: int) -> Tuple[Agent, list[Agent]]:
    try:
        player = globals().get("player", None)
    except NameError:
        player = None

    try:
        rocks = globals().get("rocks", None)
    except NameError:
        rocks = None

    if HOME_PC:
        if i == 0:
            pos = scenario["start_pos"]
            enter_dir = scenario["enter_dir"]
            rocks = []
            player = Agent(pos, enter_dir)
        else:
            if i in scenario["rocks"]:
                rocks += scenario["rocks"][i]
    else:
        inputs = input().split()
        xi = int(inputs[0])
        yi = int(inputs[1])
        pos = (xi, yi)
        enter_dir = inputs[2]
        enter_dir = Direction[enter_dir]

        rocks = []
        r = int(input())  # the number of rocks currently in the grid.
        for _ in range(r):
            inputs = input().split()
            xr = int(inputs[0])
            yr = int(inputs[1])
            tempDir = inputs[2]
            tempRock = Agent((xr, yr), Direction[tempDir])
            rocks.append(tempRock)
        player = Agent(pos, enter_dir)
    return player, rocks


# Returns possible rotations such that the tile connects to entry_dir
def get_possible_rotations(tile_nr, entry_dir):
    # myPrint("Room under examination", tile_nr)
    # myPrint("Entering room from", entry_dir)
    res = []

    if tile_nr < 0:
        return [("WAIT", tile_nr)]

    options = rotation_lookup[tile_nr]
    for rotate_direction, new_tile_nr in options:
        new_tile = logic_tiles[new_tile_nr]
        if entry_dir in new_tile:
            res.append((rotate_direction, new_tile_nr))
    return res


# Returns a possible path
def bfs(player: Agent, exit_pos: POS, history=None):
    if history is None:
        history = []

    def _calculate_clean_history(history, rotate_dir):
        if rotate_dir == "WAIT":
            return history + []
        elif rotate_dir == "DOUBLE":
            return history + [(cur.pos, "LEFT"), (cur.pos, "LEFT")]
        else:
            return history + [(cur.pos, rotate_dir)]

    node = (player, history)
    stack = deque([node])
    while stack:
        cur, history = stack.popleft()

        if cur.pos == exit_pos:
            # myPrint("Found exit")
            # if check_if_rock_collision(start_pos, entry_direction, start_rocks, history):
            #     continue
            return history

        if cur.pos not in board:
            continue

        # for rock in rocks:
        #     if rock["pos"] == pos:
        #         continue

        cur_layout_nr = board[cur.pos]
        options = get_possible_rotations(cur_layout_nr, cur.dir)

        for option in options:
            rotate_dir, new_tile_nr = option
            new_room_layout = logic_tiles[abs(new_tile_nr)]
            if cur.dir not in new_room_layout:
                continue
            exit_dir = new_room_layout[cur.dir]
            next_tile_enter_dir = flip_direction_lookup[exit_dir]
            delta = DIR_CHANGES[exit_dir]
            next_pos = (cur.pos[0] + delta[0], cur.pos[1] + delta[1])
            new_player = Agent(next_pos, next_tile_enter_dir)

            new_history = _calculate_clean_history(history, rotate_dir)
            # new_rocks = advance_rocks(rocks, new_history)

            # Skip if other node on stack with same next_pos and next_tile_enter_dir (history doesn't matter)
            if new_player in [x for x, _ in stack]:
                continue

            node = (new_player, new_history)
            stack.append(node)


# Returns updated board based on single instruction
def update_board(board, ins, pos):
    board = board.copy()
    if ins != "WAIT":
        curr_tile = board[pos]
        curr_tile = abs(curr_tile)
        new_tiles_options = rotation_lookup[curr_tile]
        new_tile_nr = [tile for tile in new_tiles_options if tile[0] == ins][0][1]
        board[pos] = new_tile_nr
    return board


# Returns updateded board based on single instruction, and updates player and rocks by one step
def update_board_and_agents(board, ins, pos, player, rocks):
    new_board = update_board(board, ins, pos)
    player = advance_agent(player, new_board)
    rocks = [advance_agent(rock, new_board) for rock in rocks]
    board[player.pos] = -abs(board[player.pos])
    for rock in rocks:
        board[rock.pos] = -abs(board[rock.pos])
    return new_board, player, rocks


# Prints the board in its solved state
def print_solution(path):
    solved_board = board.copy()
    for pos, ins in path:
        update_board(solved_board, ins, pos)
    print_board(solved_board)


# Return position and direction rocks based on board and according update instructions
def advance_rocks(rocks, instructions):
    # Update the board based on the change instructions
    solved_board = board.copy()
    for pos, ins in instructions:
        update_board(solved_board, ins, pos)

    # Update the position and direction of each rock
    new_rocks = []
    for rock in rocks:
        enter_dir = rock["dir"]
        pos = rock["pos"]
        room_nr = solved_board[pos]
        room_layout = logic_tiles[abs(room_nr)]

        if enter_dir not in room_layout:
            continue

        exit_dir = room_layout[enter_dir]
        delta = DIR_CHANGES[exit_dir]
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])
        new_enter_dir = flip_direction_lookup[exit_dir]
        new_rock = {"pos": new_pos, "dir": new_enter_dir}
        new_rocks.append(new_rock)
    return new_rocks


# Returns agent after he moved; if no move possible, returns the same agent
def advance_agent(agent, board):
    room_nr = board[agent.pos]
    room_layout = logic_tiles[abs(room_nr)]
    if agent.dir in room_layout:
        exit_dir = room_layout[agent.dir]
        delta = DIR_CHANGES[exit_dir]
        exit_pos = (agent.pos[0] + delta[0], agent.pos[1] + delta[1])
        new_entry_dir = flip_direction_lookup[exit_dir]

        # Check if I can enter the new room
        if exit_pos in board and new_entry_dir not in logic_tiles[abs(board[exit_pos])]:
            exit_pos = agent.pos
            new_entry_dir = agent.dir

    else:
        exit_pos = agent.pos
        new_entry_dir = agent.dir
    return Agent(exit_pos, new_entry_dir)


# Build new board based on instructions, check if there will be rock collision
def is_future_rock_collision(player, rocks, instructions):
    collission_rock = get_rock_in_path_of_player(player, rocks, instructions)
    if collission_rock is None:
        return False
    return True


# Returns rock that will collide with player, if any (else None)
def get_rock_in_path_of_player(player, rocks, instructions):
    solved_board = board.copy()
    for pos, ins in instructions:
        solved_board = update_board(solved_board, ins, pos)

    curr = player
    new_rocks = rocks.copy()
    while curr.pos in solved_board:
        curr = advance_agent(curr, solved_board)
        new_rocks = [advance_agent(rock, solved_board) for rock in new_rocks]
        for index, rock in enumerate(new_rocks):
            if curr.pos == rock.pos:
                return rocks[index]
    return None


# Returns first tile that can be changed in the path of the agent (first positive tile in path of rock or player)
def get_first_tile_that_can_be_changed_in_agent_path(agent, board):
    new_agent = agent
    new_agent = advance_agent(new_agent, board)

    while board[new_agent.pos] < 0:
        new_agent = advance_agent(new_agent, board)
    return new_agent.pos


# Checks if player is >= 1 time unit away from a certain tile; aka do we have time to inject a rock instruction
def is_spare_time(board, player, instructions):
    # If there are no instructions (only wait) we have time
    if instructions == []:
        return True

    new_board = board.copy()
    for pos, ins in instructions:
        new_board = update_board(new_board, ins, pos)

    target_pos, _ = instructions[0]
    new_player = player
    i = 0
    while new_player.pos != target_pos:
        new_player = advance_agent(new_player, new_board)
        i += 1
    return i > 1


# ********************************************************

logic_tiles, ascii_tiles, rotation_lookup, flip_direction_lookup, DIR_CHANGES = load_assets()
scenario = load_scenario()
board, exit_pos = get_start_parameters()

i = 0
while True:
    player, rocks = get_inputs(i)

    if HOME_PC:
        print_board(board)

    myPrint(player)
    for rock in rocks:
        myPrint(rock)

    instructions = bfs(player, exit_pos)

    if is_future_rock_collision(player, rocks, instructions) and is_spare_time(board, player, instructions):
        colliding_rock = get_rock_in_path_of_player(player, rocks, instructions)
        myPrint("Colliding rock", colliding_rock)
        first_tile = get_first_tile_that_can_be_changed_in_agent_path(colliding_rock, board)
        instructions = [(first_tile, "LEFT")] + instructions

    if instructions:
        pos, ins = instructions.pop(0)
        print(pos[0], pos[1], ins)
    else:
        pos, ins = (0, 0), "WAIT"
        print("WAIT")

    board, player, rocks = update_board_and_agents(board, ins, pos, player, rocks)
    i += 1
    myPrint("")


# rocks = [Agent((3, 5), Direction.RIGHT), Agent((4, 6), Direction.RIGHT), Agent((1, 2), Direction.TOP)]
