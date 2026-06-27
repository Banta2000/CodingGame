import random


class OBSTACLE_GAME:
    def __init__(self):
        self.numPlayers = 3
        self.GAME_OVER = False
        self.medals = [{"gold": 0, "silver": 0, "bronze": 0} for _ in range(self.numPlayers)]
        self.reset()

    def reset(self):
        def generate_track():
            s = ""
            while len(s) < 30:
                s += "." * random.randint(2, 6)
                s += "#"
            s = s[:30]
            return s

        self.counter = 0
        self.track = generate_track()
        self.pos = [0] * self.numPlayers
        self.stun = [0] * self.numPlayers

    # Text print the state of the game
    def printGame(self):
        print(self.track)
        for i in range(self.numPlayers):
            print("Player", i, "   Pos", self.pos[i], "   Stun", self.stun[i])
        print()

    # Text print the medals of each player
    def printMedals(self):
        for i, entry in enumerate(self.medals):
            print("Player", i, entry)

    # Example: .....#...#....#............... 2 2 2 0 0 0 0
    def get_state(self):
        if self.GAME_OVER:
            start = "GAME_OVER"
        else:
            start = self.track
        result = [start] + self.pos + self.stun
        result = " ".join([str(x) for x in result])
        return result

    # Draw the game, all lanes, all players
    def visualizeGame(self):
        def visualize_one_player(pos, stun):
            RESETCOL = "\x1b[0m"
            RED = "\033[91m"
            GREEN = "\033[92m"
            for i in range(30):
                if i == pos:
                    if stun == 0:
                        print(GREEN + "X" + RESETCOL, end="")
                    else:
                        print(RED + "S" + RESETCOL, end="")
                else:
                    print(self.track[i], end="")
            print()

        for i in range(self.numPlayers):
            visualize_one_player(self.pos[i], self.stun[i])

    # If Game Over do nothing. Else advance. If then Game Over, update medals and reset
    def advance_wrapper(self, actions):
        def _update_medals():

            # Points ranking gibt die Reihenfolge der Punkte [29, 27, 25]
            points_ranking = sorted(self.pos, reverse=True)
            [p1, p2, p3] = points_ranking
            lookUp = {}

            if p1 == p2 and p2 == p3:
                lookUp = {p1: "gold", p2: "gold", p3: "gold"}

            if p1 == p2 and p2 != p3:
                lookUp = {p1: "gold", p2: "gold", p3: "bronze"}

            if p1 != p2 and p2 == p3:
                lookUp = {p1: "gold", p2: "silver", p3: "silver"}

            if p1 != p2 and p2 != p3:
                lookUp = {p1: "gold", p2: "silver", p3: "bronze"}

            self.medals[0][lookUp[self.pos[0]]] += 1
            self.medals[1][lookUp[self.pos[1]]] += 1
            self.medals[2][lookUp[self.pos[2]]] += 1

        if self.GAME_OVER:
            self.GAME_OVER = False
            self.reset()
            return

        self.advance(actions)
        if self.is_game_over():
            _update_medals()
            self.GAME_OVER = True

    # Input ["U", "L", "R", "D]
    def advance(self, actions):
        def advance_one_player(action, pos, stun):
            if stun > 0:
                return pos, stun - 1

            if action == "U":
                pos += 2
                if pos >= len(self.track) or self.track[pos] == ".":
                    return pos, 0
                return pos, 2

            if action == "L":
                pos += 1
                if pos >= len(self.track) or self.track[pos] == ".":
                    return pos, 0
                return pos, 2

            if action == "D":
                for _ in range(2):
                    pos, stun = advance_one_player("L", pos, stun)
                    if stun > 0:
                        return pos, stun
                return pos, stun

            if action == "R":
                for _ in range(3):
                    pos, stun = advance_one_player("L", pos, stun)
                    if stun > 0:
                        return pos, stun
                return pos, stun

        self.counter += 1

        for i in range(self.numPlayers):
            pos, stun = advance_one_player(actions[i], self.pos[i], self.stun[i])
            self.pos[i] = pos
            self.stun[i] = stun

    # Check if any self.pos is >= 30
    def is_game_over(self):
        return self.pos[0] >= 29 or self.pos[1] >= 29 or self.pos[2] >= 29

    # Load the game from a string
    def load_config(self, config):
        config = config.split()
        self.track = config[0]
        config = [int(x) for x in config[1:]]
        self.pos = config[:3]
        self.stun = config[3:]
        self.GAME_OVER = False
        self.counter = 0

        # self.medals = [{"gold": 0, "silver": 0, "bronze": 0} for _ in range(self.numPlayers)]
        # self.reset()
