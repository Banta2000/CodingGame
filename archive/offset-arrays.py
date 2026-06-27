import sys
import os
from typing import Any, Tuple
from dataclasses import dataclass


Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


@dataclass
class MYLIST:
    start: int
    values: list[int]

    def get(self, index):
        return self.values[index - self.start]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Game:
    if HOME_PC:
        data = ["A[-1..1] = 1 2 3", "B[3..7] = 3 4 5 6 7", "C[-2..1] = 1 2 3 4"]
        data = ["ARR[-5..-3] = 11 22 33"]
        data = ["X[0..3] = 1 3 3 7"]
        question = "ARR[-4]"
        question = "X[X[2]]"
    else:
        data = []
        n = int(input())
        data = [input() for _ in range(n)]
        question = input()

    if print_input:
        myPrint("data =", data)
        myPrint("question =", question)

    for line in data:
        parse_line(line)

    # question = separate_list_name_and_index(question)
    # question = question[0], int(question[1])

    return question


def separate_list_name_and_index(line):
    first_bracket_index = line.find("[")
    name = line[:first_bracket_index]
    inside_square_brackets = line[first_bracket_index + 1 : -1]
    return name, inside_square_brackets


# Example: C[-2..1] = 1 2 3 4   returns a new MYLIST
def parse_line(line):
    parts = line.split(" = ")
    name, inside_square_brackets = separate_list_name_and_index(parts[0])
    start = int(inside_square_brackets.split("..")[0])

    values = parts[1].split(" ")
    values = [int(x) for x in values]

    list_collection[name] = MYLIST(start, values)
    return True


def parse_question_and_evalute(line):
    name, inside_brackets = separate_list_name_and_index(line)
    if "[" not in inside_brackets:
        res = int(inside_brackets)
    else:
        res = parse_question_and_evalute(inside_brackets)
    return list_collection[name].get(res)


# ********************************************************

list_collection = {}
question = get_start_parameters(print_input=True)
myPrint(list_collection)
r = parse_question_and_evalute(question)
print(r)


# myPrint(question)
# print(list_collection[question[0]].get(question[1]))
# parse_line("C[-2..1] = 1 2 3 4")
# print(list_collection)
# print(list_collection["A"].get(0))
