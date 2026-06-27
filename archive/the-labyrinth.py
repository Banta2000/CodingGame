import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "True"


def myPrint(*args: Any, end: str = "\n") -> None:
    # If a single argument is a list or tuple, print its elements as separate arguments
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        print(*args[0], file=sys.stderr, flush=True, end=end)
    else:
        print(*args, file=sys.stderr, flush=True, end=end)


def get_start_parameters():
    # r: rows.   c: columns.  # a: alarm
    r, c, a = [int(i) for i in input().split()]
    return r, c, a


def get_new_pos_and_update_board() -> Tuple[int, int]:
    POS = tuple([int(i) for i in input().split()])

    # Update BOARD
    data = [input() for _ in range(NUM_ROWS)]
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if BOARD[(r, c)] == "?":
                BOARD[(r, c)] = char
    return POS


def print_board():
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if (r, c) == POS:
                myPrint("P", end="")
            else:
                myPrint(BOARD[(r, c)], end="")
        myPrint()


def is_border_fog_of_war_cell(p):
    # Returns True if cell is at the border of fog of war (cell == "." and neighbouring a ? cell)
    r, c = p
    if BOARD[p] != ".":
        return False
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    neighbours = [n for n in neighbors if n in BOARD]
    neighbors = [n for n in neighbours if BOARD[n] == "?"]
    return len(neighbors) > 0


def get_cardinal_cells_on_board(p):
    # Returns cardinal cells (up, down, left, right) of cell p
    r, c = p
    res = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    res = [cell for cell in res if cell in BOARD]
    return res


def identify_next_target():
    # Returns next cell at the border of fog of war

    # If return home, navigate to home
    if MODUS == "RETURN HOME":
        myPrint("TARGET HOME:", START_POS)
        return START_POS

    # If we see console, navigtate to console
    if "C" in BOARD.values():
        for p, char in BOARD.items():
            if char == "C":
                myPrint("TARGET CONSOLE:", p)
                return p

    # Else, navigate to next border fog of war cell
    path_cells = [p for p in BOARD if BOARD[p] == "."]
    fog_of_war_cells = [p for p in path_cells if is_border_fog_of_war_cell(p)]
    if len(path_cells) == 0:
        print("ERROR, NO FOG OF WAR BORDER CELL")
    for candidate in fog_of_war_cells:
        path_to_target = find_path(candidate)
        if path_to_target is not None:
            myPrint("TARGET BORDER:", candidate)
            return candidate


def find_path(target, start_pos=None):
    # Returns path to target
    stack = []
    visited = set()
    if start_pos is None:
        start_pos = POS
    stack.append([start_pos, []])
    while stack:
        curr, path = stack.pop(0)
        if curr == target:
            path = path[1:] + [curr]
            return path
        if curr in visited:
            continue
        visited.add(curr)
        r, c = curr
        neighbours = get_cardinal_cells_on_board(curr)
        neighbours = [n for n in neighbours if BOARD[n] in WALKABLE_CELLS]
        neighbours = [n for n in neighbours if n not in visited]
        for n in neighbours:
            stack.append([n, path + [curr]])


def player_at_console(POS):
    # Returns True if player is at console
    return BOARD[POS] == "C"


def get_next_step(path):
    # Returns "UP", "DOWN", "LEFT", "RIGHT" based on path[0] and POS
    row_p, col_p = POS
    row_t, col_t = path[0]
    if row_t < row_p:
        return "UP"
    elif row_t > row_p:
        return "DOWN"
    elif col_t < col_p:
        return "LEFT"
    elif col_t > col_p:
        return "RIGHT"


def load_test_case():
    POS = 5, 13
    START_POS = 2, 25
    data = [
        "?????????????????####.....##??",
        "?????????????????.##########??",
        "?????????????????.#......T##??",
        "???????????#...#..#.#######.??",
        "???????????.#######...#####.??",
        "???????????.#C..#####.##??????",
        "???????????.###.......##??????",
        "???????????.#.########..??????",
        "?????????????.##....####??????",
        "??????????????????????????????",
        "??????????????????????????????",
        "??????????????????????????????",
        "??????????????????????????????",
        "??????????????????????????????",
        "??????????????????????????????",
    ]

    update_board(data)
    # MODUS = "EXPLORATION"
    MODUS = "RETURN HOME"

    return POS, START_POS, MODUS

    # Approach: pick target: A) Console (if exists), B) Border fog of war cell
    # At every step, re-evaluate fog of war cells, pick semi-randomly one of them

    # NUM_ROWS, NUM_COLS, ALARM_COUNTER = get_start_parameters()
    # BOARD = {(r, c): "?" for r in range(NUM_ROWS) for c in range(NUM_COLS)}
    # MODUS = "EXPLORATION"
    # START_POS = None

    # while True:
    #     POS = update_game()
    #     if START_POS is None:
    #         START_POS = POS

    #     print_board()
    #     myPrint("POS:", POS)

    #     if player_at_console(POS):
    #         MODUS = "RETURN HOME"
    #         myPrint("FOUND CONSOLE, RETURNING HOME")

    #     next_target = identify_next_target()
    #     path_to_target = find_path_to_target(next_target)
    #     myPrint("PATH TO TARGET:", path_to_target)

    #     next_step = get_next_step(path_to_target)
    #     print(next_step)

    # ********************************************************


def get_explore_stack():
    # Returns a stack of cells to explore
    explore_stack = [p for p, char in BOARD.items() if char in TO_EXPLORE_CELLS]
    return explore_stack


def get_already_visited_cells():
    # Returns a list of cells that have been visited
    visited_cells = [p for p, char in BOARD.items() if char == "x"]
    return visited_cells


def console_exists_and_reachable_in_time():
    # Returns True if console exists and is reachable in time
    if "C" not in BOARD.values():
        return False
    myPrint("CONSOLE EXISTS")
    console_pos = [p for p, char in BOARD.items() if char == "C"][0]
    path_to_console = find_path(START_POS, console_pos)
    myPrint("PATH TO CONSOLE:", path_to_console)
    if path_to_console is None:
        return False
    return len(path_to_console) <= ALARM_COUNTER


def update_start_and_console_positions():
    global START_POS, CONSOLE_POS
    # Updates START_POS and CONSOLE_POS based on current BOARD state
    if START_POS is None:
        START_POS = POS
    if CONSOLE_POS is None and "C" in BOARD.values():
        CONSOLE_POS = [p for p, char in BOARD.items() if char == "C"][0]


# ****************************************************************

WALKABLE_CELLS = [".", "T", "x", "C"]
TO_EXPLORE_CELLS = ["."]
NUM_ROWS, NUM_COLS, ALARM_COUNTER = get_start_parameters()
BOARD = {(r, c): "?" for r in range(NUM_ROWS) for c in range(NUM_COLS)}
MODUS = "EXPLORE"
EXPLORE_STACK = []
START_POS = None
CONSOLE_POS = None

while True:
    POS = get_new_pos_and_update_board()
    update_start_and_console_positions()
    myPrint("POS:", POS)
    myPrint("START POS:", START_POS)
    myPrint("CONSOLE POS:", CONSOLE_POS)
    BOARD[POS] = "x" if BOARD[POS] == "." else BOARD[POS]

    print_board()

    # Update explore stack with new neighbours
    neighbours = get_cardinal_cells_on_board(POS)
    neighbours = [n for n in neighbours if BOARD[n] in TO_EXPLORE_CELLS]
    EXPLORE_STACK = neighbours + EXPLORE_STACK
    EXPLORE_STACK = [x for x in EXPLORE_STACK if x not in get_already_visited_cells()]
    myPrint("EXPLORE STACK:", EXPLORE_STACK)

    # Update modus
    if MODUS == "EXPLORE" and console_exists_and_reachable_in_time():
        MODUS = "GO TO CONSOLE"
    if MODUS == "GO TO CONSOLE" and BOARD[POS] == "C":
        MODUS = "RETURN HOME"
    myPrint("MODUS:", MODUS)

    # Select target based on modus
    if MODUS == "EXPLORE":
        next_target = EXPLORE_STACK[0]
    elif MODUS == "GO TO CONSOLE":
        next_target = CONSOLE_POS
    elif MODUS == "RETURN HOME":
        next_target = START_POS

    myPrint("NEXT TARGET:", next_target)
    # next_target = identify_next_target()
    path_to_target = find_path(next_target)
    myPrint("PATH TO TARGET:", path_to_target)
    next_step = get_next_step(path_to_target)
    print(next_step)


# NUM_ROWS, NUM_COLS = 14, 31
# BOARD = {(r, c): "?" for r in range(NUM_ROWS) for c in range(NUM_COLS)}
# POS, START_POS, MODUS = load_test_case()

# print_board()
# myPrint("POS:", POS)

# next_target = identify_next_target()
# path_to_target = find_path_to_target(next_target)
# myPrint("PATH TO TARGET:", path_to_target)

# next_step = get_next_step(path_to_target)
# print(next_step)
