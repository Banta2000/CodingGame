import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"
DECK = [str(x) for x in range(2, 10)] + ["T", "J", "Q", "K", "A"]
DECK = [f"{x}{y}" for x in DECK for y in "CDHS"]
DECK = set(DECK)


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input=False) -> Game:
    if HOME_PC:
        removed = "45C"
        sought = "H"
    else:
        r, s = [int(i) for i in input().split()]
        removed = [input() for _ in range(r)]
        sought = [input() for _ in range(s)]

    if print_input:
        myPrint(removed, sought)

    return removed, sought


def match_cards(letter_combination: str):
    ranks = [x for x in letter_combination if x in "23456789TJQKA"]
    if ranks == []:
        ranks = [x for x in "23456789TJQKA"]
    suits = [x for x in letter_combination if x in "CDHS"]
    if suits == []:
        suits = [x for x in "CDHS"]

    r = set()
    for letter in ranks:
        r.update({card for card in DECK if letter in card})

    s = set()
    for letter in suits:
        s.update({card for card in DECK if letter in card})

    return r.intersection(s)


# ********************************************************

removed, sought = get_start_parameters(print_input=True)

r = set()
for x in removed:
    r.update(match_cards(x))
myPrint("Overall Removed", r)

s = set()
for x in sought:
    s.update(match_cards(x))
s = s - r
myPrint("Overall Sought", r)


DECK -= r
print(f"{len(s) / len(DECK) * 100:.0f}%", sep="")
