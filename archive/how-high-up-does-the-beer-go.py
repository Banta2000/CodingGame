from typing import Any, Tuple, List
import os
import importlib.util

Point = Tuple[int, int]
Board = dict[Point, Any]


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        # Placeholder for parsing logic
        return data

    # Read from local file
    if start_data:
        current_file = os.path.basename(__file__)[:-3]  # Remove .py extension
        testcases_filename = current_file + "-testcases.py"  # Keep hyphens for actual filename
        testcases_module_name = current_file.replace("-", "_") + "_testcases"  # Underscores for module name
        current_dir = os.path.dirname(__file__)
        testcases_file_path = os.path.join(current_dir, testcases_filename)
        spec = importlib.util.spec_from_file_location(testcases_module_name, testcases_file_path)
        testcases = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(testcases)
        data = testcases.TEST_INPUTS[start_data]

    # Read from web
    else:
        data = input()

    bottomRadius, topRadius, glassHeight, beerVol = [float(x) for x in data.split(" ")]
    return bottomRadius, topRadius, glassHeight, beerVol


def how_much_volume(h: float) -> float:
    # Returns the volume contained by a glass with boottomRadius, topRadius, glassHeight, up to height h

    # Step 1: Calculate the radius at height h using similar triangles
    new_rad = bottomRadius + h * (topRadius - bottomRadius) / glassHeight

    # Step 2: Calculate the volume of the frustum up to height h
    volume = (1 / 3) * 3.141592653589793 * h * (bottomRadius**2 + bottomRadius * new_rad + new_rad**2)
    return volume


# ********************************************************

# Now you can use any test case like this:
bottomRadius, topRadius, glassHeight, beerVol = get_start_parameters("test_3")
# print(bottomRadius, topRadius, glassHeight, beerVol)

h = 0
while True:
    if how_much_volume(h) >= beerVol:
        break
    h += 0.1

below = h - 0.1
above = h

dist_below = beerVol - how_much_volume(below)
dist_above = how_much_volume(above) - beerVol

if dist_below < dist_above:
    res = below
else:
    res = above

print(round(res, 1))
