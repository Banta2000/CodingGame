import sys
import math

HOME: bool = True


def get_input() -> list[tuple[str, int]]:
    if HOME:
        data = ["> 3", "v 2", "< 3", "^ 2"]
        data = ["< 6", "^ 4", "> 6", "v 4"]

        data = ["v 800", "> 1000", "^ 800", "< 300", "v 400", "< 400", "^ 400", "< 300"]

        # data = [
        #     "v 10",
        #     "< 10",
        #     "v 10",
        #     "< 10",
        #     "v 10",
        #     "> 10",
        #     "v 100",
        #     "> 50",
        #     "^ 70",
        #     "> 5",
        #     "^ 10",
        #     "> 5",
        #     "^ 5",
        #     "> 10",
        #     "^ 5",
        #     "> 10",
        #     "v 5",
        #     "> 10",
        #     "v 5",
        #     "> 5",
        #     "v 10",
        #     "> 5",
        #     "v 70",
        #     "> 50",
        #     "^ 100",
        #     "> 10",
        #     "^ 10",
        #     "< 10",
        #     "^ 10",
        #     "< 10",
        #     "^ 10",
        #     "< 130",
        # ]
    else:
        data = [input() for _ in range(int(input()))]
    data = [line.split() for line in data]
    data = [(direction, int(length)) for direction, length in data]
    return data


def return_corner_steps(pos, direction, length):
    step = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
    step = step[direction]
    steps = []
    if direction in ["<", ">"]:
        end_pos = (pos[0], pos[1] + length * step[1])
        steps.append(end_pos)
    else:
        for _ in range(length):
            pos = (pos[0] + step[0], pos[1] + step[1])
            steps.append(pos)
    return steps


def return_all_steps(pos, direction, length):
    step = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
    step = step[direction]
    steps = []
    for _ in range(length):
        pos = (pos[0] + step[0], pos[1] + step[1])
        steps.append(pos)
    return steps


def find_first_complete_line(contour):
    # Yields the first line that has only two points (start and stop) and no intersection in between
    min_row = min(x[0] for x in contour)
    max_row = max(x[0] for x in contour)
    for row in range(min_row, max_row + 1):
        cols = [x for x in contour if x[0] == row]
        if len(cols) == 2:
            cols = sorted(cols, key=lambda x: x[1])
            yield cols


def bfs(start_point, contour):
    stack = set()
    stack.add(start_point)
    visited = set()
    while stack:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)
        r, c = curr
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        neighbours = [n for n in neighbors if n not in visited and n not in contour and n not in stack]
        for n in neighbours:
            stack.add(n)
        print(len(visited))
    return len(visited)


data = get_input()
initial_pos = (0, 0)

# corners = []
# for line in data:
#     corners += return_corner_steps(initial_pos, *line)
#     initial_pos = corners[-1]

contour = []
for line in data:
    contour += return_all_steps(initial_pos, *line)
    initial_pos = contour[-1]

start_point, end_point = next(find_first_complete_line(contour))
mid_point = (start_point[0], (end_point[1] - start_point[1]) // 2 + start_point[1])
fill_size = bfs(mid_point, contour)
total_size = fill_size + len(contour)
print(total_size)
