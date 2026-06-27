from typing import Any, Tuple, List, Optional, Callable


# This class is deprecated, I should not use it.
# Instead, I should use the Board class in board_utils.py, which is more powerful and flexible.


class Board:
    def __init__(self) -> None:
        """Initializes an empty board. Data needs to be loaded later."""
        self.board: dict[Point2D, Any] = {}
        self.num_rows: int = 0
        self.num_cols: int = 0

    def load_data(
        self,
        data: List[str],
        skip_chars: Optional[set[str] | str] = None,
        transform: Optional[Callable[[str], Any]] = None,
    ) -> None:
        """Load an ASCII board from a list of strings.

        - skip_chars: characters to ignore (not stored). Accepts a set or a string of chars. board.load_data(lines, skip_chars='.')
        - transform: optional function char -> value. If None, store the raw char. Can be used with mapping dict. board.load_data(lines, transform=CHAR_TO_NUM.get)
        """
        board: dict[Point2D, Any] = {}
        # Normalize skip set
        if skip_chars is None:
            skip_set: set[str] = set()
        elif isinstance(skip_chars, str):
            skip_set = set(skip_chars)
        else:
            skip_set = skip_chars

        for r, line in enumerate(data):
            for c, char in enumerate(line):
                if char in skip_set:
                    continue
                p = Point2D(r, c)
                board[p] = transform(char) if transform is not None else char

        self.board = board
        # Preserve the original rectangular dimensions based on input lines
        if data:
            self.num_rows = len(data)
            self.num_cols = max(len(line) for line in data)
        else:
            self.num_rows = 0
            self.num_cols = 0

    def create_empty(self, num_rows: int, num_cols: int, default_value: Any = None) -> None:
        """Create an empty board with given dimensions, filled with default_value."""
        self.board = {}
        for r in range(num_rows):
            for c in range(num_cols):
                self.board[Point2D(r, c)] = default_value
        self.num_rows = num_rows
        self.num_cols = num_cols

    def print(self, visited=None) -> None:
        """Print the board. If visited is given, can print visited positions in red."""
        if visited is None:
            visited = set()
        board = self.board

        RESETCOL = "\x1b[0m"
        RED = "\033[91m"

        for r in range(self.num_rows):
            line_chars: List[str] = []
            for c in range(self.num_cols):
                p = Point2D(r, c)
                if p in visited and p in board:
                    line_chars.append(RED + str(board[p]) + RESETCOL)
                elif p in board:
                    line_chars.append(str(board[p]))
                else:
                    line_chars.append(" ")
            print("".join(line_chars))

    def __getitem__(self, key: "Point2D | tuple[int, int]") -> Any:
        """Get the character at a specific position. Accepts Point2D or 2D tuple."""
        if isinstance(key, tuple) and len(key) == 2:
            key = Point2D(*key)
        if key not in self.board:
            raise KeyError(f"Key {key} not found in board.")
        return self.board[key]

    def __setitem__(self, key: "Point2D | tuple[int, int]", value: Any) -> None:
        """Set the character at a specific position. Accepts Point2D or 2D tuple."""
        if isinstance(key, tuple) and len(key) == 2:
            key = Point2D(*key)
        self.board[key] = value
        # Update num_rows and num_cols if necessary
        self.num_rows = max(self.num_rows, key.row + 1)
        self.num_cols = max(self.num_cols, key.col + 1)

    def __contains__(self, key: "Point2D | tuple[int, int]") -> bool:
        """Check if a position exists on the board. Accepts Point2D or 2D tuple."""
        if isinstance(key, tuple) and len(key) == 2:
            key = Point2D(*key)
        return key in self.board

    def find(self, value: Any) -> List[Point2D]:
        """Returns a list of Point2D where the board has the given value."""
        return [pos for pos, val in self.board.items() if val == value]

    # ------ Mapping-like helpers ------
    def items(self):
        """Iterate over (Point2D, value) pairs like a dict."""
        return self.board.items()

    def keys(self):
        """Iterate over Point2D keys like a dict."""
        return self.board.keys()

    def values(self):
        """Iterate over cell values like a dict."""
        return self.board.values()

    def get(self, key: "Point2D | tuple[int, int]", default: Any = None) -> Any:
        """Safe get with optional (row, col) tuple support."""
        if isinstance(key, tuple) and len(key) == 2:
            key = Point2D(*key)
        return self.board.get(key, default)

    def __iter__(self):
        """Iterate over Point2D keys."""
        return iter(self.board)

    def __len__(self) -> int:
        return len(self.board)

    # ------ Sub-board extraction ------
    def get_subboard(
        self,
        anchor: "Point2D | tuple[int, int]",
        height: int,
        width: int,
    ) -> "Board":
        """Return a new Board containing the rectangular region anchored at `anchor`
        with dimensions `height` x `width`. The returned board's coordinates are
        normalized so that `anchor` maps to (0, 0)."""
        if isinstance(anchor, tuple) and len(anchor) == 2:
            anchor = Point2D(*anchor)

        # Handle non-positive dimensions by returning an empty board
        if height <= 0 or width <= 0:
            return Board()

        r0, c0 = anchor.row, anchor.col
        r1, c1 = r0 + height, c0 + width

        sub = Board()
        for p, val in self.board.items():
            if r0 <= p.row < r1 and c0 <= p.col < c1:
                sub.board[Point2D(p.row - r0, p.col - c0)] = val

        sub.num_rows = height
        sub.num_cols = width
        return sub

    def fill_subboard(
        self,
        anchor: "Point2D | tuple[int, int]",
        default_value: Any = None,
    ) -> None:
        """Fill a rectangular region of this board with default_value."""
        if isinstance(anchor, tuple) and len(anchor) == 2:
            anchor = Point2D(*anchor)
        r0, c0 = anchor.row, anchor.col
        r1, c1 = r0 + self.num_rows, c0 + self.num_cols
        for r in range(r0, r1):
            for c in range(c0, c1):
                self.board[Point2D(r, c)] = default_value
