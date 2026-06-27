import sys
import os
from typing import Any, Tuple


# HOME_PC: bool = os.getenv("HOME_PC") == "true"
HOME_PC = True


# Console friendly print
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


class SUDOKU:
    FULL_SET = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    def __init__(self, init_string_list: list[str]):
        self.board = [[int(x) for x in line] for line in init_string_list]
        self.lookup = [[None for _ in range(16)] for _ in range(9)]
        self._update_lookup()

    # Returns the available letters for a given position looking horizontally, vertically and in the quadrant; if the field is not empty, returns None
    def _calculate_available_letters_of_a_pos(self, row: int, col: int) -> set[str]:
        if self.board[row][col] != 0:
            return None
        row_letters = set(self.board[row])
        col_letters = set(self.board[r][col] for r in range(9))
        min_row, min_col = (row // 3) * 3, (col // 3) * 3
        quadrant_letters = {self.board[r][c] for r in range(min_row, min_row + 3) for c in range(min_col, min_col + 3)}
        res = row_letters | col_letters | quadrant_letters
        res.discard(".")
        return SUDOKU.FULL_SET - res

    # Updates self.lookup with the available letters for each field
    def _update_lookup(self) -> None:
        for row in range(9):
            for col in range(9):
                self.lookup[row][col] = self._calculate_available_letters_of_a_pos(row, col)

    # Sets a given field to a value; updates the lookup
    def set_field(self, row: int, col: int, letter: str) -> None:
        self.board[row][col] = letter
        self._update_lookup()

    # Sets a given field to "."; updates the lookup
    def remove_field(self, row: int, col: int) -> None:
        self.board[row][col] = 0
        self._update_lookup()

    # Returns the letter options for a given row and col
    def get_letter_options(self, row, col):
        return self.lookup[row][col]

    # Returns list of [row, col, set(letter_options)] sorted by the number of options
    def get_pos_options(self):
        res = []
        for row, line in enumerate(self.lookup):
            for col, char in enumerate(line):
                if char is not None:
                    res.append((row, col, self.get_letter_options(row, col)))
        res.sort(key=lambda x: len(x[2]))
        return res

    # Returns number of missing fields
    def count_missing_fields(self):
        return sum([line.count(0) for line in self.board])

    # Prints the board
    def print_board(self, r=None, c=None) -> None:
        RESETCOL = "\x1b[0m"
        for row, line in enumerate(self.board):
            for col, char in enumerate(line):
                if r == row or c == col:
                    color = "\033[91m"
                else:
                    color = "\x1b[0m"
                if HOME_PC:
                    myPrint(color + char + RESETCOL, end="")
                else:
                    myPrint(char, end="")
            myPrint()
        myPrint()
        myPrint()

    # Inserts all single letters, returns True if something was inserted
    def insert_single_letters(self):
        # Inserts letters that appear only once in a given row
        def _insert_single_letters_in_selection(selection):
            counter = {letter: 0 for letter in SUDOKU.FULL_SET}
            lastpos = {letter: None for letter in SUDOKU.FULL_SET}
            for row, col in selection:
                for letter in self.lookup[row][col]:
                    counter[letter] += 1
                    lastpos[letter] = (row, col)
            for letter, count in counter.items():
                if count == 1:
                    row, col = lastpos[letter]
                    self.set_field(row, col, letter)

        made_a_change = True
        while made_a_change:

            # Count number of filled out fields
            filled_out_start = sum([line.count(0) for line in self.board])

            # Inserts all single letters that are clear
            for row in range(9):
                for col in range(9):
                    if self.lookup[row][col] and len(self.lookup[row][col]) == 1:
                        self.set_field(row, col, self.lookup[row][col].pop())

            # Inserts letters that appear only once in a given row
            for row in range(9):
                selection = [(row, col) for col in range(9) if self.board[row][col] == 0]
                _insert_single_letters_in_selection(selection)

            # Inserts letters that appear only once in a given col
            for col in range(9):
                selection = [(row, col) for row in range(9) if self.board[row][col] == 0]
                _insert_single_letters_in_selection(selection)

            # Inserts letters that appear only once in a given quadrant
            for row in [0, 3, 6]:
                for col in [0, 3, 6]:
                    selection = [
                        (r, c) for r in range(row, row + 3) for c in range(col, col + 3) if self.board[r][c] == 0
                    ]
                    _insert_single_letters_in_selection(selection)

            # Count number of filled out fields
            filled_out_end = sum([line.count(0) for line in self.board])

            made_a_change = filled_out_start != filled_out_end

    # Solve the puzzle
    def solve(self):

        board_copy = [line.copy() for line in self.board]

        self.insert_single_letters()

        if self.count_missing_fields() == 0:
            for line in self.board:
                print("".join([str(x) for x in line]))
            return True

        next_pos_options = self.get_pos_options()
        row, col, letter_options = next_pos_options[0]
        for letter in letter_options:
            self.set_field(row, col, letter)
            if self.solve():
                return True

        self.board = board_copy
        self._update_lookup()
        return False


# Return the input based on the environment
def load_input(case):
    def load_test_case(case):
        test1 = [
            "120070560",
            "507932080",
            "000001000",
            "010240050",
            "308000402",
            "070085010",
            "000700000",
            "080423701",
            "034010028"
        ]

        if case == "test1":
            return test1

    if HOME_PC:
        grid = load_test_case(case)

    else:
        grid = []
        for _ in range(9):
            grid.append(input())
    game = SUDOKU(grid)
    return game


# ************************************************************************************

game = load_input("test1")
game.solve()
