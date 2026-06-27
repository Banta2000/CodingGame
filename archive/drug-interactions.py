from collections import Counter
from cgutils.coding_game_helper import CodingGameHelper


def read_input(CGH: CodingGameHelper):
    num_drugs = int(CGH.input())
    lines = [CGH.input() for _ in range(num_drugs)]
    return compute_can_work(lines)


def do_overlap(s1: str, s2: str) -> bool:
    # True if two drug names share 3 or more letters (case-insensitive, with multiplicity)
    c1 = Counter(s1.lower())
    c2 = Counter(s2.lower())
    return sum(min(c1[l], c2[l]) for l in c1 if l in c2) >= 3


def compute_can_work(lines: list):
    # Returns a list of bitmasks: POSSIBLE_NEXT_STATES[i] has bit j set iff drug i and drug j are compatible.
    # A drug is always compatible with itself.
    res = []
    for w1 in lines:
        mask = 0
        for n2, w2 in enumerate(lines):
            if w1 == w2 or not do_overlap(w1, w2):
                mask |= 1 << n2
        res.append(mask)
    return res


def get_candidates(path: set) -> int:
    # Returns bitmask of drugs that are compatible with all drugs in path,
    # restricted to indices strictly greater than the largest in path (canonical ordering).
    res = ALL_ONES
    for c in path:
        res &= POSSIBLE_NEXT_STATES[c]
    if path:
        # Build a mask of 1s for all bits above max(path), 0s for max(path) and below,
        # then AND it in to enforce strict ordering (only pick drugs with higher index).
        # e.g. max=3: (1<<4)-1 = 0b1111, ~0b1111 = ...11110000 → clears bits 0-3.
        res &= ~((1 << (max(path) + 1)) - 1)
    return res


def dfs(path: set) -> int:
    candidates = get_candidates(path)

    if candidates in CACHE:
        return len(path) + CACHE[candidates]

    if candidates == 0:
        return len(path)

    best_len = 0
    tmp = candidates
    while tmp:
        v = (tmp & -tmp).bit_length() - 1  # index of lowest set bit
        path.add(v)
        best_len = max(best_len, dfs(path))
        path.remove(v)
        tmp &= tmp - 1                      # clear lowest set bit
    CACHE[candidates] = best_len - len(path)
    return best_len


CACHE = dict()
CGH = CodingGameHelper(5, __file__)
POSSIBLE_NEXT_STATES = read_input(CGH)
ALL_ONES = (1 << len(POSSIBLE_NEXT_STATES)) - 1

res = dfs(set())
CGH.add_output_line(str(res))
CGH.assert_output()
