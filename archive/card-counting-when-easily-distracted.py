import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"


if HOME_PC:
    # stream = "222.333.444.some istraction.555.5.678.678.678.678.another distraction.9999.TTTT.JJJJ.QQQQ.KKKK.AAAA"
    # threshold = 4
    stream = "Did I turn the iron off?.Did I turn the iron off?.AT3A.7JA.J.Oceans11.95A.mob boss.IRS.hungry.Cute dealer.2.45T84Q.Show Girls!!.QQQ.24868.QUEEN.K837695.Is that Penn or Teller?.362436.KJ7KJ"
    threshold = 7
else:
    stream = input()
    threshold = int(input())


def is_valid(chunk: str) -> bool:
    for char in chunk:
        if char not in "23456789TJQKA":
            return False
    return True


LU = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "T": 0, "J": 0, "Q": 0, "K": 0, "A": 0}
VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 10, "Q": 10, "K": 10, "A": 1}

chunks = stream.split(".")
chunks = [chunk for chunk in chunks if is_valid(chunk)]
stream = "".join(chunks)

for chr in stream:
    if chr in LU:
        LU[chr] += 1

remaining = {k: 4 - v for k, v in LU.items() if v < 4}

remaining_under_threshold = {k: v for k, v in remaining.items() if VALUES[k] < threshold}
remaining = sum(remaining.values())

remaining_under_threshold = sum(remaining_under_threshold.values())

res = remaining_under_threshold / remaining * 100
print(f"{round(res)}%")
