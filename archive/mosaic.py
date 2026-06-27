def parseGrid(grid):
    instructions = {}
    new_grid = {}
    for row in range(len(grid)):
        for col in range(len(grid)):
            p = (row, col)
            c = grid[row][col]
            instructions[p] = c if c == "." else int(c)
            new_grid[p] = "?"
    return instructions, new_grid


def get_unfiltered_neighbours(grid, p):
    r, c = p
    res = [
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1),
        (r, c - 1),
        (r, c),
        (r, c + 1),
        (r + 1, c - 1),
        (r + 1, c),
        (r + 1, c + 1),
    ]
    res = [x for x in res if x in grid]
    return set(res)


def get_filled(grid):
    res = [k for k, v in grid.items() if v == "#"]
    return set(res)


def get_empty(grid):
    res = [k for k, v in grid.items() if v == "."]
    return set(res)


def get_instructions(grid):
    res = [k for k, v in grid.items() if v != "."]
    return set(res)


def solve_one_field(grid, instructions, p):
    # get all possible candidates
    candidates = get_unfiltered_neighbours(grid, p)

    # amount of fields to be filled (instructions) minus existing filled fields
    num_to_be_filled = instructions[p] - len(candidates & get_filled(grid))

    # substract fields covered that are filled or empty
    candidates = candidates - get_filled(grid)
    candidates = candidates - get_empty(grid)

    if num_to_be_filled == len(candidates):
        for candidate in candidates:
            grid[candidate] = "#"

    # get all possible candidates
    candidates = get_unfiltered_neighbours(grid, p)

    # amount of fields to be empty (instructions) minus existing empty fields
    num_to_be_empty = len(candidates) - instructions[p] - len(candidates & get_empty(grid))

    # substract fields covered that are filled or empty
    candidates = candidates - get_filled(grid)
    candidates = candidates - get_empty(grid)

    if num_to_be_empty == len(candidates):
        for candidate in candidates:
            grid[candidate] = "."

    # If we have solved this field entirely, delete it from the instructions
    candidates = get_unfiltered_neighbours(grid, p)
    candidates = candidates - get_filled(grid)
    candidates = candidates - get_empty(grid)
    if len(candidates) == 0:
        instructions[p] = "."

    return grid, instructions


def clean_grid(grid):
    for p in grid:
        if grid[p] == "?":
            grid[p] = "."
    return grid


def print_grid(grid):
    for r in range(SIZE):
        for c in range(SIZE):
            p = (r, c)
            print(grid[p], end="")
        print()


# ***********************************


# SIZE = int(input())
# grid = []
# for i in range(SIZE):
#     grid.append(input())


SIZE = 3
grid = ["0..", ".5.", "..."]

instructions, grid = parseGrid(grid)

while len(get_instructions(instructions)) > 0:
    fields_with_instructions = get_instructions(instructions)
    for p in fields_with_instructions:
        grid, instructions = solve_one_field(grid, instructions, p)


print_grid(grid)
