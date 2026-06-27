from typing import Any, Tuple, List

SAMPLES: dict[str, list[str]] = {
    "data1": [
        "11|  |  |24",
    ],
    "data2": [
        "   |   |-6 |   ",
    ],
    "data3": [
        "     |     |     |     |4930 ",
    ],
    "data5": [
        "     |     |     |     |1230 |     |     |     |     |     ",
    ],
}

Point = Tuple[int, int]
Board = dict[Point, Any]


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        # Placeholder for parsing logic
        return data

    if start_data and start_data in SAMPLES:
        data = SAMPLES[start_data]
    else:
        True

    return parse(data)


# ********************************************************

data = get_start_parameters()
