maze = ["#.########", "#.##..####", "..##..#...", "####..#S##", "#....#####"]


def map_number_to_char(number):
    if number < 10:
        return str(number)
    else:
        return chr(ord("A") + number - 10)


def print_maze(maze, printFlag=False):
    result = []
    for row in range(max_row + 1):
        newRow = ""
        for col in range(max_col + 1):
            newRow += maze[(row, col)]
        result.append(newRow)

    if printFlag:
        for row in result:
            print(row)
        print()
        print()
    return result


def build_maze(maze):
    data = {}
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            p = (row, col)
            if char == "S":
                start = p
                data[p] = "."
            else:
                data[p] = char
    return data, start


def dfs(maze, start, steps):
    stack = [[start, steps]]
    while stack:
        current, steps = stack.pop(0)
        if maze[current] != ".":
            continue
        maze[current] = map_number_to_char(steps)
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row = (row + dr) % (max_row + 1)
            new_col = (col + dc) % (max_col + 1)
            new_pos = (new_row, new_col)
            if maze[new_pos] == ".":
                stack.append([new_pos, steps + 1])


maze, start = build_maze(maze)
max_row = max(row for row, _ in maze)
max_col = max(col for _, col in maze)

dfs(maze, start, 0)
print_maze(maze, True)
