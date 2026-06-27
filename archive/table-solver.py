from typing import Any, Tuple
import sys

# ---------------------------------------------------------------------------
# Sample board definitions (optional). Run as: python table-solver.py data1
# If no sample key is provided, the program will read from stdin. The previous
# HOME_PC flag has been removed to make execution environment-agnostic.
# ---------------------------------------------------------------------------
SAMPLES: dict[str, list[str]] = {
    "data1": [
        "+ |  |5 |  ",
        "___________",
        "9 |11|  |  ",
        "___________",
        "  |  |9 |  ",
        "___________",
        "11|  |  |24",
    ],
    "data2": [
        "-  |   |-5 |15 ",
        "_______________",
        "-8 |16 |   |   ",
        "_______________",
        "   |   |   |6  ",
        "_______________",
        "   |   |-6 |   ",
    ],
    "data3": [
        "x    |14   |     |16   |     ",
        "_____________________________",
        "     |     |-25  |80   |     ",
        "_____________________________",
        "     |     |250  |     |     ",
        "_____________________________",
        "     |924  |     |     |5610 ",
        "_____________________________",
        "     |     |     |     |4930 ",
    ],
    "data5": [
        "+    |     |1111 |     |     |-98  |     |     |     |845  ",
        "___________________________________________________________",
        "     |     |4687 |     |     |     |     |     |     |     ",
        "___________________________________________________________",
        "     |     |     |-780 |     |     |     |     |-845 |     ",
        "___________________________________________________________",
        "99   |     |     |     |120  |     |     |     |     |944  ",
        "___________________________________________________________",
        "-123 |     |     |     |     |     |     |6845 |     |     ",
        "___________________________________________________________",
        "     |-1   |     |     |9887 |     |     |     |4000 |     ",
        "___________________________________________________________",
        "     |     |     |487  |     |     |-744 |     |     |     ",
        "___________________________________________________________",
        "     |     |     |     |1230 |     |     |     |     |     ",
    ],
}

Point = Tuple[int, int]
Board = dict[Point, Any]


def get_start_parameters(start_data: str | None = None):
    """Return parsed puzzle components.

    If a sample key (start_data) is provided and exists in SAMPLES, that sample
    is used. Otherwise input is read from stdin. Stdin format supported:
    Either:
        <n>            (first line integer) then n lines follow
    Or: (fallback) all remaining non-empty lines until EOF are used directly.
    """

    # Get Game Start Parameters
    def parse(data):
        data = [line for i, line in enumerate(data) if i % 2 == 0]
        data = [line.strip().split("|") for line in data]
        sign = data[0][0].strip()
        data[0][0] = " "
        data = [[int(x) if x.strip() != "" else "" for x in line] for line in data]

        A = data[0][1:]
        B = [line[0] for line in data[1:]]

        NUM_ROWS = len(data)
        NOW_COLS = len(data[0])

        M = {}
        for r in range(1, NUM_ROWS):
            for c in range(1, NOW_COLS):
                M[(r - 1, c - 1)] = data[r][c]

        return M, sign, A, B, NUM_ROWS - 1, NOW_COLS - 1

    # Choose data source
    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
    else:
        # Attempt to read from stdin
        raw = [line.rstrip("\n") for line in sys.stdin.readlines()]
        raw = [l for l in raw if l.strip() != ""]
        if not raw:
            raise SystemExit("No input provided and no valid sample key supplied.")
        # If first line is an int specifying count, use that many lines
        if raw[0].isdigit():
            n = int(raw[0])
            if len(raw[1:]) < n:
                raise SystemExit("Declared line count less than provided lines.")
            data = raw[1 : 1 + n]
        else:
            data = raw

    return parse(data)


def fill_cell(M, r_ind, c_ind):
    a = A[c_ind]
    b = B[r_ind]
    c = M[(r_ind, c_ind)]
    num_unknowns = sum(x == "" for x in (a, b, c))
    if num_unknowns != 1:
        return ""

    if sign == "+":
        if a == "":
            a = c - b
        if b == "":
            b = c - a
        if c == "":
            c = a + b

    elif sign == "x":
        if a == "":
            a = c // b
        if b == "":
            b = c // a
        if c == "":
            c = a * b

    elif sign == "-":
        if a == "":
            a = c + b
        if b == "":
            b = a - c
        if c == "":
            c = a - b

    A[c_ind] = a
    B[r_ind] = b
    M[(r_ind, c_ind)] = c


def is_complete(M, A, B):
    num_empty = sum(x == "" for x in A)
    if num_empty != 0:
        return False
    num_empty = sum(x == "" for x in B)
    if num_empty != 0:
        return False
    num_empty = sum(x == "" for x in M.values())
    if num_empty != 0:
        return False
    return True


def print_board(M):
    for r in range(NUM_ROWS):
        for c in range(NOW_COLS):
            p = (r, c)
            print(M[p], end=", ")
        print()
    print()


def print_board2(rows, col_width=5, sep="|", divider_char="_"):
    cell_fmt = f"{{:<{col_width}}}"
    for r, row in enumerate(rows):
        line = sep.join(cell_fmt.format(str(v)) for v in row)
        print(line)
        # Only print divider if not the last row
        if r < len(rows) - 1:
            print(divider_char * len(line))


def build_board(M, A, B, sign):
    first_line = [sign] + A
    other_lines = []
    for i in range(NUM_ROWS):
        line = [B[i]]
        for j in range(NOW_COLS):
            line.append(M[(i, j)])
        other_lines.append(line)

    res = [first_line]
    for line in other_lines:
        res.append(line)
    return res


def get_longest_number():
    a = [str(x) for x in A]
    b = [str(x) for x in B]
    c = [str(x) for x in M.values()]
    ALL_NUM = a + b + c
    longest = max(ALL_NUM, key=len)
    return len(longest)


# ********************************************************

if __name__ == "__main__":
    # Select sample key from argv if provided; default to data1 if available.
    sample_key = sys.argv[1] if len(sys.argv) > 1 else "data1"
    if sample_key not in SAMPLES:
        # Treat absence as intent to read stdin (pass None)
        sample_key = None
    M, sign, A, B, NUM_ROWS, NOW_COLS = get_start_parameters(sample_key)

    while not is_complete(M, A, B):
        for r in range(NUM_ROWS):
            for c in range(NOW_COLS):
                fill_cell(M, r, c)

    new_board = build_board(M, A, B, sign)
    longest_len = get_longest_number()
    print_board2(new_board, col_width=longest_len, sep="|", divider_char="_")
