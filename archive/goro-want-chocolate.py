import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"
Piece = Tuple[int, int]


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        h, w = 101, 97
    else:
        h, w = [int(i) for i in input().split()]

    h, w = sorted([h, w])
    return h, w


def get_horiontal_cuts(origin: Piece) -> List[Tuple[Piece, Piece]]:
    """Get horizontal cuts from the origin piece."""
    h, w = origin
    if h == 0 or w == 0:
        return []
    cuts = []
    for i in range(1, h):
        cuts.append(((i, w), (h - i, w)))
    return cuts


def get_vertical_cuts(origin: Piece) -> List[Tuple[Piece, Piece]]:
    """Get vertical cuts from the origin piece."""
    h, w = origin
    if h == 0 or w == 0:
        return []
    cuts = []
    for i in range(1, w):
        cuts.append(((h, i), (h, w - i)))
    return cuts


def get_all_cuts(origin: Piece) -> List[Tuple[Piece, Piece]]:
    cuts = []
    cuts.extend(get_horiontal_cuts(origin))
    cuts.extend(get_vertical_cuts(origin))
    return cuts


def calculate_new_entry(piece: Piece) -> None:
    """Calculate the new entry for the DP table."""
    h, w = piece
    if piece in DP:
        return

    reverse_piece = (w, h)
    if reverse_piece in DP:
        DP[piece] = DP[reverse_piece]
        return

    if h == w:
        DP[piece] = 1
        return

    cuts = get_all_cuts(piece)
    best_option = float("inf")
    for cuta, cutb in cuts:
        if cuta not in DP or cutb not in DP:
            print("This should not happen")
            print("Original piece:", piece)
            print("Cut A:", cuta)
            print("Cut B:", cutb)
        option = DP[cuta] + DP[cutb]
        if option < best_option:
            best_option = option

    DP[piece] = best_option
    return


# ********************************************************

DP = {(1, 1): 1}

max_h, max_w = get_start_parameters()

for test_h in range(1, max_h + 1):
    for test_w in range(1, max_w + 1):
        test = (test_h, test_w)
        calculate_new_entry(test)

print(DP[(max_h, max_w)])
