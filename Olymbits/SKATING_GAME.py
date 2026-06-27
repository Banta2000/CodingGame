import random


class SKATING_GAME:
    def __init__(self):
        self.numPlayers = 3
        self.GAME_OVER = False
        self.medals = [{"gold": 0, "silver": 0, "bronze": 0} for _ in range(self.numPlayers)]
        self.reset()

    def reset(self):
        self.order = ["D", "L", "R", "U"]
        random.shuffle(self.order)
        self.counter = 15
        self.player_pos = [0, 0, 0]
        self.player_risk = [0, 0, 0]

    def printGame(self):
        print("Rounds", self.counter)
        print("Order", "".join(self.order))
        for i in range(self.numPlayers):
            print("P", i, ":", self.player_pos[i], self.player_risk[i])
        print()

    def printMedals(self):
        for entry in self.medals:
            print(entry)

    def visualizeGame(self):
        def visualize_one_player(pos, risk):
            RESETCOL = "\x1b[0m"
            RED = "\033[91m"
            GREEN = "\033[92m"
            for i in range(10):
                if i == pos:
                    if risk < 0:
                        print(RED + str(abs(risk)) + RESETCOL, end="")
                    else:
                        print(GREEN + str(abs(risk)) + RESETCOL, end="")
                else:
                    print(".", end="")
            print()

        for i in range(self.numPlayers):
            visualize_one_player(self.player_pos[i] % 10, self.player_risk[i])

    def get_state(self):
        if self.GAME_OVER:
            start = "GAME_OVER"
        else:
            start = "".join(self.order)

        pos = [self.player_pos[i] for i in range(3)]
        pos = " ".join([str(x) for x in pos])
        risk = [self.player_risk[i] for i in range(3)]
        risk = " ".join([str(x) for x in risk])
        rounds_left = str(self.counter)
        result = start + " " + pos + " " + risk + " " + rounds_left
        return result

    # If Game Over do nothing. Else advance and check after advance if game is over.
    def advance_wrapper(self, actions):
        if self.GAME_OVER:
            self.GAME_OVER = False
        else:
            self.advance(actions)
            self.after_work()

    def advance(self, actions):
        def advance_one_player(action, pos, risk):
            lookUp = [[1, -1], [2, 0], [2, 1], [3, 2]]
            idx = self.order.index(action)
            move_change, risk_change = lookUp[idx]
            new_position = pos + move_change
            new_risk = risk + risk_change
            return new_position, new_risk

        def get_colliding_players():
            participating_players = [i for i in range(self.numPlayers) if self.player_risk[i] > 0]
            positions_of_players = [self.player_pos[i] % 10 for i in participating_players]
            result = []
            for participant_idx in participating_players:
                participant_pos = self.player_pos[participant_idx] % 10
                if positions_of_players.count(participant_pos) > 1:
                    result.append(participant_idx)
            return result

        for i in range(self.numPlayers):
            # If player is stunned, skip
            if self.player_risk[i] < 0:
                self.player_risk[i] += 1
                continue

            # Get new positoin and risk based on action choice
            new_position, new_risk = advance_one_player(actions[i], self.player_pos[i], self.player_risk[i])
            self.player_pos[i] = new_position
            self.player_risk[i] = new_risk
            if self.player_risk[i] < 0:
                self.player_risk[i] = 0

        # Stun check colliding players
        colliding_players = get_colliding_players()
        for i in colliding_players:
            self.player_risk[i] += 2

        # Stun players with risk >= 5
        for i in range(self.numPlayers):
            if self.player_risk[i] >= 5:
                self.player_risk[i] = -2

        random.shuffle(self.order)
        self.counter -= 1

    def is_game_over(self):
        return self.counter == 0

    def get_winners(self):
        max_distance = max(self.player_pos)
        winners = [i for i in range(self.numPlayers) if self.player_pos[i] == max_distance]
        return winners

    # Check if Game is over, identify winners, update medals, reset
    def after_work(self):
        def _update_medals(winners):
            not_winners = [i for i in range(self.numPlayers) if i not in winners]

            for player in winners:
                self.medals[player]["gold"] += 1
            for player in not_winners:
                self.medals[player]["bronze"] += 1

        if self.is_game_over():
            winners = self.get_winners()
            _update_medals(winners)
            self.reset()
            self.GAME_OVER = True
