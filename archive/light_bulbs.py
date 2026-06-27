import sys
import os
from typing import Any, Tuple
from collections import deque

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters() -> Game:
    if HOME_PC:
        s = "1111"
        t = "0000"

    else:
        s = input()
        myPrint("s", s)
        t = input()
        myPrint("t", t)

    s = tuple([True if x == "1" else False for x in s])
    t = tuple([True if x == "1" else False for x in t])

    return s, t


# Rule 1: If a bulb is on, then the bulb to its right is toggled.
def rule1(s: tuple[bool]) -> list[tuple[bool]]:
    result = set()
    for i0 in range(len(s) - 3):
        i1, i2, i3 = i0 + 1, i0 + 2, i0 + 3
        c0, c1, c2, c3 = s[i0], s[i1], s[i2], s[i3]
        if c1 and not c2 and not c3:
            new = s[0:i0] + (not c0,) + s[i1:]
            result.add(new)
    return result


# Returns all neighbours based on rule1 and rule2
def get_neighbours(s: tuple[bool]) -> list[tuple[bool]]:
    neighbours = rule1(s)
    rule2 = s[:-1] + (not s[-1],)
    neighbours.add(rule2)
    return neighbours


# Main program
def bfs(s: tuple[bool], t: tuple[bool]) -> int:
    stack = deque([])
    visited = set()
    start_node = (s, 0)
    stack.append(start_node)
    while stack:
        curr, dist = stack.popleft()
        if curr == t:
            print(dist)
            return dist
        visited.add(curr)
        for neighbour in get_neighbours(curr):
            if neighbour not in visited and neighbour not in [x[0] for x in stack]:
                stack.append((neighbour, dist + 1))


# Prints string in nicer format
def print_string(s):
    s = "".join(["1" if x else "0" for x in s])
    myPrint(s)
    myPrint()


def flip(i, s, t):
    global COUNTER

    cache_key = s[i:]
    COUNTER_FREEZE = COUNTER
    if cache_key in CACHE:
        counter_increment, result = CACHE[cache_key]
        COUNTER += counter_increment
        return s[:i] + result

    if i == len(s) - 1:
        COUNTER += 1
        return s[:i] + (not s[i],)

    if s[i + 1] == False:
        s = flip(i + 1, s, t)

    j = i + 2
    while j <= len(s) - 1:
        if s[j] == True:
            s = flip(j, s, t)
        j += 1

    COUNTER += 1
    result = (not s[i],) + s[i + 1 :]
    CACHE[cache_key] = (COUNTER - COUNTER_FREEZE, result)
    myPrint("S ready for flippint")
    myPrint(s)
    myPrint(COUNTER - COUNTER_FREEZE)
    return s[:i] + result


# ***************************************************

COUNTER = 0
CACHE = {}

s, t = get_start_parameters()
print_string(t)
print_string(s)
# bfs(s, t)


for i in range(len(s)):
    if s[i] != t[i]:
        s = flip(i, s, t)

print_string(s)

print(COUNTER)
