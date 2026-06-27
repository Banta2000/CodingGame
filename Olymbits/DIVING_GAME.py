import random


class DIVING_GAME:
    def __init__(self):
        self.numPlayers = 3
        self.GAME_OVER = False
        self.medals = [{"gold": 0, "silver": 0, "bronze": 0} for _ in range(self.numPlayers)]
        self.reset()

    def reset(self):
        self.round_len = random.randint(12, 14)
        self.sequence = [random.choice(["U", "L", "D", "R"]) for _ in range(self.round_len)]
        self.points = [0, 0, 0]
        self.multiplier = [0, 0, 0]

    def printGame(self):
        print("Sequence", self.sequence)
        for i in range(self.numPlayers):
            print("P", i, ":", self.points[i], self.multiplier[i])
        print()

    def printMedals(self):
        for entry in self.medals:
            print(entry)

    def get_state(self):
        if self.GAME_OVER:
            start = "GAME_OVER"
        else:
            start = "".join([str(x) for x in self.sequence])

        result = [start] + self.points + self.multiplier
        result = " ".join([str(x) for x in result])
        return result

    # If Game Over do nothing. Else advance and check after advance if game is over.
    def advance_wrapper(self, actions):
        if self.GAME_OVER:
            self.GAME_OVER = False
        else:
            self.advance(actions)
            self.after_work()

    def advance(self, actions):
        next_letter = self.sequence.pop(0)
        for i in range(self.numPlayers):
            if actions[i] == next_letter:
                self.multiplier[i] += 1
                self.points[i] += self.multiplier[i]
            else:
                self.multiplier[i] = 0

    def is_game_over(self):
        return self.sequence == []

    def get_winners(self):
        max_points = max(self.points)
        return [i for i in range(self.numPlayers) if self.points[i] == max_points]

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
