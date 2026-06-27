import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input: bool = False) -> list[str]:
    if HOME_PC:
        data = [
            "09:13 > C001 C052 M796",
            "10:42 < C052",
            "10:45 < C001 M796",
            "12:16 > C005 C568 C235 C485",
            "14:35 > C174 C658 C856",
            "14:49 < C005",
            "15:02 < C856",
            "15:05 < C658",
            "15:06 > C888 C889 C890",
            "15:08 < C888",
            "15:33 > C845",
            "15:34 < C485",
            "16:43 < C174 C845",
            "16:49 > M174 M45845",
            "16:52 > M574 M0545 M582",
            "17:43 < M174 M45845",
            "17:48 > C174 C845 C382",
            "18:10 > M999",
            "18:13 < C174 C845",
            "18:14 < C889 C568",
            "18:33 < C235",
            "18:44 < M999",
        ]
        
        data=['10:00 > C456 M001 M002 M003', '11:00 < C456 M001 M002']
    else:
        h = int(input())
        data = [input() for _ in range(h)]

    if print_input:
        myPrint(f"{data=}")

    return data


def parse_log(data):
    result = []
    for line in data:
        time, type, *vehicles = line.split(" ")
        h, m = time.split(":")
        time = int(h) * 60 + int(m)
        type = "IN" if type == ">" else "OUT"
        for vehicle in vehicles:
            result.append((time, type, vehicle))
    return result


def calculate_fee(time_in, time_out, type):
    time = time_out - time_in
    if time < 30:
        return 0

    # Round time to nearest 15 upwards
    time = ((time + 14) // 15) * 15

    if type == "Car":
        return time // 15 * 1.2
    else:
        return time // 15 * 0.7


# ********************************************************

data = get_start_parameters(print_input=False)
data = parse_log(data)


cars = {}
motorbikes = {}
declined = {"Car": 0, "Motorbike": 0}
parking = {}
total_fee = 0

for time, type, vehicle in data:
    vehicle_type = "Car" if vehicle[0] == "C" else "Motorbike"
    if vehicle_type == "Car":
        parking = cars
        max_parking = 7
    elif vehicle_type == "Motorbike":
        parking = motorbikes
        max_parking = 2

    # Entering vehicle
    if type == "IN":

        # Parking is full
        if len(parking) >= max_parking:
            # print(f"{vehicle} is not allowed to enter")
            declined[vehicle_type] += 1
            continue

        # Parking is not full; add vehicle
        parking[vehicle] = time
        # print(f"{vehicle} entered at {time}")


    # Exiting vehicle
    elif type == "OUT":
        if vehicle not in parking:
            # print(f"{vehicle} is not in the parking")
            continue

        # print(f"{vehicle} exited at {time}")
        time_in = parking[vehicle]
        time_out = time
        parking.pop(vehicle)
        fee = calculate_fee(time_in, time_out, vehicle_type)
        total_fee += fee

total_fee += 30 * len(motorbikes) + 30 * len(cars)

print(f"{total_fee:.1f} {declined['Car']} {declined['Motorbike']}")


