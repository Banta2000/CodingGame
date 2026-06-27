import os
from typing import Any, Tuple, List
from AlgoXSolver import AlgoXSolver


HOME_PC: bool = True


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        # data = ["2043", "0020", "4300", "0034"]
        # data = ["0000", "2014", "3021", "0000"]
        data = ["0104", "0020", "0300", "4010"]

    else:
        data = [input() for _ in range(4)]

    res = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char != "0":
                res.append((row + 1, col + 1, int(char)))

    return res


def generate_requirements() -> List[Tuple]:
    # In der 2. Zeile muss es eine 3 geben
    # ("row", "row_num", "num")
    # ("row", 2, 3)
    res = []
    for t in ["row", "col"]:
        for i in range(1, NUM_TOT + 1):
            for j in range(1, NUM_TOT + 1):
                res.append((t, i, j))

    # Im 1. quadrant muss es eine 1 geben
    # ("quadrant", "quadrant_num", "num")
    for i in range(1, NUM_TOT + 1):
        for j in range(1, NUM_TOT + 1):
            res.append(("quad", i, j))

    # Jedes Feld muss eine Zahl von 1 bis 4 haben
    # ("row", "col")
    for i in range(1, NUM_TOT + 1):
        for j in range(1, NUM_TOT + 1):
            res.append((i, j))

    return res


def generate_actions() -> List[Tuple]:
    # ("row", "col", "num")
    actions = []
    for i in range(1, NUM_TOT + 1):
        for j in range(1, NUM_TOT + 1):
            for k in range(1, NUM_TOT + 1):
                actions.append((i, j, k))

    actions = {action: map_action_to_requirements(action) for action in actions}
    return actions


def map_action_to_requirements(action: Tuple) -> List[Tuple]:
    row, col, num = action
    res = []
    res.append(("row", row, num))
    res.append(("col", col, num))
    res.append(("quad", (row - 1) // 2 * 2 + (col - 1) // 2 + 1, num))
    res.append((row, col))
    # res.append(("quad", row * 2 + col, num))
    return res


def print_output(solution: List[Tuple]):
    for row in range(1, NUM_TOT + 1):
        for col in range(1, NUM_TOT + 1):
            char = [x[2] for x in solution if x[0] == row and x[1] == col]
            print(char[0], end="")
        print()

    # ********************************************************


NUM_TOT = 4
solver = AlgoXSolver()

requirements = generate_requirements()
solver.create_header_row(requirements)

actions = generate_actions()
solver.add_action_rows(actions)

pre_actions = get_start_parameters()
for action in pre_actions:
    solver.execute_action(action)

solution = solver.solve()

solution = solution + pre_actions
print_output(solution)


# ------------------

# solver.create_header_row(["Hans", "Peter", "Sonia", "Joseph", "Manuel", "Max", "Nic"])
# solver.add_row("Mo", ["Hans", "Max", "Sonia"])
# solver.add_row("Di", ["Peter", "Manuel", "Nic", "Joseph"])
# solver.add_row("Mi", ["Sonia", "Manuel", "Nic"])
# solver.add_row("Do", ["Peter", "Hans", "Joseph"])
# solver.add_row("Fr", ["Joseph", "Nic"])

# solver.print_table()
# solver.execute_action("Mo")
# solver.print_table()

# r = solver.solve()
# print(r)

# -----------------------

# solver.create_header_row(["A", "B", "C", "D", "E", "F"])
# solver.add_row(1, ["A", "B", "E"])
# solver.add_row(2, ["A", "C", "E"])
# solver.add_row(3, ["B", "C", "D"])
# solver.add_row(4, ["C", "E", "F"])
# solver.add_row(5, ["A", "E", "F"])
# solver.print_table()
# solver.execute_action(5)
# r = solver.solve()
# print(r)
