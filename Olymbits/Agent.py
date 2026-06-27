class Agent:
    def __init__(self):
        True

    def get_action(self, medal_lst, inputs_lst):
        nb_games = 4

        utilities, utility = [], None
        points, points_this_game = [], None
        remaining_turns, remaining_turns_this_game = [], None
        medals = {}

        for i, score_info in enumerate(medal_lst):
            if i == 0:
                medals = get_medals(score_info)

        for i, inputs in enumerate(inputs_lst):
            inputs = inputs.split()

            # OBSTACLES
            if i == 0:
                GAME_OVER, track, pos, visibility, points_this_game, remaining_turns_this_game = (
                    get_OBSTACLES_variables(inputs)
                )
                utility = get_OBSTACLES_utility(GAME_OVER, visibility)
                # printGame("G1: Track", track, "Points", points_this_game, "Utility", utility)

            # ARCHERY
            if i == 1:
                GAME_OVER, p1, p2, p3, wind, points_this_game, remaining_turns_this_game = get_ARCHERY_variables(inputs)
                utility = get_ARCHERY_utility(GAME_OVER, wind, p1)
                # printGame("G2: PX PY Wind", (p1, wind), "Points", points_this_game, "Utility", utility)

            # SKATING
            if i == 2:
                GAME_OVER, points_this_game, risk_order, spaces_travelled, risks, remaining_turns_this_game = (
                    get_SCATING_variables(inputs)
                )
                utility = get_SCATING_utility(GAME_OVER, risk_order, spaces_travelled, risks)
                # printGame("G3: Pos, Risks, Seq",(spaces_travelled, risks, risk_order),"Points",points_this_game,"Utility",utility)

            # DIVING
            if i == 3:
                GAME_OVER, req_sequence, combo, points_this_game, remaining_turns_this_game = get_DIVING_variables(
                    inputs
                )
                utility = get_DIVING_utility(GAME_OVER, req_sequence)
                # printGame("G4: Sequence", req_sequence, "Points", points_this_game, "Utility", utility)

            utilities.append(utility)
            points.append(points_this_game)
            remaining_turns.append(remaining_turns_this_game)

        # myprint("")
        # myprint("Points", points)
        # myprint("Utilities", utilities)
        # myprint("")

        best_decision = decision_script(points, utilities, medals, remaining_turns)
        # myprint("")
        return best_decision


def myprint(*args):
    if len(args) == 2:
        name = args[0]
        value = args[1]
        name += " " * (25 - len(name))
        print(name, value)
        return
    print(*args)


def printGame(s1, p1, s2, p2, s3, p3):
    s1 = str(s1)
    s1 += " " * (25 - len(s1))
    p1 = str(p1)
    p1 += " " * (45 - len(p1))
    s2 = str(s2)
    s2 += " " * (8 - len(s2))
    p2 = str(p2)
    p2 += " " * (35 - len(p2))
    s3 = str(s3)
    s3 += " " * (8 - len(s3))
    p3 = str(p3)
    myprint(s1, p1, s2, p2, s3, p3)


def printMedals(medals):
    s = f'Medals                    Obstacles  {medals["OBSTACLES"][0]} {medals["OBSTACLES"][1]}       Archery  {medals["ARCHERY"][0]} {medals["ARCHERY"][1]}       Scating  {medals["SCATING"][0]} {medals["SCATING"][1]}    Diving  {medals["DIVING"][0]} {medals["DIVING"][1]}'
    myprint(s)
    myprint("")


def eucl_dist(p):
    return abs(p[0]) + abs(p[1])


def get_medals(D):
    D = D.split()
    D = [int(x) for x in D]
    medals = {"OBSTACLES": [D[1], D[3]], "ARCHERY": [D[4], D[6]], "SCATING": [D[7], D[9]], "DIVING": [D[10], D[12]]}
    return medals


# HELPER FUNCTIONS **************************************************************************************************


def normalize(vec, max_val):
    result = [x / max_val * 10 for x in vec]
    return result


def matrix_vector_multiplication(matrix, vector):
    result = []
    for row, weight in zip(matrix, vector):
        new_row = [element * weight for element in row]
        result.append(new_row)
    return result


# VARIABLES ********************************************************************************************************


def get_OBSTACLES_variables(inputs):
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

    track, pos = inputs[0], int(inputs[1])
    GAME_OVER = track == "GAME_OVER"
    points_this_game = [int(x) for x in inputs[1:4]]
    visibility = get_visibility(track, pos)
    pos1, pos2, pos3 = int(inputs[1]), int(inputs[2]), int(inputs[3])
    len_remaining = len(track) - max([pos1, pos2, pos3])
    remaining_turns = len_remaining // 2

    return GAME_OVER, track, pos, visibility, points_this_game, remaining_turns


def get_ARCHERY_variables(inputs):
    GAME_OVER = inputs[0] == "GAME_OVER"
    wind = inputs[0][0]
    wind = int(wind) if wind != "G" else 0
    p1, p2, p3 = (int(inputs[1]), int(inputs[2])), (int(inputs[3]), int(inputs[4])), (int(inputs[5]), int(inputs[6]))
    distances_per_player = [eucl_dist(x) for x in [p1, p2, p3]]
    points_this_game = [25 - x for x in distances_per_player]
    remaining_turns_this_game = len(inputs[0])
    return GAME_OVER, p1, p2, p3, wind, points_this_game, remaining_turns_this_game


def get_SCATING_variables(inputs):
    risk_order = inputs[0]
    GAME_OVER = inputs[0] == "GAME_OVER"
    points_this_game = [int(x) for x in inputs[1:4]]
    spaces_travelled = [int(x) for x in inputs[1:4]]
    risks = [int(x) for x in inputs[4:7]]
    remaining_turns_this_game = int(inputs[7])

    return GAME_OVER, points_this_game, risk_order, spaces_travelled, risks, remaining_turns_this_game


def get_DIVING_variables(inputs):
    req_sequence = inputs[0]
    GAME_OVER = req_sequence == "GAME_OVER"
    combo = inputs[4]
    remaining_turns_this_game = len(req_sequence)
    points_this_game = [int(inputs[1]), int(inputs[2]), int(inputs[3])]
    return GAME_OVER, req_sequence, combo, points_this_game, remaining_turns_this_game


# UTILITY FUNCTIONS *************************************************************************************************


def get_OBSTACLES_utility(GAME_OVER, vis):
    if GAME_OVER:
        return [0, 0, 0, 0]

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


def get_ARCHERY_utility(GAME_OVER, wind, p):
    if GAME_OVER:
        return [0, 0, 0, 0]

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

    result = [20 - x for x in distance_after_move]

    # result = [wind if x < curr_dist else penalty for x in distance_after_move]
    # result = [20 - x for x in result]

    result = normalize(result, 20)

    return result


def get_SCATING_utility(GAME_OVER, risk_order, spaces_travelled, risks):
    def simulate_landing_positions_for_other_players(positions, risks):
        result = set()
        for i in [1, 2]:
            pos, risk = positions[i], risks[i]
            # if the player is stunned, it's sture that the next position is the same
            if risk < 0:
                result.add(pos)
                continue
            # let's assume with equal probs the player moves 1, 2, or 3 steps
            for pos_delta in [1, 2, 3]:
                new_pos = (pos + pos_delta) % 10
                result.add(new_pos)
        return result

    if GAME_OVER:
        return [0, 0, 0, 0]

    result = {}
    possible_landings_of_other_players = simulate_landing_positions_for_other_players(spaces_travelled, risks)

    mypos, myrisk = spaces_travelled[0], risks[0]
    risk_order = list(risk_order)
    lookUp = [[1, -1], [2, 0], [2, 1], [3, 2]]  # [pos_advance, risk_modification]
    for move, (pos_delta, risk_delta) in zip(risk_order, lookUp):
        new_pos = mypos + pos_delta
        new_risk = myrisk + risk_delta

        # Assume worst case, we will collide, our risk will go up by 1
        if (new_pos % 10) in possible_landings_of_other_players:
            new_risk += 1

        # If we will be stunned, utility = -10 penalty
        if new_risk >= 5:
            new_utility = -10
        else:
            new_utility = pos_delta * 3 - new_risk

        result[move] = new_utility

    utility = [result[x] for x in ["U", "L", "D", "R"]]

    return utility


def get_DIVING_utility(GAME_OVER, req_sequence):
    if GAME_OVER:
        return [0, 0, 0, 0]

    # UP, LEFT, DOWN, RIGHT
    next_dir = req_sequence[0]
    results = {"U": [10, 0, 0, 0], "L": [0, 10, 0, 0], "D": [0, 0, 10, 0], "R": [0, 0, 0, 10], "G": [0, 0, 0, 0]}
    return results[next_dir]


# DECISION FUNCTIONS ************************************************************************************************


def which_place_did_I_win(points):
    if points[0] >= points[1] and points[0] >= points[2]:
        return 0
    else:
        return 1


def get_weight_based_on_ingame_position_vs_other_players(points):
    p1, p2, p3 = points
    dist1, dist2 = abs(p1 - p2), abs(p1 - p3)

    # distance to closest player
    dist_to_closest_player = min(dist1, dist2)

    # express closenes in percentage
    dist_to_closest_player = 0 if p1 == 0 else dist_to_closest_player / p1 * 100

    # Strategy 1: increase weight if closest player < 20% to me
    return 1.2 if dist_to_closest_player < 20 else 1.0

    # Strategy 2: increase weight if I am last one
    # if p1 < p2 and p1 < p3:
    # return 1.5
    return 1


def get_weight_based_on_medals(medals, sport):
    gold, bronze = 0, 1
    medals_for_this_game = medals[sport]
    # Strategy 1: weight == number of bronze medals; whoever has most bronze medals will dominante weight
    # result = medals_for_this_game[1]

    # Strategy 2: find which game has least gold; mute everyone else
    # min_gold = min([x[0] for x in medals.values()])
    # if medals_for_this_game[0] == min_gold:
    # result = 1
    # else:
    # result = 0

    # Strategy 3: find which game has most bronze; mute everyone else
    max_bronze = max([x[bronze] for x in medals.values()])
    result = 1.5 if medals_for_this_game[bronze] == max_bronze else 1.0
    return result


def get_weight_based_on_remaining_turns(remaining_turns):
    result = 1.5 if remaining_turns <= 5 else 1.0
    return result


def decision_script(points_matrix, utilities, medals, remaining_turns):
    # Only optimize for certain games (for testing)
    weight_vector = [1.0, 0.0, 0.0, 0.0]
    # myprint("w = f(filtering)", weight_vector)
    utilities = matrix_vector_multiplication(utilities, weight_vector)

    # Per-game analysis, weight based on my position vs position of the other two players
    # weight_vector = [get_weight_based_on_ingame_position_vs_other_players(x) for x in points_matrix]
    # myprint("w = f(points)", weight_vector)
    # utilities = matrix_vector_multiplication(utilities, weight_vector)

    # Cross-game analysis, weight based on number of medals
    # weight_vector = [
    # get_weight_based_on_medals(medals, sport) for sport in ["OBSTACLES", "ARCHERY", "SCATING", "DIVING"]
    # ]
    # myprint("w = f(medals)", weight_vector)
    # utilities = matrix_vector_multiplication(utilities, weight_vector)

    # Per game analysis, weight based on remaining turns; be more aggressive for games < 5 turns left
    # weight_vector = [get_weight_based_on_remaining_turns(x) for x in remaining_turns]
    # myprint("w = f(remaining turns)", weight_vector)
    # utilities = matrix_vector_multiplication(utilities, weight_vector)

    # Compute the total utility for each direction across all games
    sum_vec = [sum(x) for x in zip(*utilities)]
    # myprint("Resulting Utility", sum_vec)
    # myprint("")

    # Return instruction based on max utility
    max_value = max(sum_vec)
    max_index = sum_vec.index(max_value)
    lookUp = ["UP", "LEFT", "DOWN", "RIGHT"]
    # myprint("Decision", lookUp[max_index])
    return lookUp[max_index]
