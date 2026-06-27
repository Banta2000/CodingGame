import sys
import os
from typing import Any, Tuple

Data = dict[str, dict]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> Data:
    if HOME_PC:
        data = {
            "Elizabeth": {"parent": "-", "birth": 1926, "death": "-", "gender": "1"},
            "Charles": {"parent": "Elizabeth", "birth": 1948, "death": "-", "gender": "0"},
            "William": {"parent": "Charles", "birth": 1982, "death": "-", "gender": "0"},
            "George": {"parent": "William", "birth": 2013, "death": "-", "gender": "0"},
            "Charlotte": {"parent": "William", "birth": 2015, "death": "-", "gender": "1"},
            "Henry": {"parent": "Charles", "birth": 1984, "death": "-", "gender": "0"},
        }

    else:
        data = {}
        n = int(input())
        for _ in range(n):
            inputs = input().split()
            name = inputs[0]
            parent = inputs[1]
            birth = int(inputs[2])
            death = inputs[3]
            religion = inputs[4]
            gender = inputs[5]
            gender = 0 if gender == "M" else 1
            data[name] = {"parent": parent, "birth": birth, "death": death, "gender": gender, "religion": religion}

    if print_input:
        myPrint(data)

    return data


# Returns the member with no parent (head of the family)
def get_head(data: dict) -> str:
    for name, info in data.items():
        if info["parent"] == "-":
            return name


# Collects the children of the person, adds it to a list sorted by 1) gender, 2) birth year
def order_children_of_person(data: dict, name: str) -> list[str]:
    children = [child for child, info in data.items() if info["parent"] == name and info["death"] == "-"]
    children.sort(key=lambda x: (data[x]["gender"], data[x]["birth"]))
    data[name]["children"] = children
    return data


# Adds children to all members
def add_children_to_all_members(data: dict) -> dict:
    for name in data:
        data = order_children_of_person(data, name)
    return data


# Depth-First Search to print the order of succession
def dfs(data: dict, person: str):
    if data[person]["death"] == "-" and data[person]["religion"] == "Anglican":
        print(person)
    for child in data[person]["children"]:
        dfs(data, child)


# ********************************************************

data = get_start_parameters(print_input=False)
head = get_head(data)
data = add_children_to_all_members(data)

for k, v in data.items():
    myPrint(k, v)

dfs(data, head)
