HOME_PC = 1

import sys


def printBoard():
    for r in range(rowNum):
        line = ""
        for c in range(colNum):
            p = (r, c)
            line += board[p]
        line = line.rstrip()
        print(line)


def extract_landmarks():
    landmarks = {}
    lookUp = {
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
    }
    for r in range(rowNum):
        for c in range(colNum):
            p = (r, c)
            c = board[p]
            if c != ".":
                c = lookUp[c]
                landmarks[c] = p
    return landmarks


def get_test_input():
    data = [
        "......1.........................",
        "................................",
        "................................",
        "................................",
        "............VU..................",
        "......3....2....................",
        "......4....5....................",
        "................................",
        "................................",
        ".............T..................",
        "................................",
        "..7...6.........................",
        ".....A..B.......................",
        ".................S.....R........",
        "........................Q......P",
        "......8.9..C.....D.......N....O.",
        "................................",
        "................FE..............",
        "................................",
        "..................GJ............",
        "...................K............",
        "................HI..............",
        ".................LM.............",
    ]
    return data


def create_board(data):
    board = {}
    for r in range(rowNum):
        for c in range(colNum):
            p = (r, c)
            c = data[r][c]
            board[p] = c
    return board


def myPrint(lst):
    print("Debug messages...", lst, file=sys.stderr, flush=True)


def draw_line(p1, p2):
    p1, p2 = sorted([p1, p2])
    r1, c1 = p1
    r2, c2 = p2

    # Horizontal line
    if r1 == r2:
        for c in range(c1 + 1, c2):
            if board[(r1, c)] == ".":
                board[(r1, c)] = "-"
            elif board[(r1, c)] == "|":
                board[(r1, c)] = "+"
            else:
                board[(r1, c)] = "*"

    # Vertical line
    elif c1 == c2:
        for r in range(r1 + 1, r2):
            if board[(r, c1)] == ".":
                board[(r, c1)] = "|"
            elif board[(r, c1)] == "-":
                board[(r, c1)] = "+"
            else:
                board[(r, c1)] = "*"

    # Diagonal line
    else:

        # Diagonal \
        if c1 < c2:
            for r, c in zip(range(r1 + 1, r2), range(c1 + 1, c2)):
                if board[(r, c)] == ".":
                    board[(r, c)] = "\\"
                elif board[(r, c)] == "/":
                    board[(r, c)] = "X"
                else:
                    board[(r, c)] = "*"

        if c2 < c1:
            for r, c in zip(range(r1 + 1, r2), reversed(range(c2 + 1, c1))):
                if board[(r, c)] == ".":
                    board[(r, c)] = "/"
                elif board[(r, c)] == "\\":
                    board[(r, c)] = "x"
                else:
                    board[(r, c)] = "*"


# ********************************************************

if HOME_PC:
    data = get_test_input()
else:
    data = []
    h, w = [int(i) for i in input().split()]
    for i in range(h):
        row = input()
        data.append(row)

rowNum = len(data)
colNum = len(data[0])
board = create_board(data)

landmarks = extract_landmarks()
num_landmarks = len(landmarks)

for i in range(1, num_landmarks):
    p1 = landmarks[i]
    p2 = landmarks[i + 1]
    draw_line(p1, p2)

for _, landmark_point in landmarks.items():
    board[landmark_point] = "o"

for k, v in board.items():
    if v == ".":
        board[k] = " "

printBoard()
