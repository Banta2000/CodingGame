import sys
import os
from typing import Any, Tuple

GameState = dict[str, Any]


HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_initial_GS() -> GameState:
    GS = {}
    if HOME_PC:
        GS["coins"] = [500, 200, 100, 50, 20, 2, 1]
        GS["amount"] = 5283
    else:
        register = input()
        GS["coins"] = [int(i) for i in register.split()]
        amount = int(input())
        GS["amount"] = int(amount)

    GS["coins"].sort(reverse=True)
    return GS


def bfs(GS: GameState) -> int:
    options = GS["coins"]
    curr = GS["amount"]
    path = []
    stack = [(curr, path)]
    explored = set()

    while stack:
        curr, path = stack.pop(0)
        if curr in explored:
            continue
        explored.add(curr)
        if curr == 0:
            return path
        for option in options:
            if path and option > path[-1]:
                continue
            if option <= curr:
                stack.append((curr - option, path + [option]))
    return []


# ********************************************************

GS = get_initial_GS()
myPrint(GS)
res = bfs(GS)

if GS["amount"] == 0:
    print("0")
elif len(res) == 0:
    print("IMPOSSIBLE")
else:
    res = " ".join(str(i) for i in res)
    print(res)
