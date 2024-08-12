import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv('HOME_PC') == 'true'


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)

def get_input() -> dict[str, Any]:
    GS = {}
    if HOME_PC:
        GS["test"] = ["ABCSDE"]
    else:
        GS["test"] = ["ABCSDE"]

    return GS


# ********************************************************
