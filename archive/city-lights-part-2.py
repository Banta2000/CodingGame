from dataclasses import dataclass

Point = tuple[int, int, int]

SAMPLES = {
    "data1": [["...", ".3.", "...", "..."], ["...", "...", "...", ".2."]],
    "data2": [["....", ".2.."], ["....", "...."], ["....", "...."], ["..3.", "...."]],
    "data8": [
        ["..2.", "....", "..3.", "....", ".5.6"],
        ["...D", "....", ".11.", ".1..", "...."],
        [".J..", "....", "....", "....", "...."],
        ["2...", "33..", "....", "...2", ".22."],
        ["5...", ".6..", "...2", "....", ".1.."],
        ["....", "....", "....", "...1", ".654"],
    ],
}


@dataclass
class LightSource:
    pos: Point
    val: str


CHAR_TO_NUM = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 18,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "O": 24,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "U": 30,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
}


NEXT_CHAR = {
    ".": "0",
    "0": "1",
    "1": "2",
    "2": "3",
    "3": "4",
    "4": "5",
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
    "9": "A",
    "A": "B",
    "B": "C",
    "C": "D",
    "D": "E",
    "E": "F",
    "F": "G",
    "G": "H",
    "H": "I",
    "I": "J",
    "J": "K",
    "K": "L",
    "L": "M",
    "M": "N",
    "N": "O",
    "O": "P",
    "P": "Q",
    "Q": "R",
    "R": "S",
    "S": "T",
    "T": "U",
    "U": "V",
    "V": "W",
    "W": "X",
    "X": "Y",
    "Y": "Z",
    "Z": "Z",
}


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        light_sources = []
        for layer_num, layer in enumerate(data):
            for row_num, line in enumerate(layer):
                for col_num, char in enumerate(line):
                    p = (layer_num, row_num, col_num)
                    if char != ".":
                        ls = LightSource(pos=p, val=char)
                        light_sources.append(ls)

        layers = len(data)
        rows = len(data[0])
        cols = len(data[0][0])
        board = []
        for _ in range(layers):
            board.append([["0" for _ in range(cols)] for _ in range(rows)])

        return light_sources, board

    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
    else:
        num_cols = int(input())
        num_rows = int(input())
        num_layers = int(input())
        num_lines = int(input())

        all_lines = [input() for _ in range(num_lines)]
        data = []
        for i in range(num_layers):
            t = all_lines[i * (num_rows + 1) : i * (num_rows + 1) + num_rows]
            data.append(t)

    return parse(data)


def euclidian_dist(p1: Point, p2: Point) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5


def shine_light(board, ls: LightSource):
    value = CHAR_TO_NUM[ls.val]
    for l in range(len(board)):
        for r in range(len(board[0])):
            for c in range(len(board[0][0])):
                p = (l, r, c)
                dist = round(euclidian_dist(p, ls.pos))
                if 0 <= dist <= value:
                    strenght = value - dist
                    original_value = board[l][r][c]
                    for _ in range(strenght):
                        original_value = NEXT_CHAR[original_value]
                    board[l][r][c] = original_value


def print_board(board):
    num_layers = len(board)
    for i, layer in enumerate(board):
        for row in layer:
            print("".join(row))
        if i != num_layers - 1:
            print()


# ********************************************************

light_sources, board = get_start_parameters("data1")
for ls in light_sources:
    shine_light(board, ls)

print_board(board)
