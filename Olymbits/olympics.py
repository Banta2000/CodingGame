# BILD  -  ZAHL
# Wenn ich die Zahl zum Bild sehen will, RIGHT
# Wenn ich das Bild zur Zahl sehen will, LEFT
# UP, LEFT, DOWN, RIGHT


def myprint(*args):
    if len(args) == 2:
        name = args[0]
        value = args[1]
        name += " " * (20 - len(name))
        print(name, value, file=sys.stderr, flush=True)
        return
    print(*args, file=sys.stderr, flush=True)


def eucl_dist(p):
    return abs(p[0]) + abs(p[1])


def get_visibility(track, pos):
    end_i = len(track) - 1
    visibility = end_i - pos
    visibility = min(4, visibility)
    result = track[pos + 1 : pos + visibility]

    if len(result) == 0:
        result = result + "..."
    if len(result) == 1:
        result = result + ".."
    if len(result) == 2:
        result = result + "."
    return result


def get_OBSTACLES_utility(vis):
    # UP, LEFT, DOWN, RIGHT
    penalty = -4
    if vis[0] == "#":
        result = [2, penalty, penalty, penalty]
    elif vis[1] == "#":
        result = [penalty, 1, penalty, penalty]
    elif vis[2] == "#":
        result = [2, 1, 2, penalty]
    else:
        result = [2, 1, 2, 3]
    result = normalize(result, 4)
    return result


def get_ARCHERY_utility(wind, p):
    # UP, LEFT, DOWN, RIGHT
    # Important: y upwards is negative, y downwards is positive
    penalty = -4
    px, py = p

    curr_dist = eucl_dist(p)

    U = [px, py - wind]
    L = [px - wind, py]
    D = [px, py + wind]
    R = [px + wind, py]

    distance_after_move = [eucl_dist(x) for x in [U, L, D, R]]
    result = [wind if x < curr_dist else penalty for x in distance_after_move]
    result = normalize(result, 10)
    # result = [20 - x for x in result]
    return result


def get_DIVING_utility(req_sequence):
    # UP, LEFT, DOWN, RIGHT
    next_dir = req_sequence[0]
    results = {"U": [10, 0, 0, 0], "L": [0, 10, 0, 0], "D": [0, 0, 10, 0], "R": [0, 0, 0, 10], "G": [0, 0, 0, 0]}
    return results[next_dir]


def normalize(vec, max_val):
    result = [x / max_val * 10 for x in vec]
    return result


def matrix_factor_multiplication(num, lst):
    result = [element * num for element in lst]
    return result


def get_best_decision(points, utilities):
    weights = [get_weight_based_on_position(x) for x in points]
    myprint("Weights", weights)
    utilities = [matrix_factor_multiplication(weight, utility) for weight, utility in zip(weights, utilities)]
    myprint("Util after weights", utilities)

    # Compute the total utility for each direction across all games
    sum_vec = [sum(x) for x in zip(*utilities)]

    # Find max index
    max_value = max(sum_vec)
    max_index = sum_vec.index(max_value)
    lookUp = ["UP", "LEFT", "DOWN", "RIGHT"]
    myprint("Decision", lookUp[max_index])
    return lookUp[max_index]


def get_weight_based_on_position(points):
    if points[0] < points[1] and points[0] < points[2]:
        return 2
    return 1


def which_place_did_I_win(points):
    if points[0] >= points[1] and points[0] >= points[2]:
        return 0
    else:
        return 1


def get_OBSTACLES_variables(input):
    track, pos = input[0], int(input[1])
    GAME_OVER = track == "GAME_OVER"
    points_this_game = [int(x) for x in inputs[1:4]]
    visibility = get_visibility(track, pos)
    return GAME_OVER, track, pos, visibility, points_this_game


def get_ARCHERY_variables(input):
    GAME_OVER = input[0] == "GAME_OVER"
    wind = input[0][0]
    wind = int(wind) if wind != "G" else 0
    p1, p2, p3 = (int(input[1]), int(input[2])), (int(input[3]), int(input[4])), (int(input[5]), int(input[6]))
    distances_per_player = [eucl_dist(x) for x in [p1, p2, p3]]
    points_this_game = [25 - x for x in distances_per_player]
    return GAME_OVER, p1, p2, p3, wind, points_this_game


def get_SCATING_variables(input):
    orders = input[0]
    GAME_OVER = input[0] == "GAME_OVER"
    points_this_game = [int(x) for x in inputs[1:4]]
    return GAME_OVER, orders, points_this_game


def get_DIVING_variables(input):
    req_sequence = input[0]
    GAME_OVER = req_sequence == "GAME_OVER"
    combo = inputs[4]
    points_this_game = [int(inputs[1]), int(inputs[2]), int(inputs[3])]
    return GAME_OVER, req_sequence, combo, points_this_game


def update_medals(medals, sport_name, points):
    myprint("finished a game", sport_name, points)

    place = which_place_did_I_win(points)
    myprint("finished at place", place)
    medals[sport_name][place] += 1
    return medals


import sys
import math

player_idx = int(input())
nb_games = int(input())
medals = {"OBSTACLES": [0, 0], "ARCHERY": [0, 0], "SCATING": [0, 0], "DIVING": [0, 0]}


while True:
    for i in range(3):
        score_info = input()

    utilities = []
    points = []
    for i in range(nb_games):
        inputs = input().split()

        # OBSTACLES
        if i == 0:
            GAME_OVER, track, pos, visibility, points_this_game = get_OBSTACLES_variables(inputs)
            if GAME_OVER:
                medals = update_medals(medals, "OBSTACLES", points_this_game)
            else:
                utility = get_OBSTACLES_utility(visibility)
            # myprint("Track", track)
            # myprint("Points", points_this_game)
            # myprint("Utility", utility)
            # utilities.append(utility)
            # points.append(points_thisgame)

        # ARCHERY
        if i == 1:
            myprint("")
            GAME_OVER, p1, p2, p3, wind, points_this_game = get_ARCHERY_variables(inputs)
            if GAME_OVER:
                medals = update_medals(medals, "ARCHERY", points_this_game)
            else:
                utility = get_ARCHERY_utility(wind, p1)
            # myprint("PX PY Wind, Dist", (p1, wind, distances))
            # myprint("Points", points_this_game)
            # myprint("Utility", utility)
            # utilities.append(utility)
            # points.append(points_thisgame)

        # SKATING
        if i == 2:
            GAME_OVER, orders, points_this_game = get_SCATING_variables(inputs)
            if GAME_OVER:
                medals = update_medals(medals, "SCATING", points_this_game)
            else:
                True
                # myprint("SCATING", GAME_OVER)

        # DIVING
        if i == 3:
            myprint("")
            GAME_OVER, req_sequence, combo, points_this_game = get_DIVING_variables(inputs)
            if GAME_OVER:
                medals = update_medals(medals, "DIVING", points_this_game)
            else:
                utility = get_DIVING_utility(req_sequence)
                # myprint("Req Sequence", req_sequence)
                # myprint("Points", points_this_game)
                # myprint("Utility", utility)
                utilities.append(utility)
                points.append(points_this_game)

    myprint("")
    # myprint("POINTS", points)
    # myprint("UTILITIES", utilities)

    best_decision = get_best_decision(points, utilities)
    print(best_decision)

    myprint(medals)
