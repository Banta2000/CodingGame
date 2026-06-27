def precompute_dp_table(track):
    n = len(track)
    dp = [float("inf")] * n
    move = [""] * n

    # Initial state
    dp[0] = 0
    move[0] = "START"

    for i in range(n):
        if i + 1 < n:
            cost_up = 2 if track[i + 1] == "." else float("inf")
            if dp[i] + cost_up < dp[i + 1]:
                dp[i + 1] = dp[i] + cost_up
                move[i + 1] = "UP"
        if i + 2 < n:
            cost_left = 1 if track[i + 2] == "." else float("inf")
            if dp[i] + cost_left < dp[i + 2]:
                dp[i + 2] = dp[i] + cost_left
                move[i + 2] = "LEFT"
        if i + 3 < n:
            cost_down = 2 if track[i + 3] == "." else float("inf")
            if dp[i] + cost_down < dp[i + 3]:
                dp[i + 3] = dp[i] + cost_down
                move[i + 3] = "DOWN"
        if i + 4 < n:
            cost_right = 3 if track[i + 4] == "." else float("inf")
            if dp[i] + cost_right < dp[i + 4]:
                dp[i + 4] = dp[i] + cost_right
                move[i + 4] = "RIGHT"

    return dp, move


def get_next_move(position, move):
    return move[position]


# Example track
track = [".", ".", "#", ".", ".", "#", ".", ".", ".", "#"]
dp, move = precompute_dp_table(track)

print(dp)

# Initial position
position = 0

# while position < len(track) - 1:
#     next_move = get_next_move(position, move)
#     print(f"At position {position}, making move: {next_move}")

#     # Update position based on the move
#     if next_move == "UP":
#         position += 1
#     elif next_move == "LEFT":
#         position += 2
#     elif next_move == "DOWN":
#         position += 3
#     elif next_move == "RIGHT":
#         position += 4

#     # Check if game over or reached the end
#     if position >= len(track):
#         print("Reached the end of the track!")
#         break
#     if track[position] == "#":
#         print("Hit a hurdle!")
#         break
