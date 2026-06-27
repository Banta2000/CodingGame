import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        board = {"d": 0, "f": 1}
        required_response = ["k", "g", "j", "c", "h"]
        rules = [
            "a and b -> e",
            "a and c -> f",
            "b and d -> g",
            "c and d -> h",
            "e and g -> i",
            "f and h -> j",
            "i and j -> k",
        ]

    else:
        board = input()
        board = board.split(" ")
        board = [x.split(":") for x in board]
        board = {x[0]: int(x[1]) for x in board}

        required_response = input()
        required_response = required_response.split(" ")

        n = int(input())
        rules = [input() for _ in range(n)]

    for i in range(len(rules)):
        test = rules[i].replace("-> ", "")
        rules[i] = test.split(" ")

    return board, required_response, rules


def compute(rule):
    pa = rule[0]
    operation = rule[1]
    pb = rule[2]
    pc = rule[3]

    if pc in board and operation == "and" and board[pc] == 1:
        board[pa] = 1
        board[pb] = 1
        return True

    if pa in board and board[pa] == 0 and operation == "and":
        board[pc] = 0
        return True

    if pb in board and board[pb] == 0 and operation == "and":
        board[pc] = 0
        return True

    if pc in board and operation == "or" and board[pc] == 0:
        board[pa] = 0
        board[pb] = 0
        return True

    if pa in board and board[pa] == 1 and operation == "or":
        board[pc] = 1
        return True

    if pb in board and board[pb] == 1 and operation == "or":
        board[pc] = 1
        return True

    how_many_in_board = [pa in board, pb in board, pc in board]
    how_many_in_board = sum(how_many_in_board)

    if how_many_in_board <= 1:
        return False

    if pa in board and pb in board:
        if operation == "and":
            board[pc] = board[pa] and board[pb]
        elif operation == "or":
            board[pc] = board[pa] or board[pb]
        elif operation == "xor":
            board[pc] = board[pa] ^ board[pb]
        else:
            raise ValueError(f"Unknown operator: {rule[1]}")
        return True

    # pc is in board
    result = board[pc]
    if pa in board:
        known = board[pa]
        unknown = pb
    elif pb in board:
        known = board[pb]
        unknown = pa

    # print(f"{known} {operation} {unknown} -> {result}")

    if operation == "and" and result == 1:
        board[unknown] = 1
        return True
    elif operation == "and" and result == 0:
        if known == 1:
            board[unknown] = 0
            return True
    if operation == "or" and result == 1:
        if known == 0:
            board[unknown] = 1
            return True
    if operation == "xor" and result == 1:
        if known == 0:
            board[unknown] = 1
            return True
        elif known == 1:
            board[unknown] = 0
            return True
    if operation == "xor" and result == 0:
        if known == 0:
            board[unknown] = 0
            return True
        elif known == 1:
            board[unknown] = 1
            return True

    # print(f"Couldn't solve {known} {operation} {unknown} -> {result}")

    return False


def solve(board: dict[str, Any], rules: List[List[str]]) -> None:
    while True:
        for rule in rules[:]:
            compute(rule)
            # print(rule)
            # rules.remove(rule)
        # for rule in rules:
        # print(rule)
        # print("knowns", board.keys())
        exit_condition = all(i in board for i in required_response)
        if exit_condition:
            break


# ********************************************************

board, required_response, rules = get_start_parameters()

solve(board, rules)
response = [str(board[i]) for i in required_response]
print("".join(str(i) for i in response))
