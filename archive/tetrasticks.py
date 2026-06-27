import sys
import os
from typing import Any, Tuple, List, Optional
from copy import deepcopy
from random import randint


Point = tuple[int, int]
Game = dict[str, Any]
TetraStruct = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
HOME_PC: bool = os.getenv("HOME_PC") == "True"


class Tetra:
    def __init__(self, letter: str, tetra: TetraStruct, flipped: int = 0, offset: Point = 0, rotation: int = 0) -> None:
        self.letter = letter
        self.tetra = tuple(sorted(tetra))
        self.offset = offset
        self.rotation = rotation
        self.flipped = flipped
        self.transition_points = self.get_transition_points()

    def __hash__(self):
        return hash(self.tetra)

    def __eq__(self, other):
        if not isinstance(other, Tetra):
            return False
        return self.tetra == other.tetra

    def create_string(self) -> str:
        return f"{self.letter} {self.flipped} {self.rotation} {self.offset[0]} {self.offset[1]}"

    def get_transition_points(self) -> List[Point]:
        res = []
        for i in range(len(self.tetra) - 1):
            for j in range(i + 1, len(self.tetra)):
                ar, ac = self.tetra[i]
                br, bc = self.tetra[j]
                if ar % 2 == 0 and ar == br and ac + 1 == bc:
                    res.append((ar // 2, ac + 1))
                elif ar % 2 == 1 and ar + 2 == br and ac == bc:
                    res.append((1 + (ar // 2), ac))
        return res


Board = list[Tetra]
BOARD: Board = []


BASIC_TETRAS: dict[str, TetraStruct] = {
    "F": ((0, 0), (1, 0), (2, 0), (3, 0)),
    "H": ((1, 0), (2, 0), (3, 0), (3, 1)),
    "J": ((3, 0), (4, 0), (3, 1), (1, 1)),
    "L": ((1, 0), (3, 0), (5, 0), (6, 0)),
    "N": ((1, 0), (2, 0), (3, 1), (5, 1)),
    "O": ((0, 0), (1, 0), (1, 1), (2, 0)),
    "P": ((0, 0), (1, 1), (2, 0), (3, 0)),
    "R": ((0, 0), (1, 1), (2, 1), (3, 1)),
    "T": ((0, 0), (0, 1), (1, 1), (3, 1)),
    "U": ((1, 0), (2, 0), (2, 1), (1, 2)),
    "I": ((1, 0), (3, 0), (5, 0), (7, 0)),
    "V": ((1, 2), (3, 2), (4, 0), (4, 1)),
    "W": ((3, 0), (2, 0), (1, 1), (0, 1)),
    "X": ((2, 0), (1, 1), (2, 1), (3, 1)),
    "Y": ((1, 0), (3, 0), (5, 0), (2, 0)),
    "Z": ((0, 0), (1, 1), (3, 1), (4, 1)),
}

COLS = {
    "F": "\033[96m",
    "H": "\033[91m",
    "J": "\033[91m",
    "L": "\033[95m",
    "N": "\033[94m",
    "O": "\033[91m",
    "P": "\033[92m",
    "R": "\033[91m",
    "T": "\033[96m",
    "U": "\033[91m",
    "I": "\033[95m",
    "V": "\033[94m",
    "W": "\033[96m",
    "X": "\033[92m",
    "Y": "\033[95m",
    "Z": "\033[91m",
}


def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


def print_board() -> None:
    # Print a board made of a list of Tetra objects
    # .─.─.─.─.─.
    # │ │ │ │ │ │
    # .─.─.─.─.─.
    # │ │ │ │ │ │
    # .─.─.─.─.─.
    # │ │ │ │ │ │
    # .─.─.─.─.─.

    RESETCOL = "\x1b[0m"
    WHITE = "\033[97m"  # Added color for white

    # Create a dictionary to represent the board state
    board_dict = {(r, c): "." for r in range(11) for c in range(6) if (r % 2 == 0 and c < 5) or (r % 2 == 1 and c < 6)}

    # Mark the positions occupied by tetras
    for tetra in BOARD:
        for point in tetra.tetra:
            board_dict[point] = tetra.letter

    for r in range(11):
        if r % 2 == 0:
            print(" ", end="")
            for c in range(5):
                p = (r, c)
                if board_dict[p] == ".":
                    print(WHITE + "─" + RESETCOL, end=" ")
                else:
                    col = COLS[board_dict[p]]
                    print(col + "─" + RESETCOL, end=" ")
        else:
            for c in range(6):
                p = (r, c)
                if board_dict[p] == ".":
                    print(WHITE + "│" + RESETCOL, end=" ")
                else:
                    col = COLS[board_dict[p]]
                    print(col + "│" + RESETCOL, end=" ")
        print()
    print()


def print_board2() -> None:
    RESETCOL = "\x1b[0m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    WHITE = "\033[97m"  # Added color for white

    # Create a dictionary to represent the board state
    board_dict = {(r, c): "." for r in range(11) for c in range(6) if (r % 2 == 0 and c < 5) or (r % 2 == 1 and c < 6)}

    # Mark the positions occupied by tetras
    for tetra in BOARD:
        for point in tetra.tetra:
            board_dict[point] = tetra.letter

    if BOARD:
        last_tetra = BOARD[-1].tetra
    else:
        last_tetra = []

    for r in range(11):
        if r % 2 == 0:
            print(" ", end="")
            for c in range(5):
                p = (r, c)
                if p in last_tetra:
                    print(RED + "─" + RESETCOL, end=" ")
                elif board_dict[p] == ".":
                    print(WHITE + "─" + RESETCOL, end=" ")
                else:
                    print(YELLOW + "X" + RESETCOL, end=" ")
        else:
            for c in range(6):
                p = (r, c)
                if p in last_tetra:
                    print(RED + "│" + RESETCOL, end=" ")
                elif board_dict[p] == ".":
                    print(WHITE + "│" + RESETCOL, end=" ")
                else:
                    print(YELLOW + "X" + RESETCOL, end=" ")
        print()
    print()


def translate_to_pos(stick: TetraStruct, offset: Tuple[int, int]) -> TetraStruct:
    # Translate Tetra to a position on the board
    newStick: TetraStruct = tuple([(r + 2 * offset[0], c + offset[1]) for r, c in stick])

    return newStick


def rotate(tetra: TetraStruct) -> TetraStruct:
    coll = []
    for point in tetra:
        r, c = point

        # Horizontal stick
        if r % 2 == 0:
            new_r = 1 + (2 * c)
            new_c = -(r // 2)

        # Vertical stick
        else:
            new_r = 2 * c
            new_c = -1 - (r // 2)

        new_point = (new_r, new_c)
        coll.append(new_point)
    newStick: TetraStruct = tuple(coll)
    newStick = recenter(newStick)
    return newStick


def flip_horizontal(tetra: TetraStruct) -> TetraStruct:
    coll = []
    for stick in tetra:
        r, c = stick
        # Horizontal stick
        if r % 2 == 0:
            new_r = r
            new_c = -1 - c

        # Vertical stick
        else:
            new_r = r
            new_c = -c

        coll.append((new_r, new_c))
    newStick: TetraStruct = tuple(coll)
    newStick = recenter(newStick)
    return newStick


def recenter(stick: TetraStruct) -> TetraStruct:
    minr = min([x[0] for x in stick])
    minr = minr // 2 * 2
    minc = min([x[1] for x in stick])
    newStick: TetraStruct = tuple([(r - minr, c - minc) for r, c in stick])
    return newStick


def get_input(choice: int):
    if choice == 0:
        m = int(input())  # num remaining tetrasticks to place
        remaining = input().split()
        myPrint(f"{m} to place: {remaining}")

        n = int(input())  # amount of already placed tetrasticks
        already_placed = [input() for _ in range(n)]
        myPrint(f"{n} already placed: {already_placed}")

    elif choice == 1:
        remaining = ["X", "N", "L"]
        already_placed = [
            "Z 0 0 0 2",
            "I 0 0 0 5",
            "H 0 1 0 3",
            "F 0 0 1 4",
            "U 0 3 2 0",
            "V 0 1 3 0",
            "P 0 0 3 1",
            "R 1 1 1 1",
            "W 0 3 2 2",
            "T 0 0 3 3",
            "O 0 0 4 2",
            "J 1 3 4 3",
        ]

    elif choice == 2:
        remaining = ["P", "R", "T", "U", "V", "X", "Z"]
        already_placed = [
            "L 0 0 0 0",
            "N 1 1 0 0",
            "O 0 0 0 4",
            "J 1 0 3 0",
            "W 0 1 3 2",
            "H 0 2 3 4",
            "F 0 1 4 1",
            "I 0 1 5 1",
        ]

    elif choice == 3:
        remaining = ["P", "R", "T", "U", "V", "X", "Z", "L", "N", "O", "J"]
        already_placed = [
            "W 0 1 3 2",
            "H 0 2 3 4",
            "F 0 1 4 1",
            "I 0 1 5 1",
        ]

    elif choice == 4:
        remaining = ["F", "H", "I", "L", "N", "O", "P", "R", "T", "U", "V", "W", "X", "Y", "Z"]
        already_placed = []

    remaining = set(remaining)

    return remaining, already_placed


def generate_all_options_of_one_letter(letter):
    def is_in_bounds(tetra: TetraStruct) -> bool:
        for point in tetra:
            r, c = point
            if r % 2 == 0:
                # Horizontal stick
                if r < 0 or r > 10 or c < 0 or c > 4:
                    return False
            else:
                if r < 1 or r > 9 or c < 0 or c > 5:
                    return False
        return True

    res = []

    base_piece = BASIC_TETRAS[letter]
    flipped = 0
    for rotation in range(4):
        rotated_piece = base_piece
        for _ in range(rotation):
            rotated_piece = rotate(rotated_piece)

        for r in range(6):
            for c in range(6):
                offset = (r, c)
                new_piece = translate_to_pos(rotated_piece, offset)
                if is_in_bounds(new_piece):
                    res.append(Tetra(letter, new_piece, flipped, offset, rotation))

    base_piece = flip_horizontal(base_piece)
    flipped = 1
    for rotation in range(4):
        rotated_piece = base_piece
        for _ in range(rotation):
            rotated_piece = rotate(rotated_piece)

        for r in range(6):
            for c in range(6):
                offset = (r, c)
                new_piece = translate_to_pos(rotated_piece, offset)
                if is_in_bounds(new_piece):
                    res.append(Tetra(letter, new_piece, flipped, offset, rotation))

    res = set(res)
    return res


def generate_all_options_of_all_letters() -> list[Tetra]:
    all_options = []
    for letter in BASIC_TETRAS.keys():
        res = generate_all_options_of_one_letter(letter)
        res = set(res)
        all_options.extend(res)
    return all_options


def fits_on_board(new_tetra: Tetra) -> bool:
    occupied_edges = set()
    occupied_transition_points = set()

    # Build lookups
    for placed_tetra in BOARD:
        occupied_edges.update(placed_tetra.tetra)
        occupied_transition_points.update(placed_tetra.transition_points)

    # Two edges collide
    for edge in new_tetra.tetra:
        if edge in occupied_edges:
            return False

    # Transition point collissions
    for point in new_tetra.transition_points:
        if point in occupied_transition_points:
            return False

    # Placing it would create an island
    free_segments = get_free_segments()
    free_segments = free_segments - set(new_tetra.tetra)
    if not are_all_islands_multiple_of_four(free_segments):
        return False

    return True


def add_tetras_to_board(list_of_tetras):
    if type(list_of_tetras) == list:
        for line in list_of_tetras:
            letter, flip, rotation, offset_r, offset_c = line.split(" ")
            letter = letter.strip()
            flip = int(flip.strip())
            rotation = int(rotation.strip())
            offset_r = int(offset_r.strip())
            offset_c = int(offset_c.strip())
            offset = (offset_r, offset_c)

            letter_points = BASIC_TETRAS[letter]
            if flip == 1:
                letter_points = flip_horizontal(letter_points)
            for _ in range(rotation):
                letter_points = rotate(letter_points)
            letter_points = translate_to_pos(letter_points, offset)
            tetra = Tetra(letter, letter_points, flip, offset, rotation)
            BOARD.append(tetra)

    # If we are passing a single Tetra object
    elif type(list_of_tetras) == Tetra:
        BOARD.append(list_of_tetras)

    return


def backtrack(remaining: List[str]) -> Optional[List[Tetra]]:
    if not remaining:
        return []

    free_segments = get_free_segments()

    # key = free_segments | remaining
    key = tuple(sorted(free_segments) + sorted(remaining))
    if key in CACHE:
        return CACHE[key]

    # Abort if board has islands != 4
    if not are_all_islands_multiple_of_four(free_segments):
        CACHE[key] = None
        return None

    # Abort if any remaining piece cannot be placed
    if not can_all_remaining_pieces_be_placed(remaining):
        CACHE[key] = None
        return None

    # Abort if any segment is not covered
    if not are_all_segments_covered_by_a_piece(free_segments, remaining):
        CACHE[key] = None
        return None

    next_segment = select_next_segment(free_segments, remaining)
    candidates = [p for p in all_pieces if p.letter in remaining]
    candidates = [p for p in candidates if next_segment in p.tetra]
    candidates = [p for p in candidates if fits_on_board(p)]

    # print_board2()
    # print(remaining)
    a = 2

    for candidate in candidates:
        add_tetras_to_board(candidate)
        result = backtrack(remaining - set(candidate.letter))
        if result is not None:
            CACHE[key] = [candidate] + result
            return CACHE[key]

        BOARD.pop()

    CACHE[key] = None
    return None  # No placement worked


def sort_by_complexity(remaining: List[str]) -> List[str]:
    # Sort remaining pieces by number of valid configurations; pieces with fewer configurations are placed first.
    complexity = {letter: sum(1 for piece in all_pieces if piece.letter == letter) for letter in remaining}
    return sorted(remaining, key=lambda x: complexity[x])


def prioritize_constrained_areas(board: Board) -> List[Point]:
    """
    Generate a list of points prioritized by constrained areas:
    1. Corners
    2. Edges
    3. Center
    """
    corners = [(0, 0), (0, 4), (10, 0), (10, 4)]
    edges = [(r, c) for r, c in board if r in [0, 10] or c in [0, 4]]
    center = [(r, c) for r, c in board if (r, c) not in corners and (r, c) not in edges]
    return corners + edges + center


def generate_edges_graph():
    # Generate All Edges
    all_edges = set()
    for p in all_pieces:
        for point in p.tetra:
            all_edges.add(point)

    graph = {}

    # Generate Horizontal Edges
    for r in range(0, 11, 2):
        for c in range(0, 5):
            neighbours = [(r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
            neighbours = [x for x in neighbours if x in all_edges]
            graph[(r, c)] = neighbours

    # Generate Vertical Edges
    for r in range(1, 10, 2):
        for c in range(0, 6):
            neighbours = [(r - 1, c - 1), (r - 2, c), (r - 1, c), (r + 1, c - 1), (r + 2, c), (r + 1, c)]
            neighbours = [x for x in neighbours if x in all_edges]
            graph[(r, c)] = neighbours
    return graph


def are_all_islands_multiple_of_four(available):
    def explore_one_island(available, start_point) -> set:
        visited = set()
        stack = [start_point]
        while stack:
            curr = stack.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            neighbours = graph[curr]
            neighbours = [x for x in neighbours if x not in visited and x in available]
            stack.extend(neighbours)
        return visited

    key = tuple(sorted(available))
    if key in CACHE:
        return CACHE[key]

    # Get all islands
    islands = []
    while len(available) > 0:
        start_point = list(available)[0]
        visited = explore_one_island(available, start_point)
        islands.append(visited)
        available = available - visited

    # Check all islands bigger than 4 and mod 4
    islands_len = [len(x) for x in islands]
    bigger_4 = [x >= 4 for x in islands_len]
    mod_4 = [x % 4 == 0 for x in islands_len]
    result = all(bigger_4) and all(mod_4)
    CACHE[key] = result
    return result


def are_all_segments_covered_by_a_piece(available, remaining):
    candidates = [p for p in all_pieces if p.letter in remaining and fits_on_board(p)]
    covered_by_candidates = set()
    for candidate in candidates:
        covered_by_candidates = covered_by_candidates | set(candidate.tetra)
    return available == covered_by_candidates


def can_all_remaining_pieces_be_placed(remaining):
    for letter in remaining:
        if not any(fits_on_board(p) for p in all_pieces if p.letter == letter):
            return False
    return True


def get_free_segments():
    available = set(graph.keys())
    for tetra in BOARD:
        available = available - set(tetra.tetra)
    return available


def select_next_segment(free_segments, remaining: List[str]) -> Point:
    # Choose based on simple sorting (book reading sequence)
    # return sorted(free_segments)[0]

    # Filter down candidates
    candidates = [p for p in all_pieces if p.letter in remaining]
    candidates = [p for p in candidates if fits_on_board(p)]

    # Count how many candidates cover each segment
    counter = {}
    for candidate in candidates:
        for segment in candidate.tetra:
            if segment not in counter:
                counter[segment] = 0
            counter[segment] += 1

    min_coverage = min(counter.values())

    # Find list of segments with minimal coverage
    min_segments = [k for k, v in counter.items() if v == min_coverage]

    return sorted(min_segments)[0]


# ********************************************************

remaining, placed_tetras = get_input(1)
add_tetras_to_board(placed_tetras)
all_pieces = generate_all_options_of_all_letters()
graph = generate_edges_graph()
CACHE = {}

print_board()

solution = backtrack(remaining)

for piece in solution:
    print(piece.create_string())


# PICK A RANDOM PIECE AND SHOW IT
# i = randint(0, len(all_pieces) - 1)
# tetra = all_pieces[i]
# print(tetra.letter, tetra.tetra)
# print(tetra.transition_points)
# board.append(tetra)
# print_board(board)
