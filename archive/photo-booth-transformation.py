import sys
import math

HOME_PC = True


def to_int(r, c, w):
    # Converts row and column to a single integer index
    return r * w + c


def to_coords(i, w):
    # Converts a single integer index back to row and column
    return i // w, i % w


def create_ABC_matrix(w, h):
    # Creates a matrix with dimensions w, h filled with letters A-Z
    # Uses 1D integer keys instead of 2D tuple keys
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    matrix = {}
    for i in range(w * h):
        matrix[i] = letters[i % len(letters)]
    return matrix


def print_matrix(curr_matrix, char_mapper, w, h):
    # curr_matrix is the current state of the mapping, each pos (key) looks up the original pos
    # char_mapper maps the original position to the character

    # This mapper is used to print ABC instead of numbers
    ABC_MAPPING = create_ABC_matrix(w, h)

    for r in range(h):
        for c in range(w):
            # Convert current 2D position to 1D integer key
            current_key = to_int(r, c, w)
            # Get the original position (which should also be a 1D integer)
            original_pos = curr_matrix[current_key]
            # Get the character from the ABC mapping
            original_char = ABC_MAPPING[original_pos]
            print(original_char, end="")
        print()
    print()


def build_new_matrix_from_groups(groups, w):
    def umformen(group, w):
        res = []
        tmp = []
        i = 0
        for i, ele in enumerate(group):
            tmp.append(ele)
            if (i + 1) % (w // 2) == 0:
                res.append(tmp)
                tmp = []
        return res

    up_left = [line[0] for line in groups]
    up_left = umformen(up_left, w)

    up_right = [line[1] for line in groups]
    up_right = umformen(up_right, w)

    bottom_left = [line[2] for line in groups]
    bottom_left = umformen(bottom_left, w)

    bottom_right = [line[3] for line in groups]
    bottom_right = umformen(bottom_right, w)

    end_res = []
    for line_links, line_rechts in zip(up_left, up_right):
        end_res.append(line_links + line_rechts)
    for line_links, line_rechts in zip(bottom_left, bottom_right):
        end_res.append(line_links + line_rechts)

    # Flatten the 2D array and create dictionary with 1D indices
    flattened = [char for row in end_res for char in row]
    dict_form = {i: char for i, char in enumerate(flattened)}

    return dict_form


def build_mapper(w, h):
    # Creates a mapper with dimensions w, h that matches the original matrix to its transformation
    # Use 1D indexing instead of 2D tuples
    M = {i: i for i in range(w * h)}

    # Divide the matrix into groups of four
    groups_of_four = []
    for row in range(0, h, 2):
        for col in range(0, w, 2):
            # Convert 2D coordinates to 1D indices for the group
            top_left = to_int(row + 0, col + 0, w)
            top_right = to_int(row + 0, col + 1, w)
            bottom_left = to_int(row + 1, col + 0, w)
            bottom_right = to_int(row + 1, col + 1, w)
            tmp = [M[top_left], M[top_right], M[bottom_left], M[bottom_right]]
            groups_of_four.append(tmp)

    mapper = build_new_matrix_from_groups(groups_of_four, w)

    # Inverse the mapper
    inverse_mapper = {v: k for k, v in mapper.items()}
    return inverse_mapper


def transform(matrix, mapper):
    # Transforms the matrix according to the mapper
    transformed_matrix = {}
    for curr_pos, value in matrix.items():
        new_pos = mapper[curr_pos]
        transformed_matrix[new_pos] = value
    return transformed_matrix


def is_back_to_original(matrix):
    # Checks if the matrix is back to its original state
    for pos, value in matrix.items():
        if pos != value:
            return False
    return True


def find_cycle_length1(dimensions):
    w, h = dimensions
    mapper = build_mapper(w, h)

    M = {(r, c): (r, c) for r in range(h) for c in range(w)}
    M = transform(M, mapper)

    i = 1
    while not is_back_to_original(M):
        i += 1
        M = transform(M, mapper)

    print(i)


def find_cycle_length2(dimensions):
    # This function finds the cycle length for each element in the matrix, it analyzes the cycle length of every pos individually
    w, h = dimensions
    mapper = build_mapper(w, h)

    # Use 1D indexing instead of 2D tuples
    M = {i: i for i in range(w * h)}
    cycle_lengths = set()
    visited_collection = set()
    for i, pos in enumerate(M):
        if pos not in visited_collection:
            cycle_length, visited = find_cycle_for_one_element(mapper, pos)
            cycle_lengths.add(cycle_length)
            visited_collection.update(visited)
            # Breaking after 100 iterations to avoid long runs
            if i > 2000:
                break
    lcm = find_lcm(cycle_lengths)
    print(lcm)


def find_cycle_for_one_element(mapper, orig_pos):
    # Finds the cycle length for the element pos
    visited = set()
    visited.add(orig_pos)
    i = 1
    pos = mapper[orig_pos]
    while pos != orig_pos:
        i += 1
        pos = mapper[pos]
        visited.add(pos)
    return i, visited


def find_lcm(nums: set[int]) -> int:
    # Finds the least common multiple of a set of numbers
    if not nums:
        return 1
    lcm = 1
    for num in nums:
        lcm = lcm * num // math.gcd(lcm, num)
    return lcm


# ***********************************************************

if HOME_PC:
    data = [[6, 4], [4, 6]]
    data = [[1716, 638], [462, 110], [1178, 1632]]
    # data = [[84, 354], [368, 336], [344, 70], [98, 486], [32, 274], [100, 338], [434, 62]]

else:
    lines = int(input())
    data = [input() for _ in range(lines)]
    data = [line.split() for line in data]
    data = [[int(x) for x in line] for line in data]

for line in data:
    find_cycle_length2(line)
