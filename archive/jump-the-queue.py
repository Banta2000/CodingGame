from typing import Any, Tuple, List
from cgutils.coding_game_helper import CodingGameHelper


def read_input(CGH: CodingGameHelper):
    g, e = [int(i) for i in CGH.input().split()]
    groups = [CGH.input() for _ in range(g)]
    groups = [line.split() for line in groups]
    groups = [[int(i) for i in group] for group in groups]
    events = [int(i) for i in CGH.input().split()]
    return events, groups


def is_friend(myself, other, groups):
    for group in groups:
        if myself in group and other in group:
            return True
    return False


def insert_into_queue(queue, myself, groups):
    if len(queue) == 0:
        queue.append(myself)
        return queue

    for i in reversed(range(len(queue))):
        other = queue[i]
        if is_friend(myself, other, groups):
            if i == len(queue) - 1:
                queue.append(myself)
            else:
                queue.insert(i + 1, myself)
            return queue
    queue.append(myself)
    return queue


# ********************************************************

CGH = CodingGameHelper()
events, groups = read_input(CGH)
queue = []
for event in events:
    if event > 0:
        queue = insert_into_queue(queue, event, groups)
    else:
        res = queue.pop(0)
        CGH.print(res)
