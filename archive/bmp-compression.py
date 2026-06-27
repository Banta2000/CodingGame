from typing import Any, Tuple, List
from cgutils import Board, Point2D

SAMPLES: dict[str, list[str]] = {
    "data1": ["....#", "...#.", "#.#..", ".#..."],
    "data2": ["...", "..#", "..."],
    "data3": ["###", "###", "###", "###", "###"],
    "data4": [
        "...........................................",
        "...................#######.................",
        "..............#####.......#####............",
        "...........###.................###.........",
        ".........##.......................##.......",
        ".......##..........................###.....",
        "......##.............................##....",
        ".....##........##..........###........##...",
        "....##........####........#####.......##...",
        "....##..........#...........#..........##..",
        "....##.................................##..",
        "....##.................................##..",
        "....##.................................##..",
        "....##........##.............##.......##...",
        ".....##........##...........###.......##...",
        "......##........###.......###........##....",
        ".......###.........#######.........###.....",
        ".........##......................###.......",
        "...........###.................###.........",
        "..............######.....######............",
        "....................#####..................",
        "...........................................",
        "...........................................",
    ],
    #
    # ,
    # "data4": ,
    # "data5": ,
    # "data6": ,
}


def break_table_in_squares(board: Board) -> List[Board]:
    new_dimensions = cut_in_squares(board.num_rows, board.num_cols)
    if len(new_dimensions) == 4:
        h1, w1 = new_dimensions[0]
        h2, w2 = new_dimensions[1]
        h3, w3 = new_dimensions[2]
        h4, w4 = new_dimensions[3]
        b1 = board.get_subboard(Point2D(0, 0), h1, w1)
        b2 = board.get_subboard(Point2D(0, w1), h2, w2)
        b3 = board.get_subboard(Point2D(h1, 0), h3, w3)
        b4 = board.get_subboard(Point2D(h1, w1), h4, w4)
        return [b1, b2, b3, b4]

    if len(new_dimensions) == 2:
        h1, w1 = new_dimensions[0]
        h2, w2 = new_dimensions[1]
        if board.num_rows == 1:
            # Vertical cut
            b1 = board.get_subboard(Point2D(0, 0), h1, w1)
            b2 = board.get_subboard(Point2D(0, w1), h2, w2)
        else:
            # Horizontal cut
            b1 = board.get_subboard(Point2D(0, 0), h1, w1)
            b2 = board.get_subboard(Point2D(h1, 0), h2, w2)
        return [b1, b2]

    # If no valid cut, return an empty list
    return []


def cut_in_squares(H, W) -> list[Tuple[int, int]]:
    # Received the heights and widths of the image
    # Returns [(h1, w1), (h2, w2), ...] the sizes of the four squares to cut
    # if the width and height of the area are even, the cutting lines cut at
    # the middle of the sides. If the width is odd, the left side sub-areas will
    # have one pixel wider than the right sub-areas. If the height is odd,
    # the upper sub-areas will have one pixel taller than the lower sub-areas.
    # If the area to be decomposed has only one row of pixels, horizontal cut is
    # skipped. Do only the vertical cut. If the area has only one column of pixels,
    # vertical cut is skipped. Do only the horizontal cut.
    if H > 1 and W > 1:
        # Normal case
        h1 = H // 2 if H % 2 == 0 else (H // 2) + 1
        w1 = W // 2 if W % 2 == 0 else (W // 2) + 1
        h2 = h1
        w2 = W - w1
        h3 = H - h1
        w3 = w1
        h4 = h3
        w4 = w2
        return [(h1, w1), (h2, w2), (h3, w3), (h4, w4)]

    if W == 1 and H > 1:
        # Only horizontal cut
        h1 = H // 2 if H % 2 == 0 else (H // 2) + 1
        w1 = 1
        h2 = H - h1
        w2 = 1
        return [(h1, w1), (h2, w2)]

    if H == 1 and W > 1:
        # Only vertical cut
        h1 = 1
        w1 = W // 2 if W % 2 == 0 else (W // 2) + 1
        h2 = 1
        w2 = W - w1
        return [(h1, w1), (h2, w2)]

    if H == 1 and W == 1:
        return [(1, 1)]

    raise ValueError("Invalid dimensions")


def all_one_color(board) -> int:
    # Return 0 if all pixels are ".", 1 if all pixels are "#", -1 if mixed
    values = set(board.values())
    if len(values) == 1:
        if "." in values:
            return "0"
        if "#" in values:
            return "1"
    return -1


def encode_board(board):
    containing_color = all_one_color(board)
    if containing_color in ["0", "1"]:
        RESULT.append(containing_color)
        return

    RESULT.append("+")
    sub_boards = break_table_in_squares(board)
    for sb in sub_boards:
        encode_board(sb)


def decode_board(encoded_string: str, board: Board) -> None:
    # Decode the encoded string and fill the board accordingly
    stack = [((0, 0), board.num_rows, board.num_cols)]
    i = -1
    while stack:
        i += 1
        ins = encoded_string[i]
        anchor_point, h, w = stack.pop()
        if ins in ["0", "1"]:
            fill_char = "." if ins == "0" else "#"
            board.fill_subboard(anchor_point, fill_char)
            continue
        if ins == "+":
            new_dimensions = cut_in_squares(h, w)
            if len(new_dimensions) == 4:
                h1, w1 = new_dimensions[0]
                ap1 = (anchor_point[0], anchor_point[1])
                h2, w2 = new_dimensions[1]
                ap2 = (anchor_point[0], anchor_point[1] + w1)
                h3, w3 = new_dimensions[2]
                ap3 = (anchor_point[0] + h1, anchor_point[1])
                h4, w4 = new_dimensions[3]
                ap4 = (anchor_point[0] + h1, anchor_point[1] + w1)
                stack.append((ap4, h4, w4))
                stack.append((ap3, h3, w3))
                stack.append((ap2, h2, w2))
                stack.append((ap1, h1, w1))
            elif len(new_dimensions) == 2:
                h1, w1 = new_dimensions[0]
                h2, w2 = new_dimensions[1]
                if h == 1:
                    # Vertical cut
                    ap1 = (anchor_point[0], anchor_point[1])
                    ap2 = (anchor_point[0], anchor_point[1] + w1)
                else:
                    # Horizontal cut
                    ap1 = (anchor_point[0], anchor_point[1])
                    ap2 = (anchor_point[0] + h1, anchor_point[1])
                stack.append((ap2, h2, w2))
                stack.append((ap1, h1, w1))
            else:
                raise ValueError("Invalid cut dimensions")


def get_start_parameters(start_data: str | None = None):
    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
    else:
        inputs = input().split()
        mode = inputs[0]
        cols = int(inputs[1])
        rows = int(inputs[2])
        lines = int(input())
        data = [input() for _ in range(lines)]

    board = Board()
    if mode == "B":
        board.load_data(data)
        return mode, board, ""

    elif mode == "C":
        board.create_empty(rows, cols, ".")
        encoded_str = "".join(data)
        return mode, board, encoded_str


# ********************************************************

RESULT = []
# mode, board, encoded_str = get_start_parameters("data1")

encoded_str = "+++00+0++01000+1++1011+10+++0001+01+01010++010++100+10+++10100+10+1011+01++01011+0+++100+100000++++01+0100+1000+11+10100++++0+0111++011++10000++101++0101+01++1011111+1110+00++100000+++1+1011++101+11010+1000++01011+01011+++011+1011+00+++100++100+011+++1011+100++0+++011++0110++1000+0011++++01+0101++011++01+0101++011++01011+00+1100+10+01+10+10+0+01010+0100+00++0011+0100++01+0100++++1110000+++100++10000+00+1100+10+00+10+10+00+0011+00+100+00++0011+0100++01+0100++10100+10000"
board = Board()
board.create_empty(42, 19, ".")
mode = "C"

if mode == "B":
    encode_board(board)
    res_str = "".join(RESULT)

    num_lines = (len(res_str) + 49) // 50
    res = []
    for i in range(num_lines):
        res.append(res_str[i * 50 : (i + 1) * 50])

    print(" ".join(["C", str(board.num_cols), str(board.num_rows)]))
    print(num_lines)

    for x in res:
        print(x)

elif mode == "C":
    decode_board(encoded_str, board)
    print(" ".join(["B", str(board.num_cols), str(board.num_rows)]))
    print(board.num_rows)
    board.print()
