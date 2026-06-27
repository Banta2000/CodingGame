import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_input(GS: dict[str, Any]) -> dict[str, Any]:
    if HOME_PC:
        GS["test"] = ["ABCSDE"]
    else:
        inputs = input().split()
        GS["clone_floor"] = int(inputs[0])  # floor of the leading clone
        GS["clone_pos"] = int(inputs[1])  # position of the leading clone on its floor
        GS["direction"] = inputs[2]  # direction of the leading clone: LEFT or RIGHT

    return GS


def get_init_input() -> dict[str, Any]:
    GS = {}
    # nb_floors: number of floors
    # width: width of the area
    # nb_rounds: maximum number of rounds
    # exit_floor: floor on which the exit is found
    # exit_pos: position of the exit on its floor
    # nb_total_clones: number of generated clones
    # nb_additional_elevators: ignore (always zero)
    # nb_elevators: number of elevators
    nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [
        int(i) for i in input().split()
    ]
    GS["nb_floors"] = nb_floors
    GS["width"] = width
    GS["nb_rounds"] = nb_rounds
    GS["exit_floor"] = exit_floor
    GS["exit_pos"] = exit_pos
    GS["nb_total_clones"] = nb_total_clones
    GS["nb_additional_elevators"] = nb_additional_elevators
    GS["nb_elevators"] = nb_elevators
    GS["elevators"] = []
    for i in range(nb_elevators):
        # elevator_floor: floor on which this elevator is found
        # elevator_pos: position of the elevator on its floor
        elevator_floor, elevator_pos = [int(j) for j in input().split()]
        GS["elevators"].append((elevator_floor, elevator_pos))
    return GS


def is_heading_into_teleporter(GS: dict[str, Any]) -> bool:
    teleporter_on_floor = [e for e in GS["elevators"] if e[0] == GS["clone_floor"]]
    if len(teleporter_on_floor) == 0:
        return False

    if len(teleporter_on_floor) > 1:
        print("ERROR: More than one teleporter on floor")

    teleporter_pos = teleporter_on_floor[0][1]
    if GS["direction"] == "RIGHT":
        return GS["clone_pos"] <= teleporter_pos
    else:
        return GS["clone_pos"] >= teleporter_pos


def is_heading_into_exit(GS: dict[str, Any]) -> bool:
    if GS["direction"] == "RIGHT":
        return GS["clone_pos"] <= GS["exit_pos"]
    else:
        return GS["clone_pos"] >= GS["exit_pos"]


# ********************************************************


GS = get_init_input()

while True:
    GS = get_input(GS)
    myPrint(GS)

    ON_FINAL_FLOOR = GS["clone_floor"] == GS["exit_floor"]
    HEADING_INTO_TELEPORTER = is_heading_into_teleporter(GS)
    HEADING_INTO_EXIT = is_heading_into_exit(GS)

    myPrint(f"ON_FINAL_FLOOR: {ON_FINAL_FLOOR}")
    myPrint(f"HEADING_INTO_TELEPORTER: {HEADING_INTO_TELEPORTER}")
    myPrint(f"HEADING_INTO_EXIT: {HEADING_INTO_EXIT}")

    if GS["direction"] == "NONE":
        myPrint("No direction, wait")
        print("WAIT")
        continue

    if not ON_FINAL_FLOOR and not HEADING_INTO_TELEPORTER:
        myPrint("Not on final floor and not heading into teleporter, block")
        print("BLOCK")
        continue

    if ON_FINAL_FLOOR and not HEADING_INTO_EXIT:
        myPrint("On final floor but not heading into exit, block")
        print("BLOCK")
        continue

    myPrint("On final floor, heading into exit, wait")
    print("WAIT")
