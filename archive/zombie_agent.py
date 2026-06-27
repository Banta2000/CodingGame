import sys
import os
from typing import Any, Tuple, Union

HOME_PC: bool = os.getenv("HOME_PC") == "true"


class Player:
    def __init__(self, human_id: int, x: int, y: int, x_next: int = None, y_next: int = None) -> None:
        self.id: int = human_id
        self.pos: Tuple[int, int] = (x, y)
        if x_next is not None:
            self.next_pos: Tuple[int, int] = (x_next, y_next)
        else:
            self.next_pos: Tuple[int, int] = None

    def __str__(self) -> str:
        return f"ID {self.id}  POS {self.pos}  NEXT {self.next_pos}"

    def __repr__(self) -> str:
        return self.__str__()


class Agent:
    def __init__(self, GS) -> None:
        self.zombies = GS["zombies"]
        self.humans = GS["humans"]
        self.player = GS["player"]

    def __str__(self) -> str:
        return "Agent"

    def __repr__(self) -> str:
        return self.__str__()

    def get_closest_human(self) -> Player:
        closest_human = get_closest_player(self.player, self.humans)
        return closest_human

    def get_closest_zombie(self) -> Player:
        closest_zombie = get_closest_player(self.player, self.zombies)
        return closest_zombie


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_input() -> dict[str, Any]:
    if HOME_PC:
        params = {}
    else:
        params: dict[str, Any] = {}
        x, y = [int(i) for i in input().split()]
        params["player"] = Player(0, x, y)

        params["humans"] = []
        human_count = int(input())
        for i in range(human_count):
            human_id, human_x, human_y = [int(j) for j in input().split()]
            params["humans"].append(Player(human_id, human_x, human_y))

        params["zombies"] = []
        zombie_count = int(input())
        for i in range(zombie_count):
            zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
            params["zombies"].append(Player(zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext))

    return params


def distance(A: Union[Tuple[int, int], Player], B: Union[Tuple[int, int], Player]) -> int:
    if isinstance(A, Player):
        pos1 = A.pos
    else:
        pos1 = A

    if isinstance(B, Player):
        pos2 = B.pos
    else:
        pos2 = B

    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def get_closest_player(p1: Player, players: list[Player]) -> Player:
    closest_player = min(players, key=lambda p2: distance(p1, p2))
    return closest_player


def evalute_surival_chance_of_human(human: Player, GS) -> float:
    zombies: list[Player] = GS["zombies"]
    player: Player = GS["player"]

    zombie_steps = 400
    player_steps = 1000

    closest_zombie = get_closest_player(human, zombies)
    distance_to_closest_zombie = distance(human, closest_zombie)
    cycles_before_zombie_reaches_human = (distance_to_closest_zombie // zombie_steps) + 1

    distance_to_playert = distance(human, player)
    cycles_before_player_reaches_human = (distance_to_playert // player_steps) + 1

    myPrint(human)
    myPrint(closest_zombie)
    myPrint(cycles_before_zombie_reaches_human)
    myPrint(cycles_before_player_reaches_human)
    myPrint()
    return cycles_before_player_reaches_human <= cycles_before_zombie_reaches_human


# ********************************************************


while True:
    GS = get_input()
    agent = Agent(GS)
    humans_i_can_save = [human for human in GS["humans"] if evalute_surival_chance_of_human(human, GS)]
    if humans_i_can_save:
        chosen_one = humans_i_can_save[0]
    else:
        chosen_one = agent.get_closest_human()
    # closest_zombie = agent.get_closest_zombie()
    # chosen_one = humans_i_can_save[0]
    print(chosen_one.pos[0], chosen_one.pos[1])
