import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


def get_start_parameters(print_input: bool = False):
    if HOME_PC:
        n, c, p = 4, 10, 5
        data = ["9 4", "7 10", "9 3", "6 1"]

        n, c, p = 3, 10, 7
        data = ["13 -4", "120 -9", "31 -73"]

        n, c, p = 12, 20, 5
        data = [
            "12 1",
            "4 -5",
            "6 10",
            "9 -11",
            "12 20",
            "32 11",
            "511 -22",
            "31 -64",
            "54 23",
            "9 101",
            "67 -12",
            "43 -14",
        ]

    else:
        n, c, p = [int(i) for i in input().split()]
        data = [input() for _ in range(n)]

    data = [[int(j) for j in line.split()] for line in data]
    res = []
    for budget, joy in data:
        res.append({"budget": budget, "joy": joy})

    return n, c, p, res


def price_per_person(num_friends: int) -> float:
    total_people = num_friends + 1
    total_cost = C + (total_people * P)
    return total_cost / total_people


def get_eligible_friends(price_per_person: float):
    eligible_friends = []
    for i in range(N):
        if DATA[i]["budget"] >= price_per_person:
            eligible_friends.append(DATA[i])
    return eligible_friends


def max_joy(eligible_friends: List[dict], num_friends: int) -> int:
    # I must bring exactly num_friends

    # If there are not enough eligible friends, return 0
    if len(eligible_friends) < num_friends:
        return 0

    # Sort the eligible friends by joy in descending order
    eligible_friends.sort(key=lambda x: x["joy"], reverse=True)
    # Select the top num_friends friends
    selected_friends = eligible_friends[:num_friends]
    # Calculate the total joy
    total_joy = sum(friend["joy"] for friend in selected_friends)
    return total_joy


def get_max_joy(num_friends) -> int:
    # print("Number of friends:", num_friends)
    price = price_per_person(num_friends)
    # print("Price per person:", price_per_person)
    eligible_friends = get_eligible_friends(price)
    # for friend in eligible_friends:
    # print("Eligible friend:", friend)
    max_joy_value = max_joy(eligible_friends, num_friends)
    # print("Max joy value:", max_joy_value)
    return max_joy_value


# ********************************************************

N, C, P, DATA = get_start_parameters(print_input=True)
# print(N, C, P, DATA)
options = [get_max_joy(i) for i in range(0, N + 1)]
max_joy_value = max(options)
print(max_joy_value)
