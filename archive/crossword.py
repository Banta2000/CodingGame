import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters() -> Tuple[str, str, str, str]:
    if HOME_PC:
        h1, h2, v1, v2 = ["CORNEILLE", "BOILEAU", "RACINE", "MOLIERE"]
        # h1, h2, v1, v2 = ["SIN", "BUT", "SOB", "NOT"]
    else:
        h1 = input()
        h2 = input()
        v1 = input()
        v2 = input()
    myPrint(h1, h2, v1, v2)
    return h1, v1, h2, v2


# Returns list of (p1, p2) where strings have same letter
def get_match(s1, s2):
    result = []
    for i1, c1 in enumerate(s1):
        for i2, c2 in enumerate(s2):
            if c1 == c2:
                result.append((i1, i2))
    return result


# Returns true
def check_points(h11, v11, h12, v21, h21, v12, h22, v22):
    dist_h1 = h11 - h12
    dist_v1 = v11 - v12
    dist_h2 = h21 - h22
    dist_v2 = v21 - v22

    cond1 = dist_h1 == dist_h2 and dist_v1 == dist_v2
    cond2 = abs(dist_h1) > 1 and abs(dist_v1) > 1
    if cond1 & cond2:
        return True


# Returns the solution, the four intersection points
def find_match(h1, v1, h2, v2):
    h1_v1 = get_match(h1, v1)
    h1_v2 = get_match(h1, v2)
    h2_v1 = get_match(h2, v1)
    h2_v2 = get_match(h2, v2)

    res = []
    for h11, v11 in h1_v1:
        for h12, v21 in h1_v2:
            for h21, v12 in h2_v1:
                for h22, v22 in h2_v2:
                    if check_points(h11, v11, h12, v21, h21, v12, h22, v22):
                        res.append((h11, v11, h12, v21, h21, v12, h22, v22))
    
    return res


# Returns the starting coordinates of the four words
def get_starting_points(h11, v11, h12, v21, h21, v12, h22, v22):
    dist_h = h12 - h11
    dist_v = v12 - v11

    h1x, h1y = 0, 0

    h2y = h1y + dist_v
    h2x = h1x + h11 - h21

    v1x = h1x + h11
    v1y = h1y - v11

    v2x = v1x + dist_h
    v2y = h1y - v21
    return [(h1x, h1y), (h2x, h2y), (v1x, v1y), (v2x, v2y)]


def create_matrix(h1_p, v1_p, h2_p, v2_p, h1, h2, v1, v2):
    minx = min([x for x, y in [h1_p, v1_p, h2_p, v2_p]])
    miny = min([y for x, y in [h1_p, v1_p, h2_p, v2_p]])

    h1x, h1y = h1_p[0] - minx, h1_p[1] - miny
    v1x, v1y = v1_p[0] - minx, v1_p[1] - miny
    h2x, h2y = h2_p[0] - minx, h2_p[1] - miny
    v2x, v2y = v2_p[0] - minx, v2_p[1] - miny

    maxx = max([h1x + len(h1), h2x + len(h2)])
    maxy = max([v1y + len(v1), v2y + len(v2)])

    grid = [["." for _ in range(maxx)] for _ in range(maxy)]

    for i, c in enumerate(h1):
        grid[h1y][h1x + i] = c

    for i, c in enumerate(h2):
        grid[h2y][h2x + i] = c

    for i, c in enumerate(v1):
        grid[v1y + i][v1x] = c

    for i, c in enumerate(v2):
        grid[v2y + i][v2x] = c

    for line in grid:
        print("".join(line))


# ********************************************************

#    P1    P2
#    C R A N E       h1
#    A     P
#    R     P
# P3 D E C O R       v1
#    S     L P4
#          E


h1, v1, h2, v2 = get_start_parameters()

solutions = find_match(h1, v1, h2, v2)

if len(solutions) == 1:
    h11, v11, h12, v21, h21, v12, h22, v22 = solutions[0]
    h1_p, h2_p, v1_p, v2_p = get_starting_points(h11, v11, h12, v21, h21, v12, h22, v22)
    create_matrix(h1_p, v1_p, h2_p, v2_p, h1, h2, v1, v2)
else:
    print(len(solutions))



