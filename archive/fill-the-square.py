from cgutils.coding_game_helper import CodingGameHelper


def pb(i: int):
    # Prints the board form of a integer
    s = int_to_board(i)
    for line in s:
        print(line)
    print()


def read_input(CGH: CodingGameHelper) -> list[str]:
    n = int(CGH.input())
    lines = [CGH.input() for _ in range(n)]
    return lines


def board_to_int(lines: list[str]) -> int:
    s = "".join(lines)
    return int(s.replace(".", "0").replace("*", "1"), 2)


def int_to_str(i: int) -> str:
    # Converts int into a binary / string "...*.*.."
    b = bin(i)[2:].zfill(LEN_BOARD)
    return b.replace("0", ".").replace("1", "*")


def int_to_board(i: int) -> list[str]:
    # Converts a integer into a lines of "..*.."
    b = int_to_str(i)
    lines = str_to_lines(b)
    return lines


def str_to_lines(b: str) -> list:
    res = []
    for i in range(NUM_ROWS):
        s = b[i * NUM_COLS : (i + 1) * NUM_COLS]
        res.append(s)
    return res


def create_button_and_effect(row: int, col: int, NUM_ROWS, NUM_COLS, LEN_BOARD):
    effect = 0
    for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < NUM_ROWS and 0 <= nc < NUM_COLS:
            pos = nr * NUM_COLS + nc
            effect |= 1 << (LEN_BOARD - 1 - pos)
    return effect


def create_button_map(NUM_ROWS, NUM_COLS, LEN_BOARD):
    BUTTON_MAP = dict()

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            effect = create_button_and_effect(row, col, NUM_ROWS, NUM_COLS, LEN_BOARD)
            BUTTON_MAP[row * NUM_COLS + col] = effect
    return BUTTON_MAP


def parse_input(lines: list):
    NUM_ROWS = len(lines)
    NUM_COLS = len(lines[0])
    LEN_BOARD = NUM_ROWS * NUM_COLS
    BOARD = board_to_int(lines)
    BUTTON_MAP = create_button_map(NUM_ROWS, NUM_COLS, LEN_BOARD)
    return BOARD, BUTTON_MAP, NUM_ROWS, NUM_COLS, LEN_BOARD


def get_candidates(curr, idx):
    # checks all buttons moving forward from idx and returns the one button that lights up a cell above it
    for i in range(idx, len(ALL_BUTTONS)):
        # check if button above is not lit
        if (curr & ABOVE_CELL_MASK[i]) == 0:
            return [i]
    return []


def dfs(curr, path, idx):
    if curr == TARGET:
        return list(path)

    # Since we now handle the first row in a loop outside,
    # dfs only needs to handle "chasing the lights" for rows 1 to N-1.
    candidates = get_candidates(curr, idx)

    for i in candidates:
        path.append(i)
        new_board = curr ^ BUTTON_MAP[i]
        res = dfs(new_board, path, i + 1)
        if res is not None:
            return res
        path.pop()
    return None


def print_result(buttons, NUM_ROWS, NUM_COLS, CGH):
    res = ["."] * (NUM_COLS * NUM_ROWS)
    for button in buttons:
        res[button] = "X"
    
    for r in range(NUM_ROWS):
        line = "".join(res[r * NUM_COLS : (r + 1) * NUM_COLS])
        print(line)
        CGH.add_output_line(line)


def create_cell_mask(NUM_ROWS, NUM_COLS, LEN_BOARD):
    # Returns a lookup table, for a given button, which cell is above it in binary form
    ABOVE_CELL_MASK = []
    for i in range(LEN_BOARD):
        button_above = i - NUM_COLS
        if button_above >= 0:
            ABOVE_CELL_MASK.append(1 << (LEN_BOARD - 1 - button_above))
        else:
            ABOVE_CELL_MASK.append(0)
    return ABOVE_CELL_MASK


# ********************************************************

CGH = CodingGameHelper(4, __file__)
lines = read_input(CGH)
BOARD, BUTTON_MAP, NUM_ROWS, NUM_COLS, LEN_BOARD = parse_input(lines)
ALL_BUTTONS = [num for num in range(NUM_ROWS * NUM_COLS)]
ABOVE_CELL_MASK = create_cell_mask(NUM_ROWS, NUM_COLS, LEN_BOARD)
TARGET = (1 << LEN_BOARD) - 1

# Instead of calling dfs once, we loop through all 2^N first-row combinations.
# 1 << NUM_COLS is a bitwise way to calculate 2^NUM_COLS.
# For example, if NUM_COLS is 3, 1 << 3 (binary 1000) is 8.
# This loop lets us try every possible "on/off" pattern for the first row buttons.
final_buttons = None
for i in range(1 << NUM_COLS):
    temp_board = BOARD
    initial_path = []
    for col in range(NUM_COLS):
        # 'i >> position' moves the bit we want to the very end (index 0).
        # '& 1' then reads only that last bit (returning 1 if set, 0 if not).
        if (i >> (NUM_COLS - 1 - col)) & 1:
            temp_board ^= BUTTON_MAP[col]
            initial_path.append(col)

    res = dfs(temp_board, initial_path, NUM_COLS)
    if res is not None:
        final_buttons = res
        break

if final_buttons:
    print_result(final_buttons, NUM_ROWS, NUM_COLS, CGH)
CGH.assert_output()
