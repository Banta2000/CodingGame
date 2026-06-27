import random


class ARCHERY_GAME:
    def __init__(self):
        self.numPlayers = 3
        self.GAME_OVER = False
        self.medals = [{"gold": 0, "silver": 0, "bronze": 0} for _ in range(self.numPlayers)]
        self.reset()

    def reset(self):
        this_round_len = random.randint(12, 15)
        self.wind_lst = [random.randint(1, 9) for _ in range(this_round_len)]
        self.player_pos = [[0, 0], [0, 0], [0, 0]]

    def printGame(self):
        print("Wind", self.wind_lst)
        for i in range(self.numPlayers):
            print("Pos ", i, ":", self.player_pos[i])
        print()

    def printMedals(self):
        for entry in self.medals:
            print(entry)

    def get_state(self):
        if self.GAME_OVER:
            start = "GAME_OVER"
        else:
            start = "".join([str(x) for x in self.wind_lst])
        t = self.player_pos[0] + self.player_pos[1] + self.player_pos[2]
        t = [str(x) for x in t]
        t = " ".join(t)
        result = start + " " + t
        return result

    # If Game Over do nothing. Else advance and check after advance if game is over.
    def advance_wrapper(self, actions):
        if self.GAME_OVER:
            self.GAME_OVER = False
        else:
            self.advance(actions)
            self.after_work()

    def advance(self, actions):
        def advance_one_player(action, pos, wind):
            px, py = pos
            if action == "U":
                py -= wind
            if action == "L":
                px -= wind
            if action == "D":
                py += wind
            if action == "R":
                px += wind

            return [px, py]

        wind = self.wind_lst.pop(0)

        for i in range(self.numPlayers):
            pos = advance_one_player(actions[i], self.player_pos[i], wind)
            self.player_pos[i] = pos

    def is_game_over(self):
        return self.wind_lst == []

    def get_winners(self):
        final_distance = [abs(x[0]) + abs(x[1]) for x in self.player_pos]
        min_distance = min(final_distance)
        return [i for i in range(self.numPlayers) if final_distance[i] == min_distance]

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
