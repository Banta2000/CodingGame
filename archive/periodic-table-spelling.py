import sys
import os
from typing import Any, Tuple, List

ELEMENTS = [
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
]

E1 = [x for x in ELEMENTS if len(x) == 1]
E2 = [x for x in ELEMENTS if len(x) == 2]


def get_matching_elements(index: int) -> List[str]:
    if index >= len(WORD):
        return []

    res = []
    for x in E1:
        if WORD[index].lower() == x.lower():
            res.append(x)

    if index + 1 < len(WORD):
        for x in E2:
            if WORD[index : index + 2].lower() == x.lower():
                res.append(x)
    return res


def dfs(index):
    if index == len(WORD):
        return [""]

    res = []
    MATCHING = get_matching_elements(index)
    for SUFFIX in MATCHING:
        ret = dfs(index + len(SUFFIX))
        for x in ret:
            res.append(SUFFIX + x)

    return res


# ********************************************************

WORD = input()
# WORD = "pause"
res = dfs(0)
if len(res) == 0:
    print("none")
    sys.exit()
for x in res:
    print(x)
