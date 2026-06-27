import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "True"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input=False) -> Game:
    if HOME_PC:

    else:


    if print_input:
        myPrint()

    return True


# Update the game per round
def update_game(GS: Game) -> None:
    if HOME_PC:
        True
    else:
        True
    return GS


# ********************************************************

G = get_start_parameters()

while True:
    update_game(G)
