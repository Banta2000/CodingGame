import sys
import os
from typing import Any, Tuple, List, Optional
from copy import deepcopy
from random import randint
import copy
import logging

# Configure logging
logging.basicConfig(
    filename="logfile.log",  # Name of the log file
    level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(levelname)s - %(message)s",  # Log format
)

Point = tuple[int, int]
TetraStruct = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]


class Tetra:
    def __init__(self, letter: str, tetra: TetraStruct, flipped: int = 0, offset: Point = 0, rotation: int = 0) -> None:
        self.letter = letter
        self.tetra = tuple(sorted(tetra))
        self.offset = offset
        self.rotation = rotation
        self.flipped = flipped
        self.transition_points = self.get_transition_points()
        self.id = self.create_string()

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
                    res.append(("T", ar // 2, ac + 1))
                elif ar % 2 == 1 and ar + 2 == br and ac == bc:
                    res.append(("T", 1 + (ar // 2), ac))
        return res

    def __hash__(self):
        return hash(self.tetra)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


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

COLORS = {
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
    if choice == -1:
        input()  # num remaining tetrasticks to place
        input()
        n = int(input())  # amount of already placed tetrasticks
        for _ in range(n):
            input()
        return set(), []

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
        remaining = ["F", "H", "I", "L", "O", "P", "R", "T", "U", "V", "W", "X", "Y", "Z", "J"]
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

    # all_options = {x.id: x for x in all_options}
    return all_options


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


def filter_only_placeable_pieces(all_pieces):
    # Only keep pieces that are part of the remaining letters
    all_pieces = [x for x in all_pieces if x.letter in remaining]

    # Only keep pieces that fit on the board
    all_pieces = [x for x in all_pieces if fits_on_board(x)]
    return all_pieces


def fits_on_board(new_tetra: Tetra) -> bool:
    occupied_edges = set()

    # Build lookups
    for placed_tetra in BOARD:
        occupied_edges.update(placed_tetra.tetra)

    # Two edges collide
    for edge in new_tetra.tetra:
        if edge in occupied_edges:
            return False

    return True


def build_X_and_Y():
    # The columns of Y are all empty edges + letters + transition points
    empty_edges = set()
    transition_points = set()
    letters = set()
    for tetra in all_pieces:
        empty_edges.update(tetra.tetra)
        transition_points.update(tetra.transition_points)
        letters.add(tetra.letter)

    columns = empty_edges.union(letters).union(transition_points)

    # One row (piece) contains the letter, the segments adn the tras points
    Y = {}
    for piece in all_pieces:
        Y[piece.id] = set()
        Y[piece.id].update(piece.tetra)
        Y[piece.id].add(piece.letter)
        Y[piece.id].update(piece.transition_points)

    # # Build X from Y:
    X = {}
    for c in columns:
        X[c] = set()

    for row, cols in Y.items():
        for col in cols:
            X[col].add(row)

    return X, Y


def get_keys_with_least_number_of_values(D):
    D2 = {k: v for k, v in D.items() if len(k) != 3}
    min_val = min(len(v) for v in D2.values())
    keys = [k for k, v in D2.items() if len(v) == min_val]
    # Sort by the total number of columns covered by their rows
    keys.sort(key=lambda col: sum(len(Y[row]) for row in D[col]))
    return keys


def create_key(X):
    # I'm intersted in the remaining fields and letters
    letters = [k for k in X.keys() if len(k) == 1]
    fields = [k for k in X.keys() if len(k) == 2]
    letters.sort()
    fields.sort()
    return tuple(letters + fields)


def algo_x(X, Y, path=[]):
    # Check Cache
    key = create_key(X)
    if key in VISITED:
        return
    VISITED.add(key)

    remaining_fields = [x for x in X.keys() if len(x) != 3]

    if not remaining_fields:
        yield path
        return

    # Candidate cols: cols with most constraints
    candidate_cols = get_keys_with_least_number_of_values(X)
    logging.debug(f"Depth: {len(path)}, Candidate Columns: {candidate_cols}")

    for chosen_col in candidate_cols:
        logging.debug(f"Depth: {len(path)}, Chosen Column: {chosen_col}, Rows: {len(X[chosen_col])}")

        # Candidate rows: rows that include the col
        candidate_rows = sorted(X[chosen_col], key=lambda row: -len(Y[row]))
        for chosen_row in candidate_rows:
            cols_that_chosen_row_will_cover = Y[chosen_row]

            # All rows that include the cols of chosen_row must be deleted
            rows_to_delete = set()
            for col in cols_that_chosen_row_will_cover:
                rows_that_have_a_given_col = X[col]
                rows_to_delete.update(rows_that_have_a_given_col)

            X_copy = {k: v.copy() for k, v in X.items()}
            Y_copy = {k: v.copy() for k, v in Y.items()}

            # Delete the cols from X
            for c in cols_that_chosen_row_will_cover:
                del X_copy[c]

            # Delete the rows from Y
            for r in rows_to_delete:
                del Y_copy[r]

            # If any of the deleted rows is still mentioned in the cols, remove it
            for r in rows_to_delete:
                for values in X_copy.values():
                    if r in values:
                        values.remove(r)

            yield from algo_x(X_copy, Y_copy, path + [chosen_row])


# ********************************************************
TEST_CASE = 4


VISITED = set()
SOLUTION_COLLECTION = set()
remaining, placed_tetras = get_input(TEST_CASE)
add_tetras_to_board(placed_tetras)
all_pieces = generate_all_options_of_all_letters()
all_pieces = filter_only_placeable_pieces(all_pieces)
X, Y = build_X_and_Y()

SOLUTION = next(algo_x(X, Y), None)


for x in SOLUTION:
    print(x)
    if TEST_CASE == 0:
        _, _ = get_input(-1)
