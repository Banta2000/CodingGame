import sys
import os
from math import sqrt
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"
Solution = Tuple[int, int, int, int]


def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


def get_start_parameters() -> int:
    if HOME_PC:
        n = 24
    else:
        n = int(input())
    return n


def get_cond1_solutions(n: int) -> List[Solution]:
    res = []
    n_sqrt = int(sqrt(n)) + 2
    for a in range(n_sqrt):
        for b in range(a, n_sqrt):
            for c in range(b, n_sqrt):
                for d in range(c, n_sqrt):
                    if a**2 + b**2 + c**2 + d**2 == n:
                        res.append((a, b, c, d))
                        break
                    if a**2 + b**2 + c**2 + d**2 > n:
                        break
    return res


def check_cond2(s1, s2, s3):
    cases = [(s1, s2, s3), (s1, s3, s2), (s2, s1, s3), (s2, s3, s1), (s3, s1, s2), (s3, s2, s1)]
    res = set()
    for b, c, d in cases:
        e = b + 3 * c + 5 * d
        if int(sqrt(e)) ** 2 == e:
            res.add((b, c, d, int(sqrt(e))))
    return res


def get_cond2_solutions(sol: Solution):
    a, b, c, d = sol
    s1 = check_cond2(b, c, d)
    s1 = [(a,) + x for x in s1]
    s2 = check_cond2(a, c, d)
    s2 = [(b,) + x for x in s2]
    s3 = check_cond2(a, b, d)
    s3 = [(c,) + x for x in s3]
    s4 = check_cond2(a, b, c)
    s4 = [(d,) + x for x in s4]

    res = set()
    for x in s1:
        res.add(x)
    for x in s2:
        res.add(x)
    for x in s3:
        res.add(x)
    for x in s4:
        res.add(x)
    return res


# ********************************************************

# a² + b² + c² + d² = n
# b + 3c + 5d = e².

n = get_start_parameters()
solutions = get_cond1_solutions(n)

end_sol = set()
for sol in solutions:
    r = get_cond2_solutions(sol)
    end_sol.update(r)

print(len(end_sol))


# for a in range(0, n):
#     for b in range(0, n):
#         for c in range(0, n):
#             for d in range(0, n):
#                 if a**2 + b**2 + c**2 + d**2 == n:
#                     e = b + 3 * c + 5 * d
#                     if int(sqrt(e)) ** 2 == e:
#                         print(a, b, c, d, e)
#                         break


# 4 0 2 2 4
