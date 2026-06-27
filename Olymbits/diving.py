def lookahead_strategy(current_sequence, goal_sequence):
    best_action = None
    best_score = -float("inf")

    for action in ["U", "L", "D", "R"]:
        simulated_sequence = current_sequence + action

        # Evaluate how well simulated_sequence matches goal_sequence
        score = evaluate_match(simulated_sequence, goal_sequence)

        if score > best_score:
            best_score = score
            best_action = action

    return best_action


def evaluate_match(simulated_sequence, goal_sequence):
    # Example evaluation function (customize based on your scoring logic)
    score = 0
    for i in range(min(len(simulated_sequence), len(goal_sequence))):
        if simulated_sequence[i] == goal_sequence[i]:
            score += 1  # Increase score for each matching character

    return score


def lookahead_strategy_with_combo(current_sequence, goal_sequence, current_combo):
    best_action = None
    best_score = -float("inf")

    for action in ["U", "L", "D", "R"]:
        simulated_sequence = current_sequence + action

        # Evaluate how well simulated_sequence matches goal_sequence
        score = evaluate_match(simulated_sequence, goal_sequence)

        # Adjust score based on combo management
        score += current_combo  # Example: Consider current combo as bonus

        if score > best_score:
            best_score = score
            best_action = action

    return best_action


# Example usage:
current_sequence = "ULD"
goal_sequence = "ULDR"
current_combo = 2  # Example of current combo multiplier

best_action = lookahead_strategy_with_combo(current_sequence, goal_sequence, current_combo)
print("Best Action to Take:", best_action)


result = 1 if medals_for_this_game["bronze"] == max_bronze else 0

return result
