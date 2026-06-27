import sys
import math


def myPrint(lst):
    print("Debug messages...", lst, file=sys.stderr, flush=True)


def solveOneGroup(group):
    group = sorted(group)
    Adults = [x for x in group if x == "A"]
    Childs = [x for x in group if x in ["x", "k"]]

    if len(Adults) < len(Childs):
        return []

    Childs = sorted(Childs, reverse=True)
    result = []
    while Childs:
        result.append(Adults.pop(0))
        result.append(Childs.pop(0))

    while Adults:
        result.append(Adults.pop(0))

    if len(result) % 2 == 1:
        result.append("D")
    return result


def solveOneRide(groups):
    result = []
    for group in groups:
        result += solveOneGroup(group)
    while len(result) < 20:
        result.append("D")
    return result


def getGroupLength(group):
    res = solveOneGroup(group)
    return len(res)


def createASCII(ride):
    r = [x for i, x in enumerate(ride) if i % 2 == 0]

    right_ascii = "/< |"
    for x in r:
        right_ascii += " " + x + " |"

    l = [x for i, x in enumerate(ride) if i % 2 == 1]
    left_ascii = "\\< |"
    for x in l:
        left_ascii += " " + x + " |"

    return right_ascii, left_ascii


def putInGroups(groups):
    group_of_groups = []
    while groups:
        group = []
        while groups and sum([len(sub) for sub in group]) + len(groups[0]) <= 20:
            group.append(groups.pop(0))
        group_of_groups.append(group)
    return group_of_groups


def solve(input):
    groups = [sorted(x) for x in input.split(" ")]
    groups = [solveOneGroup(x) for x in groups]

    # Put all the group in trains of max 20 people
    group_of_groups = putInGroups(groups)

    # Find the train where I am
    for i, group in enumerate(group_of_groups):
        if "x" in [x for sub in group for x in sub]:
            ride = solveOneRide(group)
            break

    left_ascii, right_ascii = createASCII(ride)

    print(i+1)
    print(left_ascii)
    print(right_ascii)


# ********************************************************

# n = int(input())
# groups = input()

# myPrint(n)
# myPrint(groups)


# groups = "AkkAA kAAkA kAAkA AAk AAAx"
groups = "kAA AkA AkAAA Ax"
solve(groups)

# # print("1")
# # print("/< | A | A | A | A | A | A | A | A | D | D |")
# # print("\\< | k | k | k | A | k | k | x | k | D | D |")


# | A | A | A |
# | k | A | D |

# | A | A | A |
# | k | D | A |
