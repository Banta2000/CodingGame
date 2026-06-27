HOME_PC = 1
import sys


def myPrint(*args):
    print(*args, file=sys.stderr, flush=True)


def get_input():
    if HOME_PC:
        # n = 15
        # myInput = ["..oo.o..", ".oo....o", "o..o..oo", "..o.....", "...o.o..", "..o.o...", ".o.o.oo.", "o.oo...."]

        n = 3
        myInput = ["....", "o...", "..oo"]

        # n = 9
        # myInput = ["..o.o..", "ooo.o.o", "..oo.o.", "oo.o.oo", "..oo.o."]

    else:
        n = int(input())
        h, w = [int(i) for i in input().split()]
        myInput = []
        for i in range(h):
            myInput.append(input())

    return n, myInput, len(myInput), len(myInput[0])


def create_map(lst):
    board = {}
    for row in range(MAX_ROW):
        for col in range(MAX_COL):
            board[(row, col)] = lst[row][col]
    return board


def get_possible_directions(board, p):
    r, c = p
    pN1, pN2 = (r - 1, c), (r - 2, c)
    pS1, pS2 = (r + 1, c), (r + 2, c)
    pE1, pE2 = (r, c + 1), (r, c + 2)
    pW1, pW2 = (r, c - 1), (r, c - 2)

    result = []

    if pN1 in board and pN2 in board and board[pN1] in [".", "|"] and board[pN2] in [".", "o"]:
        result.append("N")
    if pS1 in board and pS2 in board and board[pS1] in [".", "|"] and board[pS2] in [".", "o"]:
        result.append("S")
    if pE1 in board and pE2 in board and board[pE1] in [".", "-"] and board[pE2] in [".", "o"]:
        result.append("E")
    if pW1 in board and pW2 in board and board[pW1] in [".", "-"] and board[pW2] in [".", "o"]:
        result.append("W")
    return result


def printBoard(board, dumbbells):
    flat_dumbbells = flatten_dumbbells(dumbbells)

    for row in range(MAX_ROW):
        for col in range(MAX_COL):
            p = (row, col)
            if p in flat_dumbbells:
                print(flat_dumbbells[p], end="")
            else:
                print(board[p], end="")
        print()


def printDumbbells(dumbbells):
    flat_dumbbells = flatten_dumbbells(dumbbells)
    for row in range(MAX_ROW):
        for col in range(MAX_COL):
            p = (row, col)
            if p in flat_dumbbells:
                print(flat_dumbbells[p], end="")
            else:
                print(".", end="")
        print()


def get_circles(board):
    return [p for p in board if board[p] == "o"]


def get_three_points_in_direction(p, direction):
    r, c = p
    pN1, pN2 = (r - 1, c), (r - 2, c)
    pS1, pS2 = (r + 1, c), (r + 2, c)
    pE1, pE2 = (r, c + 1), (r, c + 2)
    pW1, pW2 = (r, c - 1), (r, c - 2)

    lookUp = {"N": (p, pN1, pN2), "S": (p, pS1, pS2), "E": (p, pE1, pE2), "W": (p, pW1, pW2)}
    result = lookUp[direction]

    return result


def solve_dumbbell_in_direction(board, dumbbells, p, direction):
    db = get_three_points_in_direction(p, direction)
    dumbbells.append(db)
    for p in db:
        board.pop(p)
    return board, dumbbells


def solve_one_dumbbell(board, dumbbells):
    possible_start_points = list(board.keys())

    for p in possible_start_points:
        options = get_possible_directions(board, p)

        for dir in options:
            new_board = board.copy()
            new_dumbbells = dumbbells.copy()

            new_board, new_dumbbells = solve_dumbbell_in_direction(new_board, new_dumbbells, p, dir)

            if len(new_dumbbells) == NUM_DBS and get_circles(new_board) == []:
                for db in new_dumbbells:
                    END_RESULT.append(db)
                return True

            res = solve_one_dumbbell(new_board, new_dumbbells)
            if res:
                return True
        if board[p] == ".":
            board.pop(p)
    return False


def flatten_dumbbells(dumbbells):
    result = {}
    for p1, p2, p3 in dumbbells:
        result[p1] = "o"
        result[p3] = "o"
        if p1[0] == p2[0]:
            result[p2] = "-"
        else:
            result[p2] = "|"
    return result


def solve_obvious_dumbbells(board, dumbbells):
    while True:
        obvious_dumbbells = [p for p in board if board[p] == "o" and len(get_possible_directions(board, p)) == 1]

        if len(obvious_dumbbells) == 0:
            return board, dumbbells

        p = obvious_dumbbells[0]
        dir = get_possible_directions(board, p)[0]
        board, dumbbells = solve_dumbbell_in_direction(board, dumbbells, p, dir)


# ********************************************************


NUM_DBS, myInput, MAX_ROW, MAX_COL = get_input()
END_RESULT = []

board = create_map(myInput)
dumbbells = []

# printBoard(board, dumbbells)
# print("")

board, dumbbells = solve_obvious_dumbbells(board, dumbbells)

# printBoard(board, dumbbells)

if len(dumbbells) == NUM_DBS and get_circles(board) == []:
    for db in dumbbells:
        END_RESULT.append(db)


solve_one_dumbbell(board, dumbbells)

printDumbbells(END_RESULT)
# printBoard(board, dumbbells)
