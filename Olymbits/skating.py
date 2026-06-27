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

    # result = []
    # if current_risk < 0:
    #     return [[current_position, current_risk+1]]

    # for i in range(4):
    #     action = risks[i]
    #     if action == "U":
    #         move_distance = 1
    #         risk_change = -1
    #     elif action == "L":
    #         move_distance = 2
    #         risk_change = 0
    #     elif action == "D":
    #         move_distance = 2
    #         risk_change = 1
    #     elif action == "R":
    #         move_distance = 3
    #         risk_change = 2

    # spaces_traveled = current_state[f"reg{player_idx}"]
    # risk_or_stun_timer = current_state[f"reg{player_idx + 3}"]

    # new_risk = risk_or_stun_timer + risk_change
    # new_position = (spaces_traveled + move_distance) % 10

    # return new_position, new_risk


def check_collisions(simulated_positions, simulated_risks):
    collisions = set()
    for i in range(len(simulated_positions)):
        for j in range(i + 1, len(simulated_positions)):
            if simulated_positions[i] == simulated_positions[j]:
                collisions.add(i)
                collisions.add(j)
    return collisions


def get_SCATING_utility(current_state, risk_order):
    num_players = 3  # Assuming 3 players
    utilities = [0, 0, 0, 0]  # UP, LEFT, DOWN, RIGHT
    simulated_positions = [0] * num_players
    simulated_risks = [0] * num_players

    for player_idx in range(num_players):
        action = risk_order[player_idx]
        new_position, new_risk = simulate_player_movement(current_state, action, player_idx)
        simulated_positions[player_idx] = new_position
        simulated_risks[player_idx] = new_risk

    collisions = check_collisions(simulated_positions, simulated_risks)

    for i, action in enumerate(risk_order):
        if i in collisions:
            utilities[i] -= 20  # Penalize for collision

    return utilities


# # Example usage:
# current_state = {"reg0": 2, "reg1": 9, "reg2": 21, "reg3": 4, "reg4": -1, "reg5": 0, "reg6": 14}
# risk_order = "ULDR"

# utilities = get_SCATING_utility(current_state, risk_order)
# print(utilities)  # Output: [utility for UP, utility for LEFT, utility for DOWN, utility for RIGHT]


risks = "ULDR"

mypos, myrisk = spaces_travelled[0], risks[0]
risks = list(risks)
# list_entry: [advance, risk_modificator]
lookUp = [[1, -1], [2, 0], [2, 1], [3, 2]]
result = {}
for move, (pos_delta, risk_delta) in zip(risks, lookUp):
    new_pos = mypos + pos_delta
    new_risk = myrisk + risk_delta
    # Utility starts with position advancement * 3 minus new risk
    new_utility = pos_delta * 3
    new_utility -= new_risk
    # If we have a chance of collission (unweighted) we penalize with -2
    if new_pos in simulate_landing_positions_for_other_players(spaces_travelled, risks):
        new_utility -= 2
    # If we know we are going to be stunned, we penalize with -10
    if new_risk >= 5:
        new_utility -= 10
    result[move] = new_utility
