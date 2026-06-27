import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        lengthofline = 50
        data = [
            "Sudamerica 1",
            ">Argentina 5",
            ">>BuenosAires 8",
            ">>Cordoba 10",
            ">Brasil 15",
            ">>SaoPaulo 20",
            ">>Fortaleza 25",
            "Asia 30",
            ">Japan 32",
            ">>Yokohama 35",
            ">>Tokio 40",
            ">Iran 42",
            ">>Teheran 45",
        ]

        lengthofline = 30
        data = [
            "One 5",
            "Two 10",
            "Three 11",
            "Four 20",
            "Five 40",
            "Six 45",
            "Seven 66",
            "Eight 80",
            "Nine 99",
            "AppendixA 100",
        ]
    else:

        lengthofline = int(input())
        n = int(input())
        data = [input() for _ in range(n)]
    return data, lengthofline


def parse_line(line: str) -> List:
    line, page_num = line.split(" ")
    counter = 0
    while line[counter] == ">":
        counter += 1
    line = line[counter:]
    return [counter, line, page_num]


def print_line(line: list) -> None:
    indentation, title, page_num, numbering = line
    indentation = " " * (indentation * 4)
    fill_length = lengthofline - len(indentation) - len(page_num) - len(title) - len(str(numbering)) - 1
    fill_length = "." * fill_length
    print(f"{indentation}{numbering} {title}{fill_length}{page_num}")


def add_numbers_to_subsections(data):
    level_stack = [1]
    result = [1]
    for i in range(1, len(data)):
        curr_level, prev_level = data[i][0], data[i - 1][0]
        # print(f"Current level: {curr_level}, Previous level: {prev_level}")
        if curr_level == prev_level:
            level_stack[-1] += 1
            result.append(level_stack[-1])
        elif curr_level > prev_level:
            level_stack.append(1)
            result.append(1)
        elif curr_level < prev_level:
            for _ in range(prev_level - curr_level):
                level_stack.pop()
            level_stack[-1] += 1
            result.append(level_stack[-1])
    data = [data[i] + [result[i]] for i in range(len(data))]
    return data


# ********************************************************

data, lengthofline = get_start_parameters()
data = [parse_line(line) for line in data]
data = add_numbers_to_subsections(data)
for line in data:
    print_line(line)
