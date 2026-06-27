from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper
from dataclasses import dataclass
from collections import Counter


@dataclass
class Ship:
    type: str
    hp: int
    armor: int
    damage: int

    def copy(self):
        return Ship(type=self.type, hp=self.hp, armor=self.armor, damage=self.damage)


def find_candidates(ships: list[Ship]) -> list[int]:
    res = []
    for i, ship in enumerate(ships):
        if ship.hp > 0:
            res.append(i)
    return res


def is_won(ships: list[Ship]) -> bool:
    # Returns true if all ships HP is equal or smaller 0
    hp = [ship.hp <= 0 for ship in ships]
    return all(hp)


def hit_player(ships: list[Ship], player: Ship):
    # All ships that are alive hit the player
    for ship in ships:
        if ship.hp > 0:
            player.hp -= ship.damage
    return player


def hit_ship(ship):
    # Player hits the ship
    attack = PD * 2 if ship.type == "FIGHTER" else PD
    damage = attack - ship.armor
    damage = damage if damage > 0 else 1
    ship.hp -= damage
    return ship


def dfs(kill_order):
    player = Ship(type="player", hp=5000, armor=0, damage=10)
    ships2 = [ship.copy() for ship in ships]

    i = 0
    while i < len(kill_order):
        idx = kill_order[i]
        player = hit_player(ships2, player)
        ships2[idx] = hit_ship(ships2[idx])
        if ships2[idx].hp <= 0:
            i += 1
    return player.hp


def read_input() -> list[Ship]:
    n = int(CGH.input())
    ships = []
    for _ in range(n):
        line = CGH.input().split(" ")
        ships.append(Ship(type=line[0], hp=int(line[1]), armor=int(line[2]), damage=int(line[3])))
    return ships


def compute_lookups(ships: list[Ship]):
    # Returns dict (si, tj) -> strength of ship i, time to kill ship j
    res = {}
    for i, ship1 in enumerate(ships):
        for j, ship2 in enumerate(ships):
            if i == j:
                continue
            attack = PD * 2 if ship2.type == "FIGHTER" else PD
            damage = attack - ship2.armor
            damage = damage if damage > 0 else 1
            time_to_kill = ship2.hp // damage + (1 if ship2.hp % damage > 0 else 0)
            res[(i, j)] = ship1.damage * time_to_kill
    res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}
    return res


# ********************************************************


CGH = CodingGameHelper(8, __file__)
PD = 10
ships = read_input()
player = Ship(type="player", hp=5000, armor=0, damage=10)

LU = compute_lookups(ships)

# Construct a collection of pairs of ships that are strong against each other
collection = []
for c1, c2 in LU.keys():
    if (c1, c2) not in collection and (c2, c1) not in collection:
        collection.append((c1, c2))


# Get the order of ships for destruction
collection = [c2 for c1, c2 in collection]
remaining = [i for i in range(len(ships)) if i not in collection][0]

collection = Counter(collection)
order = [item[0] for item in collection.most_common()]
order.append(remaining)

res = dfs(order)
if res >= 0:
    CGH.print(res)
else:
    CGH.print("FLEE")

CGH.assert_output()
