import sys
import os
from typing import Any, Tuple
from collections import deque

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        radius = 4
        center = "ball"
    else:
        radius = int(input())
        center = input()
    myPrint("Radius:", radius)
    myPrint("Center1:", center)
    center = [ord(x) - 97 for x in center]
    myPrint("Center2:", center)
    return radius, center


def get_neighbours(num_list):
    neighbours = []
    for i, num in enumerate(num_list):
        for j in [-1, 1]:
            if 0 <= num + j <= 25:
                num_list_copy = list(num_list)
                num_list_copy[i] = num + j
                neighbours.append(tuple(num_list_copy))
    return neighbours


def bfs(center, radius):
    node = (center, 0)
    stack = deque([])
    stack.append(node)
    visited = set()
    counter = 0

    while stack:
        curr, dist = stack.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        counter += 1
        if dist == radius:
            continue
        neighbours = get_neighbours(curr)
        for neighbour in neighbours:
            if neighbour not in visited:
                node = (neighbour, dist + 1)
                stack.append(node)
    print(counter)


def find_num_combinations_one_all_capacities_combinations(center, radius):
    combinations = create_combinations(center, radius)
    count = 0
    for capacities in combinations:
        count += find_num_combinations_one_set_capacities(capacities, radius)
    return count


def find_num_combinations_one_set_capacities(capacities, liquid):
    # Helper function to recursively count distributions
    def distribute(remaining_liquid, remaining_capacities):
        if not remaining_capacities:
            return 1 if remaining_liquid == 0 else 0

        count = 0
        current_capacity = remaining_capacities[0]
        for x in range(0, min(remaining_liquid, current_capacity) + 1):
            count += distribute(remaining_liquid - x, remaining_capacities[1:])

        return count

    return distribute(liquid, capacities)


def find_combinations(liquid, capacities):
    CACHE = {}

    # Helper function to recursively count distributions
    def distribute(remaining_liquid, remaining_capacities):
        key = (remaining_liquid, remaining_capacities)
        if key in CACHE:
            return CACHE[key]

        if not remaining_capacities:
            return 1 if remaining_liquid == 0 else 0

        count = 0
        current_capacity = remaining_capacities[0]
        new_capacities = remaining_capacities[1:]
        for x in range(current_capacity[0], current_capacity[1] + 1):
            count += distribute(remaining_liquid - abs(x), new_capacities)

        CACHE[key] = count
        return count

    return distribute(liquid, capacities)


# Convert the center into a series of vessels with minus size / plus size, capped with radius
def create_combinations(nums: list, radius: int):
    def _convert_to_two_side_with_caps(num, radius):
        return [min(num, radius), min(25 - num, radius)]

    nums = [_convert_to_two_side_with_caps(x, radius) for x in nums]

    response = []
    for x1, x2 in nums:
        if response == []:
            response = [[x1], [x2]]
        else:
            c1 = [x + [x1] for x in response]
            c2 = [x + [x2] for x in response]
            response = c1 + c2
    return response


# Convert the center into a series of vessels with minus size / plus size, capped with radius
def create_combinations2(nums: list, radius: int):
    def _convert_to_two_side_with_caps(num, radius):
        return [-min(num, radius), min(25 - num, radius)]

    response = [_convert_to_two_side_with_caps(x, radius) for x in nums]
    response = [tuple(x) for x in sorted(response, key=lambda x: (x[0], x[1]))]
    response = tuple(response)
    return response


# ********************************************************

# bfs(center, radius)

radius, center = get_start_parameters()
center2 = create_combinations2(center, radius)
myPrint("Center3:", center2)

count = 1
for i in range(1, radius + 1):
    count += find_combinations(i, center2)
print(count)
