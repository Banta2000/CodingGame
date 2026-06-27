from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper


def read_input():
    n = int(CGH.input())
    cases = []
    for i in range(n):
        case_entry = []
        line = CGH.input().split(" ")
        line = [int(x) for x in line]
        r = line[1]
        case_entry.append(r)
        line = line[2:]
        for i in range(0, len(line), 2):
            x = line[i]
            y = line[i + 1]
            case_entry.append((x, y))
        cases.append(case_entry)
    return cases


# ********************************************************

CGH = CodingGameHelper(1, __file__)
cases = read_input(
case_nr = 1

case = cases[case_nr]
print(case)
# CGH.print(XXXXX)
# CGH.assert_output()


# for case_nr in range(1, 4):
# CGH.print prints the line and also adds it to the queue for assert_output
# At the end, simply remove all CGH. from the code and it should work without the need to import CGH utils


# import matplotlib.pyplot as plt

# # Points data
# points = [(34, 5), (-36, 1), (4, 7), (-52, 5), (-61, 3), (44, 3), (27, 3), (59, 5)]

# radius = 7


# points = [(-39, 30), (-19, 11), (-51, 20), (-29, 18), (-77, 13)]

# radius = 29

# points = [(51, 11), (-22, 12), (-36, 17), (44, 4), (-25, 3), (26, 4), (-56, 17), (3, 7), (72, 18), (75, 11)]
# radius = 27


# fig, ax = plt.subplots()

# # Extract x and y coordinates
# x_coords, y_coords = zip(*points)

# # Plot the points
# ax.scatter(x_coords, y_coords, color="blue", label="Points")

# # Draw circles around each point
# for x, y in points:
#     circle = plt.Circle((x, y), radius, color="red", fill=False, linestyle="--")
#     ax.add_patch(circle)

# # Adjust plot limits to see all circles
# all_x = [x - radius for x, _ in points] + [x + radius for x, _ in points]
# all_y = [y - radius for _, y in points] + [y + radius for _, y in points]
# ax.set_xlim(min(all_x) - 5, max(all_x) + 5)
# ax.set_ylim(min(all_y) - 5, max(all_y) + 5)

# ax.set_aspect("equal", adjustable="box")
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.set_title("Points with Circles (Radius=7)")
# ax.grid(True)
# ax.legend()
