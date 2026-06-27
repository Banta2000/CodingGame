import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    """
    Custom print function to print to stderr.
    """
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters() -> Tuple[int, int]:
    """
    Get the starting parameters for the game.
    """
    if HOME_PC:
        r, l = 1, 6
    else:
        r = int(input())
        l = int(input())
        myPrint("r:", r, "l:", l)
    return r, l


def calculate_next_line(a: List[int]) -> List[int]:
    """
    Calculate the next line in the Conway sequence.
    """
    res = []
    curr_char = a[0]
    count = 0
    for c in a:
        if c == curr_char:
            count += 1
        else:
            res.append(count)
            res.append(curr_char)
            curr_char = c
            count = 1
    res.append(count)
    res.append(curr_char)
    return res


# Main execution
if __name__ == "__main__":
    r, l = get_start_parameters()

    line = [r]
    for i in range(l - 1):
        line = calculate_next_line(line)

    print(*line)
