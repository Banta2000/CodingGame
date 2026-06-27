import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"

SIGNAL_ON = "-"
SIGNAL_OFF = "_"

GATE_FUNCS = {
    "AND": lambda a, b: SIGNAL_ON if a == SIGNAL_ON and b == SIGNAL_ON else SIGNAL_OFF,
    "OR": lambda a, b: SIGNAL_ON if a == SIGNAL_ON or b == SIGNAL_ON else SIGNAL_OFF,
    "XOR": lambda a, b: SIGNAL_ON if a != b else SIGNAL_OFF,
    "NAND": lambda a, b: SIGNAL_ON if not (a == SIGNAL_ON and b == SIGNAL_ON) else SIGNAL_OFF,
    "NOR": lambda a, b: SIGNAL_ON if not (a == SIGNAL_ON or b == SIGNAL_ON) else SIGNAL_OFF,
    "NXOR": lambda a, b: SIGNAL_ON if not (a != b) else SIGNAL_OFF,
}


def get_start_parameters():
    if HOME_PC:
        data = [
            "A __---___---___---___---___",
            "B ____---___---___---___---_",
            "C AND A B",
            "D OR A B",
            "E XOR A B",
        ]

    else:
        n = int(input())
        m = int(input())
        data = [input() for _ in range(n + m)]

    DATA = {}
    RULES = []
    OUTPUT = []

    for line in data:
        line = line.split(" ")
        key = line[0]
        if len(line) == 2:
            DATA[key] = line[1]
        else:
            DATA[key] = ""
            RULES.append(line)
            OUTPUT.append(key)

    return DATA, RULES, OUTPUT


def apply_rule(data, rule, i):
    res_key, op, a_key, b_key = rule
    a = data[a_key][i]
    b = data[b_key][i]
    data[res_key] += GATE_FUNCS[op](a, b)


# ********************************************************

DATA, RULES, OUTPUT = get_start_parameters()

LEN_SIGNAL = max([len(x) for x in DATA.values() if x is not None])
for i in range(LEN_SIGNAL):
    for rule in RULES:
        apply_rule(DATA, rule, i)

for key in OUTPUT:
    print(f"{key} {DATA[key]}")
