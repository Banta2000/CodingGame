from typing import Tuple, List, Optional, List, Tuple, Iterator
from Point2D import Point2D
from dataclasses import dataclass
from collections import deque

HOME_PC = True
FULL_BOARD = [
    (3, 0),
    (2, 1),
    (3, 1),
    (4, 1),
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (0, 3),
    (1, 3),
    (2, 3),
    (3, 3),
    (4, 3),
    (5, 3),
    (6, 3),
    (1, 4),
    (2, 4),
    (3, 4),
    (4, 4),
    (5, 4),
    (2, 5),
    (3, 5),
    (4, 5),
    (3, 6),
    (-1, 3),
]
FULL_BOARD = set([Point2D(p[0], p[1]) for p in FULL_BOARD])

SAMPLES = {
    "data1": {
        "max_turns": 3,
        "dead_cells": [(3, 2), (3, 4)],
        "active_cells": [(0, 2, 3), (0, 3, 3)],
    },
    "data3": {
        "max_turns": 4,
        "dead_cells": [(1, 4), (5, 4)],
        "active_cells": [(0, 2, 4), (0, 3, 4), (5, 3, 3), (5, 4, 4), (5, 3, 5)],
    },
    "data5": {
        "max_turns": 30,
        "dead_cells": [(3, 1), (5, 4)],
        "active_cells": [(0, 3, 5), (0, 4, 5), (6, 1, 2), (6, -1, 3), (6, 0, 3), (7, 3, 2), (7, 4, 2), (7, 5, 3)],
    },
}


@dataclass
class Piece:
    id: int
    points: List[Point2D]

    def push_left(self):
        # Push piece one field to left
        new_points = [p.left() for p in self.points]
        new_piece = Piece(self.id, new_points)
        return new_piece

    def push_right(self):
        # Push piece one field to right
        new_points = [p.right() for p in self.points]
        new_piece = Piece(self.id, new_points)
        return new_piece

    def push_up(self):
        # Push piece one field up
        new_points = [p.up() for p in self.points]
        new_piece = Piece(self.id, new_points)
        return new_piece

    def push_down(self):
        # Push piece one field down
        new_points = [p.down() for p in self.points]
        new_piece = Piece(self.id, new_points)
        return new_piece

    def is_on_board(self):
        # Returns True if piece is within LIMITED BOARD
        for p in self.points:
            if p not in board.limited_board_points_set:
                return False
        return True

    def get_neighbours_right(self):
        # Returns the piece id's of all pieces that are directly to the right
        res = set()
        moved_points = [p.right() for p in self.points]
        ids = set([board.get_piece_id_at_point(p) for p in moved_points])
        ids.discard(None)
        ids.discard(self.id)
        return ids

    def get_neighbours_left(self):
        # Returns the piece id's of all pieces that are directly to the left
        res = set()
        moved_points = [p.left() for p in self.points]
        ids = set([board.get_piece_id_at_point(p) for p in moved_points])
        ids.discard(None)
        ids.discard(self.id)
        return ids

    def get_neighbours_up(self):
        # Returns the piece id's of all pieces that are directly above
        res = set()
        moved_points = [p.up() for p in self.points]
        ids = set([board.get_piece_id_at_point(p) for p in moved_points])
        ids.discard(None)
        ids.discard(self.id)
        return ids

    def get_neighbours_down(self):
        # Returns the piece id's of all pieces that are directly below
        res = set()
        moved_points = [p.down() for p in self.points]
        ids = set([board.get_piece_id_at_point(p) for p in moved_points])
        ids.discard(None)
        ids.discard(self.id)
        return ids


class Board:
    def __init__(self) -> None:
        self.full_board_points_set = FULL_BOARD
        self.limited_board_points_set = FULL_BOARD.copy()
        self.pieces: dict[int, Piece] = {}

    def get_state(self) -> tuple:
        """Get a hashable representation of the current board state.
        Only includes piece positions since other board properties are immutable.
        """
        # Sort pieces by ID for consistent hashing
        piece_positions = []
        for piece_id in sorted(self.pieces.keys()):
            piece = self.pieces[piece_id]
            # Sort points within each piece for consistency
            sorted_points = tuple(sorted((p[0], p[1]) for p in piece.points))
            piece_positions.append((piece_id, sorted_points))
        return tuple(piece_positions)

    def set_state(self, state: tuple) -> None:
        """Restore board to a given state representation."""
        self.pieces.clear()
        for piece_id, points_tuple in state:
            points = [Point2D(x, y) for x, y in points_tuple]
            self.pieces[piece_id] = Piece(piece_id, points)

    def remove_dead_cells_from_board(self, dead_cells):
        # Removes dead cells from the limited board points set, dead_cells is a list of (x,y) tuples
        for cell in dead_cells:
            p = Point2D(cell[1], cell[0])
            if p in self.limited_board_points_set:
                self.limited_board_points_set.remove(p)

    def get_piece_id_at_point(self, point: Point2D):
        # Returns the piece_id at the given point, or None if no piece is there
        for piece_id, piece in self.pieces.items():
            if point in piece.points:
                return piece_id
        return None

    def get_piece(self, piece_id: int):
        # Returns the piece with the given id, or None if not found
        return self.pieces.get(piece_id, None)

    def update_piece(self, piece: Piece):
        # Updates the piece in the board with the given piece (by id)
        self.pieces[piece.id] = piece

    def print(self):
        for row in range(7):
            print(" ", end="")
            for col in range(-1, 7):
                p = Point2D(row, col)
                if p not in self.full_board_points_set:
                    print(" ", end="")
                elif p not in self.limited_board_points_set:
                    print("X", end="")
                else:
                    id = self.get_piece_id_at_point(p)
                    if id is not None:
                        print(id, end="")
                    else:
                        print(".", end="")
            print("")

    def get_pieces_affected_by_push(self, id: int, direction: str):
        """Get all pieces that would be affected by pushing in given direction."""
        affected_pieces = set()
        affected_pieces.add(id)
        piece = self.get_piece(id)
        stack = [id]
        while stack:
            current_id = stack.pop()
            current_piece = self.get_piece(current_id)

            # Get neighbors based on direction
            if direction == "U":
                neighbours = current_piece.get_neighbours_up()
            elif direction == "D":
                neighbours = current_piece.get_neighbours_down()
            elif direction == "L":
                neighbours = current_piece.get_neighbours_left()
            elif direction == "R":
                neighbours = current_piece.get_neighbours_right()
            else:
                raise ValueError(f"Invalid direction: {direction}")

            for n in neighbours:
                if n not in affected_pieces:
                    affected_pieces.add(n)
                    stack.append(n)
        return affected_pieces

    def can_pieces_be_pushed(self, id: int, direction: str):
        """Check if pieces can be pushed in given direction without going off board."""
        for n in self.get_pieces_affected_by_push(id, direction):
            piece = self.get_piece(n)

            # Get new piece position based on direction
            if direction == "U":
                new_piece = piece.push_up()
            elif direction == "D":
                new_piece = piece.push_down()
            elif direction == "L":
                new_piece = piece.push_left()
            elif direction == "R":
                new_piece = piece.push_right()
            else:
                raise ValueError(f"Invalid direction: {direction}")

            if not new_piece.is_on_board():
                return False
        return True

    def push_pieces(self, id: int, direction: str):
        """Push all affected pieces in given direction."""
        for n in self.get_pieces_affected_by_push(id, direction):
            piece = self.get_piece(n)

            # Push piece based on direction
            if direction == "U":
                new_piece = piece.push_up()
            elif direction == "D":
                new_piece = piece.push_down()
            elif direction == "L":
                new_piece = piece.push_left()
            elif direction == "R":
                new_piece = piece.push_right()
            else:
                raise ValueError(f"Invalid direction: {direction}")

            self.update_piece(new_piece)

    def execute_move(self, move: Tuple[int, str]):
        piece_id, direction = move
        if self.can_pieces_be_pushed(piece_id, direction):
            self.push_pieces(piece_id, direction)

    def get_possible_moves(self):
        """Get all valid moves for current board state."""
        moves = []
        for piece_id in self.pieces.keys():
            for direction in ["U", "D", "L", "R"]:
                if self.can_pieces_be_pushed(piece_id, direction):
                    moves.append((piece_id, direction))
        return moves

    def is_solved(self):
        # Check if piece with id 0 is at the center (3,3) and (3,4)
        piece = self.get_piece(0)
        required_positions = {Point2D(3, 0), Point2D(3, 1)}
        return required_positions.issubset(set(piece.points))

    def solve(self):
        stack = deque()
        stack.append((board.get_state(), []))
        visited = set()
        visited.add(board.get_state())

        while stack:
            state, history = stack.popleft()
            board.set_state(state)
            if board.is_solved():
                return history

            possible_moves = board.get_possible_moves()
            original_state = board.get_state()
            for move in possible_moves:
                board.set_state(original_state)
                board.execute_move(move)
                new_state = board.get_state()
                if new_state not in visited:
                    visited.add(new_state)
                    new_history = history + [move]
                    stack.append((new_state, new_history))
        return None


def get_start_parameters(start_data: Optional[str] = None):
    board = Board()

    if start_data and start_data in SAMPLES:
        max_turns = SAMPLES[start_data]["max_turns"]
        dead_cells = SAMPLES[start_data]["dead_cells"]
        active_cells = SAMPLES[start_data]["active_cells"]
    else:
        max_turns = int(input())

        dead_cells = []
        dead_count = int(input())  # number of dead (immovable) cells
        for i in range(dead_count):
            x, y = [int(j) for j in input().split()]
            dead_cells.append((x, y))

        active_cells = []
        cell_count = int(input())  # number of cells currently occupied by molecules
        for i in range(cell_count):
            molecule_id, x, y = [int(j) for j in input().split()]
            active_cells.append((molecule_id, x, y))

    # First find all piece_ids, then create pieces and add to board
    all_pieces_id = set(p[0] for p in active_cells)
    for piece_id in all_pieces_id:
        points_of_piece = [Point2D(p[2], p[1]) for p in active_cells if p[0] == piece_id]
        board.pieces[piece_id] = Piece(piece_id, points_of_piece)

    board.remove_dead_cells_from_board(dead_cells)

    return board


def get_round_input():
    if HOME_PC:
        return
    cell_count = int(input())  # number of cells currently occupied by molecules
    for i in range(cell_count):
        molecule_id, x, y = [int(j) for j in input().split()]


def print_move(move):
    piece_id, direction = move
    LU = {"U": "UP", "D": "DOWN", "L": "LEFT", "R": "RIGHT"}
    print(f"{piece_id} {LU[direction]}")


# ********************************************************

board = get_start_parameters("data3")
start_state = board.get_state()
board.print()
solution = board.solve()


board.set_state(start_state)
for move in solution:
    print_move(move)
    get_round_input()
print("0 LEFT")
