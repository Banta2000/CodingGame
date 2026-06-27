import random
from Agent import Agent
from OBSTACLE_GAME import OBSTACLE_GAME
from ARCHERY_GAME import ARCHERY_GAME
from SKATING_GAME import SKATING_GAME
from DIVING_GAME import DIVING_GAME
import utils


class FULL_GAME:
    def __init__(self):
        self.g1 = OBSTACLE_GAME()
        self.g2 = ARCHERY_GAME()
        self.g3 = SKATING_GAME()
        self.g4 = DIVING_GAME()

    def get_state(self):
        state1 = self.g1.get_state()
        state2 = self.g2.get_state()
        state3 = self.g3.get_state()
        state4 = self.g4.get_state()

        # state1 = "......#...#....#.............. 23 26 26 0 0 0 0"
        # state2 = "23831262 7 -6 8 -1 8 -1 0"
        # state3 = "DLRU 3 4 4 2 -2 -2 13"
        # state4 = "RLDDRULRUR 15 1 1 5 0 0 0"
        return [state1, state2, state3, state4]

    def get_medals_state(self):
        def compute_player_medals(medals):
            s = []
            full_points = 1
            for entry in medals:
                line = [entry["gold"], entry["silver"], entry["bronze"]]
                points_for_one_game = line[0] * 3 + line[1]
                full_points *= points_for_one_game
                s += line
            result = str(full_points) + " " + " ".join([str(x) for x in s])

            return result

        # Get medals for each game; each game has 3 players
        medals1 = self.g1.medals
        medals2 = self.g2.medals
        medals3 = self.g3.medals
        medals4 = self.g4.medals

        # Combine the medals for each player
        p0 = [medals1[0], medals2[0], medals3[0], medals4[0]]
        p1 = [medals1[1], medals2[1], medals3[1], medals4[1]]
        p2 = [medals1[2], medals2[2], medals3[2], medals4[2]]

        # Get the string representation of the medals per player
        s0 = compute_player_medals(p0)
        s1 = compute_player_medals(p1)
        s2 = compute_player_medals(p2)
        return [s0, s1, s2]

    def advance(self, actions):
        CHOICES_LOOKUP = {"UP": "U", "LEFT": "L", "RIGHT": "R", "DOWN": "D"}
        actions = [CHOICES_LOOKUP[x] if x in CHOICES_LOOKUP else x for x in actions]

        game.g1.advance_wrapper(actions)
        game.g2.advance_wrapper(actions)
        game.g3.advance_wrapper(actions)
        game.g4.advance_wrapper(actions)

    def get_total_points(self):
        medal_state = self.get_medals_state()
        points = [int(x.split()[0]) for x in medal_state]
        return points


# START **************************************************************************************

g1_configs = [
    ".....#...#....#............... 0 0 0 0 0 0 0",
    ".....#....#...#...#....#....#. 0 0 0 0 0 0 0",
    "....#...#...#...#....#....#... 0 0 0 0 0 0 0",
    ".....#...#....#...#....#...#.. 0 0 0 0 0 0 0",
    "......#...#...#....#...#...... 0 0 0 0 0 0 0",
]


game = FULL_GAME()
player = Agent()

user_actions = utils.extract_user_actions()
user_actions = list(zip(*user_actions))

game.g1.load_config(g1_strings.pop(0))


CHOICES = ["U", "L", "R", "D"]

for i in range(0, 100):
    print(i)
    inputs_lst = game.get_state()
    medal_lst = game.get_medals_state()

    print(inputs_lst[0])
    game.g1.visualizeGame()

    # a1 = player.get_action(medal_lst, inputs_lst)
    # a2 = random.choice(CHOICES)
    # a3 = random.choice(CHOICES)
    # actions = [a1, a2, a2]
    actions = user_actions.pop(0)
    game.advance(actions)

    # GANZ AM ENDE DER LOOP MUSS ICH CONFIG LADEN; SCHAUE NICHT AUF g1.game_over da dies zu dem zeitpunkt bereits wieder true ist

    # TODO KOENNTE IN SPEZIELLE FUNKTION LOAD_GAME_OVER_CONFIGS AUSGELAGERT WERDEN
    if inputs_lst[0].startswith("GAME_OVER"):
        game.g1.load_config(g1_configs.pop(0))

    print()

print(game.g1.printGame())

# print(game.get_medals_state())
# print(game.get_total_points())


# TODO load_config sollte nicht variablen laden, sondern regs laden und die uebergeben
