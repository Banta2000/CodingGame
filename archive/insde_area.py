from math import atan2, degrees

HOME: bool = True
DEBUG: bool = True

loopLookUp = {
    "U": ["U", "R", "D"],
    "R": ["R", "D", "L"],
    "D": ["D", "L", "U"],
    "L": ["L", "U", "R"],
}

reverseLoopLookup = {
    ("U", "R", "D"): "U",
    ("R", "D", "L"): "R",
    ("D", "L", "U"): "D",
    ("L", "U", "R"): "L",
}


def createFullCircumference(instructions):
    r, c = 0, 0
    graph = [(r, c)]
    delta = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    for line in instructions:
        dir, length = line
        rDelta, cDelta = delta[dir]
        for _ in range(length):
            r += rDelta
            c += cDelta
            graph.append((r, c))
    return graph


def createGraphPart1(instructions):
    r, c = 0, 0
    graph = {}
    delta = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    for line in instructions:
        dir, length, col = line
        rDelta, cDelta = delta[dir]
        for i in range(length):
            r += rDelta
            c += cDelta
            p = (r, c)
            graph[p] = col
    minRow = min([x[0] for x in graph.keys()])
    maxRow = max([x[0] for x in graph.keys()])
    minCol = min([x[1] for x in graph.keys()])
    maxCol = max([x[1] for x in graph.keys()])
    return graph, minRow, maxRow, minCol, maxCol


def printAll(graph):
    minRow = min([x[0] for x in graph.keys()])
    maxRow = max([x[0] for x in graph.keys()])
    minCol = min([x[1] for x in graph.keys()])
    maxCol = max([x[1] for x in graph.keys()])

    for r in range(minRow, maxRow + 1):
        for c in range(minCol, maxCol + 1):
            p = (r, c)
            if p == (0, 0):
                print("O", end="")
                continue
            if p in graph:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def getNeighbours(p, graph):
    r, c = p
    neighbours = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    neighbours = [x for x in neighbours if x not in graph]
    return neighbours


def part1(instructions):
    graph, minRow, maxRow, minCol, maxCol = createGraphPart1(instructions)
    print(minRow, maxRow, minCol, maxCol)

    start = (0, 20)
    stack = [start]

    while stack:
        p = stack.pop(0)
        if p in graph:
            continue
        else:
            graph[p] = "."
        neighbours = getNeighbours(p, graph)
        for n in neighbours:
            stack.append(n)

    printAll(graph)
    print("Part 1", len(graph))


def createCornerStones(instructions):
    r, c = 0, 0
    cornerStones = []
    delta = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    for line in instructions:
        dir, length = line
        rDelta, cDelta = delta[dir]
        r += rDelta * length
        c += cDelta * length
        p = (r, c)
        cornerStones.append(p)
    return cornerStones


# drop the col part, only keep the first two
def rewriteInstructionsPart2(instructions):
    result = []
    lookUp = {"0": "R", "1": "D", "2": "L", "3": "U"}
    for line in instructions:
        _, _, line = line
        part1, part2 = line[1:6], line[-1]
        part1 = int(part1, 16)
        part2 = lookUp[part2]
        result.append((part2, int(part1)))
    return result


# drop the col part, only keep the first two
def rewriteInstructionsPart1(instructions):
    newInstructions = [(x[0], x[1]) for x in instructions]
    return newInstructions


def printInstructions(instructions):
    print()
    circumference = createFullCircumference(instructions)

    minRow, maxRow = min([x[0] for x in circumference]), max([x[0] for x in circumference])
    minCol, maxCol = min([x[1] for x in circumference]), max([x[1] for x in circumference])

    # maxRow = minRow + 20
    for r in range(minRow, maxRow + 1):
        for c in range(minCol, maxCol + 1):
            p = (r, c)
            if p in circumference:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()


def needToAbort(instructions, i, direction):
    forbiddenDirection = {"U": "L", "R": "U", "D": "R", "L": "D"}
    forbidden = forbiddenDirection[direction]

    dir1, len1 = instructions[i - 1]
    dir2, len2 = instructions[i + 0]
    dir3, len3 = instructions[(i + 1) % len(instructions)]
    dir4, len4 = instructions[(i + 2) % len(instructions)]
    dir5, len5 = instructions[(i + 3) % len(instructions)]

    if len2 == len4 and (dir1 == forbidden or dir5 == forbidden):
        return True

    if len2 < len4 and dir1 == forbidden:
        return True

    if len2 > len4 and dir5 == forbidden:
        return True

    return False


def cutLoop(instructions, i, direction):
    leg1, leg2, leg3 = loopLookUp[direction]

    i1 = (i + 0) % len(instructions)
    i2 = (i + 1) % len(instructions)
    i3 = (i + 2) % len(instructions)

    dir1, len1 = instructions[i1]
    dir2, len2 = instructions[i2]
    dir3, len3 = instructions[i3]

    lostArea = 0
    if len1 == len3:
        lostArea = (len1) * (len2 - 1)
        newPiece = [(leg2, len2)]
    if len1 > len3:
        lostArea = (len3) * (len2 - 1)
        newPiece = [(leg1, len1 - len3), (leg2, len2)]
    if len3 > len1:
        lostArea = (len1) * (len2 - 1)
        newPiece = [(leg2, len2), (leg3, len3 - len1)]

    for x in sorted([i1, i2, i3], reverse=True):
        del instructions[x]

    insert_i = i
    if i2 == 0:
        insert_i -= 2
    elif i3 == 0:
        insert_i -= 1
    else:
        insert_i = insert_i

    instructions = instructions[:insert_i] + newPiece + instructions[insert_i:]

    instructions = cleanInstructions(instructions)
    return instructions, lostArea


def cleanInstructions(lst):
    def flipIfNeeded(ins):
        if ins[1] < 0:
            print("SOLLTE NICH PASSIEREN")
            return opposite[ins[0]], -ins[1]
        else:
            return ins

    opposite = {"U": "D", "D": "U", "L": "R", "R": "L"}

    merged_lst = [lst[0]]

    i = 1
    while i < len(lst):
        dir1, num1 = merged_lst[-1]
        dir2, num2 = lst[i]
        if dir1 == dir2:
            merged_lst[-1] = (dir1, num1 + num2)
        elif dir2 == opposite[dir1]:
            print("SOLLTE NICH PASSIEREN")
            merged_lst[-1] = (dir1, num1 - num2)
        else:
            merged_lst.append((dir2, num2))
        merged_lst[-1] = flipIfNeeded(merged_lst[-1])
        i += 1
    return merged_lst


def findAllLoops(instructions, direction):
    res = []

    for i in range(len(instructions) - 2):
        i1, i2, i3 = instructions[i : i + 3]
        dir1, len1 = i1
        dir2, len2 = i2
        dir3, len3 = i3
        if [dir1, dir2, dir3] == loopLookUp[direction]:
            res.append(i)
    return res


def checkIfThisIsValidLoop(instructions, i):
    i1 = (i + 0) % len(instructions)
    i2 = (i + 1) % len(instructions)
    i3 = (i + 2) % len(instructions)

    dir1, len1 = instructions[i1]
    dir2, len2 = instructions[i2]
    dir3, len3 = instructions[i3]

    if (dir1, dir2, dir3) not in reverseLoopLookup:
        return False

    dir = reverseLoopLookup[(dir1, dir2, dir3)]

    if needToAbort(instructions, i, dir):
        return False

    # Check if the loop will not enter another line's field
    startPoint = calculateEndPoint(instructions[:i1])
    endPoint = calculateEndPoint(instructions[:i3])
    minRow, maxRow = min([startPoint[0], endPoint[0]]), max([startPoint[0], endPoint[0]])
    minCol, maxCol = min([startPoint[1], endPoint[1]]), max([startPoint[1], endPoint[1]])

    cornerPoints = createCornerStones(instructions)
    for p in cornerPoints:
        if minRow < p[0] < maxRow and minCol < p[1] < maxCol:
            return False

    return dir


def calculateCircumference(instructions):
    return sum([x[1] for x in instructions])


def calculateFinalCube(instructions):
    l = instructions[0][1]
    b = instructions[1][1]
    return (l - 1) * (b - 1)


def doOneRound(instructions):
    totalLostArea = 0
    i = 0
    while i < len(instructions):
        dir = checkIfThisIsValidLoop(instructions, i)
        if dir:
            instructions, lostArea = cutLoop(instructions, i, dir)
            totalLostArea += lostArea
            i -= 1
        i += 1
    return instructions, totalLostArea


def checkIfCircumferenceIsClosed(instructions):
    p = calculateEndPoint(instructions)
    if p != (0, 0):
        print("Circumference is not closed")


def calculateEndPoint(instructions):
    delta = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    r, c = 0, 0
    for line in instructions:
        dir, length = line
        rDelta, cDelta = delta[dir]
        r += rDelta * length
        c += cDelta * length
    return (r, c)


def get_input() -> list[tuple[str, int]]:
    if HOME:
        # data = ["> 3", "v 2", "< 3", "^ 2"] # Solution 12
        # data = ["> 4", "v 3", "< 4", "^ 3"]  # Solution 20
        # data = ["< 6", "^ 4", "> 6", "v 4"]  # Solution 35
        # data = ["^ 5", "> 2", "v 2", "> 2", "^ 2", "> 2", "v 5", "< 6"]  # Burg Solution 40
        # data = ["^ 3", "> 2", "^ 2", "> 2", "v 2", "> 2", "v 3", "< 6"]  # Hut Solution 34
        # data = ["v 800", "> 1000", "^ 800", "< 300", "v 400", "< 400", "^ 400", "< 300"]  # Solution 642201

        # data = ["^ 1000", "< 1000", "^ 1000", "< 1000", "v 3000", "> 1000", "^ 1000", "> 1000"]  # Solution 4005001
        data = ["^ 10", "< 10", "^ 10", "< 10", "v 30", "> 10", "^ 10", "> 10"]  # Solution 4005001

        # Solution: 15791
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

        data = [
            "> 461937",
            "v 56407",
            "> 356671",
            "v 863240",
            "> 367720",
            "v 266681",
            "< 577262",
            "^ 829975",
            "< 112010",
            "v 829975",
            "< 491645",
            "^ 686074",
            "< 5411",
            "^ 500254",
        ]

    else:
        data = [input() for _ in range(int(input()))]
    data = [line.split() for line in data]
    data = [(direction, int(length)) for direction, length in data]
    LU = {"^": "U", "v": "D", "<": "L", ">": "R"}
    data = [(LU[direction], length) for direction, length in data]
    return data


def reverse_instructions(instructions):
    LU = {"D": "U", "U": "D", "L": "R", "R": "L"}
    instructions = instructions[::-1]
    instructions = [(LU[direction], length) for direction, length in instructions]
    return instructions


def angle_between_points(p1, p2):
    # Returns the angle in degrees between two points p1 and p2
    x, y = p1[1], p1[0]
    angle = atan2(y, x)
    deg1 = degrees(angle)

    x, y = p2[1], p2[0]
    angle = atan2(y, x)
    deg2 = degrees(angle)

    res = deg2 - deg1
    return res


def calculate_all_delta_angles(instructions):
    # Returns a list of angles between all points in the instructions
    # TODO we can change this to only use the corner points, we don't need the full circumference
    contour = createFullCircumference(instructions)
    angles = []
    for i in range(1, len(contour) - 2):
        p1 = contour[i]
        p2 = contour[i + 1]
        angle = angle_between_points(p1, p2)
        angles.append(angle)
    return sum(angles)


# *****************************************************


instructions = get_input()
copy_of_instructions = instructions.copy()

instructions = reverse_instructions(instructions)
circumference = calculateCircumference(instructions)

i = 0
totalLostArea = 0
while len(instructions) != 4:
    checkIfCircumferenceIsClosed(instructions)
    instructions, deltaLost = doOneRound(instructions)
    totalLostArea += deltaLost
    i += 1
    if i > 100:
        # My algorithm only works in one direction of painting (clock-wise), if the direction is not correct, the loop never ends
        # I use this chip trick to invert the direction of the painting (from CCW to CW) if I notice that I'm in a infinite loop
        instructions = copy_of_instructions
        totalLostArea = 0
        i = 0


# printInstructions(instructions)
finalCube = calculateFinalCube(instructions)
print(circumference + totalLostArea + finalCube)
