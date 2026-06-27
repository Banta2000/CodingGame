from typing import Any, List, Optional, Callable
from .point_utils import Point

Board = dict  # dict[Point, Any]


# ===== CREATION =====


def create(
    data: List[str],
    skip_chars: Optional[set | str] = None,
    transform: Optional[Callable[[str], Any]] = None,
) -> Board:
    """Create a Board from a list of strings.

    - skip_chars: characters to ignore. Accepts a set or string of chars.
    - transform: optional function char -> value. If None, store the raw char.
    """
    if skip_chars is None:
        skip_set: set = set()
    elif isinstance(skip_chars, str):
        skip_set = set(skip_chars)
    else:
        skip_set = skip_chars

    board: Board = {}
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char in skip_set:
                continue
            board[Point(r, c)] = transform(char) if transform is not None else char

    return board


def create_empty(num_rows: int, num_cols: int, default_value: Any = None) -> Board:
    """Create a Board filled with default_value."""
    return {Point(r, c): default_value for r in range(num_rows) for c in range(num_cols)}


# ===== DIMENSIONS =====


def num_rows(board: Board) -> int:
    """Return the number of rows (max row index + 1)."""
    return max(p.row for p in board) + 1 if board else 0


def num_cols(board: Board) -> int:
    """Return the number of columns (max col index + 1)."""
    return max(p.col for p in board) + 1 if board else 0


# ===== SEARCH =====


def find(board: Board, value: Any) -> List[Point]:
    """Return all positions where the board has the given value."""
    return [pos for pos, val in board.items() if val == value]


# ===== PRINTING =====


def print_board(board: Board, visited=None) -> None:
    """Print the board. Positions in visited are highlighted in red."""
    if visited is None:
        visited = set()

    RESET = "\x1b[0m"
    RED = "\033[91m"

    rows = num_rows(board)
    cols = num_cols(board)
    for r in range(rows):
        line_chars: List[str] = []
        for c in range(cols):
            p = Point(r, c)
            if p in visited and p in board:
                line_chars.append(RED + str(board[p]) + RESET)
            elif p in board:
                line_chars.append(str(board[p]))
            else:
                line_chars.append(" ")
        print("".join(line_chars))
