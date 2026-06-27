from cgutils.coding_game_helper import CodingGameHelper


Player = dict[str, float]


def read_input(CGH: CodingGameHelper) -> tuple[Player, Player]:
    inputs = CGH.input().split()
    p1: Player = {
        "hp": int(inputs[1]),
        "blows": int(inputs[2]),
        "to_hit": int(inputs[3]) / 100,
        "damage": int(inputs[4]),
    }

    inputs = CGH.input().split()
    p2: Player = {
        "hp": int(inputs[1]),
        "blows": int(inputs[2]),
        "to_hit": int(inputs[3]) / 100,
        "damage": int(inputs[4]),
    }
    return p1, p2


def has_blows_left(p: Player) -> bool:
    return p["blows"] > 0


def hit(p1: Player, p2: Player, hits: bool) -> tuple[Player, Player]:
    # Returns two new players with updated hp and blows
    p1_new = p1.copy()
    p2_new = p2.copy()

    p1_new["blows"] -= 1
    if hits:
        p2_new["hp"] -= p1["damage"]
    return p1_new, p2_new


def is_over(p1: Player, p2: Player) -> bool:
    return p1["hp"] <= 0 or p2["hp"] <= 0 or (not has_blows_left(p1) and not has_blows_left(p2))


def update_stats(p1: Player, p2: Player, prob: float, stats: dict[str, float]):
    if p1["hp"] <= 0:
        stats["p1_death"] += prob
    elif p2["hp"] <= 0:
        stats["p2_death"] += prob
    else:
        stats["draw"] += prob


def dfs(p1: Player, p2: Player, prob: float, p1_turn: bool, stats: dict[str, float]):
    if is_over(p1, p2):
        update_stats(p1, p2, prob, stats)
        return

    if p1_turn:
        if p1["blows"] <= 0:
            # No blows left, switch turn
            dfs(p1, p2, prob, False, stats)
            return
        else:
            # Blows left, continue with the current player; can hit or not
            p1_new, p2_new = hit(p1, p2, True)
            dfs(p1_new, p2_new, prob * p1["to_hit"], False, stats)
            p1_new, p2_new = hit(p1, p2, False)
            dfs(p1_new, p2_new, prob * (1 - p1["to_hit"]), False, stats)
    else:
        if p2["blows"] <= 0:
            # No blows left, switch turn
            dfs(p1, p2, prob, True, stats)
            return
        else:
            # Blows left, continue with the current player; can hit or not
            p2_new, p1_new = hit(p2, p1, True)
            dfs(p1_new, p2_new, prob * p2["to_hit"], True, stats)
            p2_new, p1_new = hit(p2, p1, False)
            dfs(p1_new, p2_new, prob * (1 - p2["to_hit"]), True, stats)


# ********************************************************


for case_nr in range(1, 9):
    CGH = CodingGameHelper(case_nr, __file__)
    p1, p2 = read_input(CGH)
    stats = {"p1_death": 0.0, "p2_death": 0.0, "draw": 0.0}

    dfs(p1, p2, 1.0, True, stats)
    p1_res = int(round(stats["p1_death"] * 100))
    p2_res = int(round(stats["p2_death"] * 100))
    s = f"{p1_res} {p2_res}"
    CGH.add_output_line(s)
    CGH.assert_output()
