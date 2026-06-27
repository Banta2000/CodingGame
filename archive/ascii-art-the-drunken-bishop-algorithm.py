from typing import Any, Tuple, List

SAMPLES: dict[str, str] = {
    "data1": "fc:94:b0:c1:e5:b0:98:7c:58:43:99:76:97:ee:9f:b7",
    "data2": "51:8e:d2:95:25:73:8c:eb:da:c4:9c:49:e6:0e:a9:d3",
    "data3": "00:00:00:00:00:00:00:00:ff:ff:ff:ff:ff:ff:ff:ff",
}

INT_TO_CHAR = {
    0: " ",
    1: ".",
    2: "o",
    3: "+",
    4: "=",
    5: "*",
    6: "B",
    7: "O",
    8: "X",
    9: "@",
    10: "%",
    11: "&",
    12: "#",
    13: "/",
    14: "^",
}


def get_start_parameters(start_data: str | None = None):
    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
    else:
        data = input()
    return data


def str_to_directions(s: str) -> List[str]:
    BIN_TO_DIR = {"00": "NW", "01": "NE", "10": "SW", "11": "SE"}
    s1 = s.split(":")

    ins = []
    for byte in s1:
        a = int(byte, 16)
        a = f"{a:08b}"
        a = [a[n : n + 2] for n in range(0, 8, 2)]
        a.reverse()
        a = [BIN_TO_DIR[x] for x in a]
        ins += a
    return ins


def move_player(player: tuple[int, int], dir: str) -> tuple[int, int]:
    r, c = player
    if dir == "NW":
        r -= 1
        c -= 1
    elif dir == "NE":
        r -= 1
        c += 1
    elif dir == "SW":
        r += 1
        c -= 1
    elif dir == "SE":
        r += 1
        c += 1

    if r < 0:
        r = 0
    if r > 8:
        r = 8
    if c < 0:
        c = 0
    if c > 16:
        c = 16

    return (r, c)


def print_board(board, start_pos, end_pos):
    print("+---[CODINGAME]---+")
    for r in range(9):
        print("|", end="")
        for c in range(17):
            p = r, c
            if p == start_pos:
                print("S", end="")
            elif p == end_pos:
                print("E", end="")
            else:
                val = board[p] % len(INT_TO_CHAR)
                c = INT_TO_CHAR[val]
                print(c, end="")
        print("|")
    print("+-----------------+")


# ********************************************************


orig_str = get_start_parameters("data3")
instructions = str_to_directions(orig_str)
board = {(r, c): 0 for r in range(9) for c in range(17)}
start_pos = (4, 8)
player = start_pos
for ins in instructions:
    board[player] += 1
    player = move_player(player, ins)
print(instructions)
print_board(board, start_pos, player)
