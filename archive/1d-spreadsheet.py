import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> bool:
    if HOME_PC:
        data = [
            ("MULT", "$61", "$95"),
            ("ADD", "$26", "$80"),
            ("ADD", "$6", "$0"),
            ("ADD", "$98", "$39"),
            ("ADD", "$72", "$14"),
            ("SUB", "$12", "$32"),
            ("MULT", "$73", "$86"),
            ("ADD", "$80", "$12"),
            ("MULT", "$86", "$60"),
            ("SUB", "$39", "$59"),
            ("SUB", "$64", "$83"),
            ("SUB", "$98", "$91"),
            ("SUB", "$59", "$80"),
            ("MULT", "$65", "$73"),
            ("ADD", "$25", "$3"),
            ("ADD", "$93", "$10"),
            ("SUB", "$93", "$72"),
            ("MULT", "$43", "$23"),
            ("MULT", "$43", "$51"),
            ("MULT", "$71", "$0"),
            ("SUB", "$60", "$3"),
            ("ADD", "$77", "$46"),
            ("SUB", "$23", "$40"),
            ("MULT", "$99", "$6"),
            ("MULT", "$44", "$39"),
            ("VALUE", "$28", "_"),
            ("VALUE", "$43", "_"),
            ("ADD", "$92", "$46"),
            ("ADD", "$49", "$86"),
            ("SUB", "$82", "$41"),
            ("ADD", "$12", "$89"),
            ("ADD", "$91", "$86"),
            ("SUB", "$60", "$9"),
            ("MULT", "$51", "$3"),
            ("SUB", "$12", "$94"),
            ("ADD", "$12", "$28"),
            ("ADD", "$66", "$69"),
            ("SUB", "$53", "$1"),
            ("ADD", "$98", "$53"),
            ("ADD", "$98", "$98"),
            ("ADD", "$42", "$59"),
            ("SUB", "$64", "$0"),
            ("SUB", "$98", "$6"),
            ("MULT", "609", "-14"),
            ("ADD", "$60", "$55"),
            ("SUB", "$59", "-245"),
            ("MULT", "$64", "$1"),
            ("MULT", "$99", "$98"),
            ("ADD", "$46", "$97"),
            ("SUB", "$86", "$43"),
            ("MULT", "$28", "$18"),
            ("MULT", "$64", "$40"),
            ("SUB", "$70", "$32"),
            ("MULT", "$91", "$80"),
            ("ADD", "$83", "$6"),
            ("ADD", "$97", "$76"),
            ("MULT", "$23", "$45"),
            ("SUB", "$53", "$22"),
            ("MULT", "$6", "$10"),
            ("ADD", "$39", "$98"),
            ("MULT", "$17", "$26"),
            ("MULT", "$93", "$59"),
            ("SUB", "$70", "$99"),
            ("SUB", "$64", "$43"),
            ("SUB", "$9", "$9"),
            ("MULT", "$91", "$53"),
            ("MULT", "$26", "$80"),
            ("ADD", "$9", "$43"),
            ("SUB", "$72", "$13"),
            ("ADD", "$64", "$82"),
            ("ADD", "$80", "$45"),
            ("SUB", "$12", "$61"),
            ("ADD", "$53", "$73"),
            ("SUB", "$43", "$98"),
            ("MULT", "$47", "$86"),
            ("SUB", "$56", "$99"),
            ("SUB", "$53", "$51"),
            ("ADD", "681", "$43"),
            ("ADD", "$70", "$18"),
            ("MULT", "$12", "$51"),
            ("MULT", "$6", "$45"),
            ("SUB", "$99", "$40"),
            ("VALUE", "$45", "_"),
            ("SUB", "$59", "$98"),
            ("SUB", "$6", "$59"),
            ("MULT", "$55", "$51"),
            ("SUB", "$39", "$39"),
            ("SUB", "$26", "$73"),
            ("ADD", "$84", "$92"),
            ("ADD", "$97", "$50"),
            ("SUB", "$75", "$66"),
            ("ADD", "$86", "$43"),
            ("MULT", "295", "$60"),
            ("MULT", "$31", "$17"),
            ("SUB", "$9", "$11"),
            ("SUB", "$87", "$65"),
            ("MULT", "$64", "$55"),
            ("MULT", "$49", "$23"),
            ("MULT", "-6", "380"),
            ("VALUE", "$53", "_"),
        ]
    else:
        n = int(input())
        data = []
        for _ in range(n):
            operation, arg_1, arg_2 = input().split()
            data.append((operation, arg_1, arg_2))

    if print_input:
        myPrint(f"{data=}")

    return data


# Go through the data and see if all values are solved
def is_done(data):
    res = [isinstance(x, int) for x in data]
    return all(res)


# Check if the arguments of a given instruction are solved
def is_possible(inst, arg1, arg2):
    def check_arg(arg):
        if arg[0] != "$":
            return True
        else:
            arg = int(arg[1:])
            return isinstance(data[arg], int)

    a1 = check_arg(arg1)
    a2 = check_arg(arg2)
    return a1 and a2


# Compute the result of an instruction, it assumes that both arguments are solved
def compute(inst, arg1, arg2):
    def get_arg_value(arg):
        if arg == "_":
            return "_"  #
        elif arg[0] != "$":
            return int(arg)
        else:
            arg = int(arg[1:])
            return int(data[arg])

    a1 = get_arg_value(arg1)
    a2 = get_arg_value(arg2)

    if inst == "ADD":
        return a1 + a2

    if inst == "SUB":
        return a1 - a2

    if inst == "MULT":
        return a1 * a2

    if inst == "VALUE":
        return a1


# Go through the data and solve all possible instructions
def do_one_round(data):
    for i, line in enumerate(data):
        if isinstance(line, tuple) and is_possible(*line):
            data[i] = compute(*line)
    return data


# ********************************************************

data = get_start_parameters(print_input=False)
while not is_done(data):
    data = do_one_round(data)

for i, line in enumerate(data):
    if isinstance(line, int):
        print(line)
