import sys
import os
from typing import Tuple, List, Dict, FrozenSet, Set
import math
from dataclasses import dataclass
from collections import deque
import time  # Import the time module
from collections import defaultdict
import joblib
import logging

Point = Tuple[int, int]

logging.basicConfig(
    filename="_logfile.txt",  # Log file path
    level=logging.DEBUG,  # Log level
    format="%(message)s",  # Log format
    filemode="w",  # Overwrite the log file each time
)


RAW_PIECES = [
    ("I liegend", 0, ((0, 0), (0, 1), (0, 2), (0, 3)), (1, 0, 0, 0, 0, 0, 0)),
    ("I stehend", 0, ((0, 0), (1, 0), (2, 0), (3, 0)), (1, 0, 0, 0, 0, 0, 0)),
    ("Viereck", 1, ((0, 0), (0, 1), (1, 0), (1, 1)), (0, 1, 0, 0, 0, 0, 0)),
    ("T stehend", 2, ((0, 0), (0, 1), (0, 2), (1, 1)), (0, 0, 1, 0, 0, 0, 0)),
    ("T wie 3", 2, ((0, 0), (1, 0), (2, 0), (1, -1)), (0, 0, 1, 0, 0, 0, 0)),
    ("T wie E", 2, ((0, 0), (1, 0), (2, 0), (1, 1)), (0, 0, 1, 0, 0, 0, 0)),
    ("T auf Rücken", 2, ((0, 0), (1, -1), (1, 0), (1, 1)), (0, 0, 1, 0, 0, 0, 0)),
    ("L Liegestütze", 3, ((0, 0), (0, 1), (0, 2), (1, 0)), (0, 0, 0, 1, 0, 0, 0)),
    ("L Strassenlaterne", 3, ((0, 0), (0, 1), (1, 1), (2, 1)), (0, 0, 0, 1, 0, 0, 0)),
    ("L liegend", 3, ((0, 0), (1, -2), (1, -1), (1, 0)), (0, 0, 0, 1, 0, 0, 0)),
    ("L stehend", 3, ((0, 0), (1, 0), (2, 0), (2, 1)), (0, 0, 0, 1, 0, 0, 0)),
    ("J Liegestütze", 4, ((0, 0), (0, 1), (0, 2), (1, 2)), (0, 0, 0, 0, 1, 0, 0)),
    ("J stehend", 4, ((0, 0), (1, 0), (2, 0), (2, -1)), (0, 0, 0, 0, 1, 0, 0)),
    ("J liegend", 4, ((0, 0), (1, 0), (1, 1), (1, 2)), (0, 0, 0, 0, 1, 0, 0)),
    ("J Strassenlaterne", 4, ((0, 0), (0, 1), (1, 0), (2, 0)), (0, 0, 0, 0, 1, 0, 0)),
    ("Z liegend", 5, ((0, 0), (0, 1), (1, 1), (1, 2)), (0, 0, 0, 0, 0, 1, 0)),
    ("Z stehend", 5, ((0, 0), (1, 0), (1, -1), (2, -1)), (0, 0, 0, 0, 0, 1, 0)),
    ("S liegend", 6, ((0, 0), (0, 1), (1, -1), (1, 0)), (0, 0, 0, 0, 0, 0, 1)),
    ("S stehend", 6, ((0, 0), (1, 0), (1, 1), (2, 1)), (0, 0, 0, 0, 0, 0, 1)),
]


class Examples:
    examples = {}

    name = "Studio 1"
    sol_cost, sol_hist, sol_solutions = 207.64, "0 4 0 2 0 0 0", 2
    w, h = 7, 7
    prices = [17.25, 14.13, 72.37, 75.56, 83.64, 42.80, 17.46]
    plan = ["#######", "#.....#", "#.....#", "#..#..#", "#.....#", "#.....#", "#######"]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Studio 2"
    sol_cost, sol_hist, sol_solutions = 226.42, "0 0 2 0 4 2 0", 2
    w, h = 8, 8
    prices = [42.41, 50.85, 89.13, 16.09, 9.57, 4.94, 52.58]
    plan = [
        "########",
        "#.....##",
        "#......#",
        "#...#..#",
        "#..#...#",
        "#......#",
        "##.....#",
        "########",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "One Bedroom"
    sol_cost, sol_hist, sol_solutions = 114.44, "0 0 1 1 12 0 0", 2
    w, h = 10, 10
    prices = [91.39, 41.12, 32.22, 43.58, 3.22, 20.19, 91.59]
    plan = [
        "##########",
        "#........#",
        "#........#",
        "#....#...#",
        "#...#....#",
        "#........#",
        "####..####",
        "#........#",
        "#........#",
        "##########",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "One Bedroom 2"
    sol_cost, sol_hist, sol_solutions = 157.00, "0 0 0 2 12 0 0", 4
    w, h = 10, 10
    prices = [45.15, 60.33, 62.97, 18.02, 10.08, 25.97, 74.97]
    plan = [
        "##########",
        "#.....#..#",
        "#.....#..#",
        "#.....#..#",
        "#..#.....#",
        "#..#.....#",
        "#.....#..#",
        "#.....#..#",
        "#.....#..#",
        "##########",
    ]

    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)
    name = "Two Bedroom"
    sol_cost, sol_hist, sol_solutions = 764.88, "1 0 6 0 13 1 0", 1
    w, h = 17, 9
    prices = [64.86, 61.09, 20.66, 97.93, 41.82, 32.40, 52.78]
    plan = [
        "#################",
        "#.......#.......#",
        "#....#..#.......#",
        "#...#...######..#",
        "#...#...........#",
        "#...#...######..#",
        "#....#..#.......#",
        "#.......#.......#",
        "#################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Many Possibilities"
    sol_cost, sol_hist, sol_solutions = 3729.15, "18 0 0 9 153 0 9", 10077696
    w, h = 100, 12
    prices = [71.51, 75.49, 48.69, 92.90, 6.34, 72.82, 70.65]
    plan = [
        "####################################################################################################",
        "#..........#..........#..........#..........#..........#..........#..........#..........#..........#",
        "#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#",
        "#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#",
        "#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#",
        "#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#",
        "#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#",
        "#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#",
        "#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#",
        "#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#",
        "#..........#..........#..........#..........#..........#..........#..........#..........#..........#",
        "####################################################################################################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Many Possibilities Single"
    sol_cost, sol_hist, sol_solutions = 414.35, "2 0 0 1 17 0 1", 6
    w, h = 12, 12
    prices = [71.51, 75.49, 48.69, 92.90, 6.34, 72.82, 70.65]
    plan = [
        "############",
        "#..........#",
        "#..#....#..#",
        "#..#....#..#",
        "#...#..#...#",
        "#...#..#...#",
        "#...#..#...#",
        "#...#..#...#",
        "#..#....#..#",
        "#..#....#..#",
        "#..........#",
        "############",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Conformity"
    sol_cost, sol_hist, sol_solutions = 898.56, "0 0 0 0 48 0 96", 1
    w, h = 49, 17
    prices = [21.26, 50.21, 30.59, 84.03, 12.38, 66.47, 3.17]
    plan = [
        "#################################################",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#...#...#...#...#...#...#...#...#...#...#...#...#",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#################################################",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#...#...#...#...#...#...#...#...#...#...#...#...#",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#.......#.......#.......#.......#.......#.......#",
        "#################################################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Conformity 2"
    sol_cost, sol_hist, sol_solutions = 4070.40, "24 84 24 36 0 0 0", 1
    w, h = 50, 21
    prices = [54.46, 4.71, 67.50, 20.77, 39.51, 33.15, 58.21]
    plan = [
        "##################################################",
        "#.......#.......#.......##.......#.......#.......#",
        "#.......#.......#.......##.......#.......#.......#",
        "#...#...#...#...#...#...##...#...#...#...#...#...#",
        "#.......#.......#.......##.......#.......#.......#",
        "#...#...#...#...#...#...##...#...#...#...#...#...#",
        "#.......#.......#.......##.......#.......#.......#",
        "#.......#.......#.......##.......#.......#.......#",
        "####.#######.#######.########.#######.#######.####",
        "#................................................#",
        "##################################################",
        "#.......#.......#.......##.......#.......#.......#",
        "#.......#.......#.......##.......#.......#.......#",
        "#...#...#...#...#...#...##...#...#...#...#...#...#",
        "#.......#.......#.......##.......#.......#.......#",
        "#...#...#...#...#...#...##...#...#...#...#...#...#",
        "#.......#.......#.......##.......#.......#.......#",
        "#.......#.......#.......##.......#.......#.......#",
        "####.#######.#######.########.#######.#######.####",
        "#................................................#",
        "##################################################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Conformity 3"
    sol_cost, sol_hist, sol_solutions = 74.88, "0 0 0 0 4 0 8", 1
    w, h = 9, 9
    prices = [21.26, 50.21, 30.59, 84.03, 12.38, 66.47, 3.17]
    plan = [
        "#########",
        "#.......#",
        "#.......#",
        "#.......#",
        "#...#...#",
        "#.......#",
        "#.......#",
        "#.......#",
        "#########",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Tetris"
    sol_cost, sol_hist, sol_solutions = 1634.04, "26 3 54 0 23 1 7", 96
    w, h = 85, 12
    prices = [24.47, 34.38, 3.38, 48.19, 20.45, 85.64, 22.31]
    plan = [
        "#####################################################################################",
        "#.............#.............#.............#.............##...........###...........##",
        "#..#########..#..#########..#..#########..#..#######....##...#####...##...#######...#",
        "#..##.###.##..#..#########..#..##.###.##..#..##....##...##...#####..###..###...###..#",
        "#..##.###.##..#..##.........#..##.###.##..#..##....##...###..#####..###..##.....##..#",
        "##....###....##..#######....##....###....##..##....##...###..#####..###..###.......##",
        "###...###....##..#######....###...###....##..#######...####..#####..####..#######..##",
        "###...###...###..##.........###...###...###..##...###..####..#####..####........##..#",
        "##....###...###..#########..##....###...###..##...###...###..#####...##..##.....##..#",
        "##....###....##..#########..##....###....##..##....##...##...#####...##..#########..#",
        "#...#.....#...#.............#...#.....#...#.............##...........###...........##",
        "#####################################################################################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Random"
    sol_cost, sol_hist, sol_solutions = 9489.92, "16 16 32 176 512 16 32", 65536
    w, h = 100, 50
    prices = [81.11, 16.64, 81.55, 10.31, 1.38, 93.48, 40.61]
    plan = [
        "####################################################################################################",
        "#...#.......#..##.......##....#......#......#.#..##...#.......#..##.......##....#......#......#.#..#",
        "#.........#.#.#..#.#....##..##..#..#.#.#.#.......##.........#.#.#..#.#....##..##..#..#.#.#.#.......#",
        "#........#..#......#....###.........##..#..#.#.#.##........#..#......#....###.........##..#..#.#.#.#",
        "#.........#.#....#.....###..#..#....##.........#.##.........#.#....#.....###..#..#....##.........#.#",
        "#.##........#.#.........###...#..#.#.#......#...###.##........#.#.........###...#..#.#.#......#...##",
        "#........#..#...#.......##..#........#.......#...##........#..#...#.......##..#........#.......#...#",
        "#.#.#..#...###...#......##........##.#.........#.##.#.#..#...###...#......##........##.#.........#.#",
        "##....#..#..#.#.........##.#.........##.....#....###....#..#..#.#.........##.#.........##.....#....#",
        "##.........##.#.#.#..#..##..#........#....#......###.........##.#.#.#..#..##..#........#....#......#",
        "#.#..#..##..#.......#.#.##.#.........#....#.#..#.##.#..#..##..#.......#.#.##.#.........#....#.#..#.#",
        "#......#....#..#.#......##.......#...#.......##..##......#....#..#.#......##.......#...#.......##..#",
        "####################################################################################################",
        "#...........##.....#....##......#...##.##........##...........##.....#....##......#...##.##........#",
        "#.....#....##..##.#.....##...........#.....#.##..##.....#....##..##.#.....##...........#.....#.##..#",
        "#..........##.....#.....##.#.#..##.#.#...#.......##..........##.....#.....##.#.#..##.#.#...#.......#",
        "#........#..#..##.......##.#....##.#.#.....#..#..##........#..#..##.......##.#....##.#.#.....#..#..#",
        "##....#.....##.##.......##...........#...........###....#.....##.##.......##...........#...........#",
        "#.##....#.#.#......#..#.##.#.#....##.#.#..#......##.##....#.#.#......#..#.##.#.#....##.#.#..#......#",
        "#...........#...........##.....#....##.......##.###...........#...........##.....#....##.......##.##",
        "#.#.##....#.#..#..#.....##..#........#.......##..##.#.##....#.#..#..#.....##..#........#.......##..#",
        "#.#.##..#.#.#.......#...###..........#.....#.....##.#.##..#.#.#.......#...###..........#.....#.....#",
        "#...........#..##.#.....###....#.....#.....#.##..##...........#..##.#.....###....#.....#.....#.##..#",
        "##...#......#........##.##...........#....#.....####...#......#........##.##...........#....#.....##",
        "####################################################################################################",
        "####################################################################################################",
        "#...#.......#..##.......##....#......#......#.#..##...#.......#..##.......##....#......#......#.#..#",
        "#.........#.#.#..#.#....##..##..#..#.#.#.#.......##.........#.#.#..#.#....##..##..#..#.#.#.#.......#",
        "#........#..#......#....###.........##..#..#.#.#.##........#..#......#....###.........##..#..#.#.#.#",
        "#.........#.#....#.....###..#..#....##.........#.##.........#.#....#.....###..#..#....##.........#.#",
        "#.##........#.#.........###...#..#.#.#......#...###.##........#.#.........###...#..#.#.#......#...##",
        "#........#..#...#.......##..#........#.......#...##........#..#...#.......##..#........#.......#...#",
        "#.#.#..#...###...#......##........##.#.........#.##.#.#..#...###...#......##........##.#.........#.#",
        "##....#..#..#.#.........##.#.........##.....#....###....#..#..#.#.........##.#.........##.....#....#",
        "##.........##.#.#.#..#..##..#........#....#......###.........##.#.#.#..#..##..#........#....#......#",
        "#.#..#..##..#.......#.#.##.#.........#....#.#..#.##.#..#..##..#.......#.#.##.#.........#....#.#..#.#",
        "#......#....#..#.#......##.......#...#.......##..##......#....#..#.#......##.......#...#.......##..#",
        "####################################################################################################",
        "#...........##.....#....##......#...##.##........##...........##.....#....##......#...##.##........#",
        "#.....#....##..##.#.....##...........#.....#.##..##.....#....##..##.#.....##...........#.....#.##..#",
        "#..........##.....#.....##.#.#..##.#.#...#.......##..........##.....#.....##.#.#..##.#.#...#.......#",
        "#........#..#..##.......##.#....##.#.#.....#..#..##........#..#..##.......##.#....##.#.#.....#..#..#",
        "##....#.....##.##.......##...........#...........###....#.....##.##.......##...........#...........#",
        "#.##....#.#.#......#..#.##.#.#....##.#.#..#......##.##....#.#.#......#..#.##.#.#....##.#.#..#......#",
        "#...........#...........##.....#....##.......##.###...........#...........##.....#....##.......##.##",
        "#.#.##....#.#..#..#.....##..#........#.......##..##.#.##....#.#..#..#.....##..#........#.......##..#",
        "#.#.##..#.#.#.......#...###..........#.....#.....##.#.##..#.#.#.......#...###..........#.....#.....#",
        "#...........#..##.#.....###....#.....#.....#.##..##...........#..##.#.....###....#.....#.....#.##..#",
        "##...#......#........##.##...........#....#.....####...#......#........##.##...........#....#.....##",
        "####################################################################################################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Random 2"
    sol_cost, sol_hist, sol_solutions = None, None, None
    w, h = 13, 13
    prices = [81.11, 16.64, 81.55, 10.31, 1.38, 93.48, 40.61]
    plan = [
        "#############",
        "#...#.......#",
        "#.........#.#",
        "#........#..#",
        "#.........#.#",
        "#.##........#",
        "#........#..#",
        "#.#.#..#...##",
        "##....#..#..#",
        "##.........##",
        "#.#..#..##..#",
        "#......#....#",
        "#############",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Random 3"
    sol_cost, sol_hist, sol_solutions = None, None, None
    w, h = 13, 11
    prices = [81.11, 16.64, 81.55, 10.31, 1.38, 93.48, 40.61]
    plan = [
        "#############",
        "#........#..#",
        "#.........#.#",
        "#.##........#",
        "#........#..#",
        "#.#.#..#...##",
        "##....#..#..#",
        "##.........##",
        "#.#..#..##..#",
        "#......#....#",
        "#############",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    name = "Orientation N-S"
    sol_cost, sol_hist, sol_solutions = 18992.56, "36 56 232 46 8 0 0", 6718464
    w, h = 100, 23
    prices = [71.51, 75.49, 48.69, 92.90, 6.34, 72.82, 70.65]
    plan = [
        "####################################################################################################",
        "#......#...#..........#......#...#..........#......#...#..........#......#...#..........#......#...#",
        "##.....#...#...#......##.....#...#...#......##.....#...#...#......##.....#...#...#......##.....#...#",
        "#.#....#...#...#......#.#....#...#...#......#.#....#...#...#......#.#....#...#...#......#.#....#...#",
        "#..#...#...#...#......#..#...#...#...#......#..#...#...#...#......#..#...#...#...#......#..#...#...#",
        "#...#..#...#...#..#####...#..#...#...#..#####...#..#...#...#..#####...#..#...#...#..#####...#..#...#",
        "#..........#...#.....##..........#...#.....##..........#...#.....##..........#...#.....##..........#",
        "#....##....#...#....#.#....##....#...#....#.#....##....#...#....#.#....##....#...#....#.#....##....#",
        "#...#.#....#...#...#..#...#.#....#...#...#..#...#.#....#...#...#..#...#.#....#...#...#..#...#.#....#",
        "#..#..#....#...#..#...#..#..#....#...#..#...#..#..#....#...#..#...#..#..#....#...#..#...#..#..#....#",
        "#.....#....#..........#.....#....#..........#.....#....#..........#.....#....#..........#.....#....#",
        "####################################################################################################",
        "#....#.....#..........#....#.....#..........#....#.....#..........#....#.....#..........#....#.....#",
        "#....#..#..#...#..#...#....#..#..#...#..#...#....#..#..#...#..#...#....#..#..#...#..#...#....#..#..#",
        "#....#.#...#..#...#...#....#.#...#..#...#...#....#.#...#..#...#...#....#.#...#..#...#...#....#.#...#",
        "#....##....#.#....#...#....##....#.#....#...#....##....#.#....#...#....##....#.#....#...#....##....#",
        "#..........##.....#...#..........##.....#...#..........##.....#...#..........##.....#...#..........#",
        "#...#..#...#####..#...#...#..#...#####..#...#...#..#...#####..#...#...#..#...#####..#...#...#..#...#",
        "#...#...#..#......#...#...#...#..#......#...#...#...#..#......#...#...#...#..#......#...#...#...#..#",
        "#...#....#.#......#...#...#....#.#......#...#...#....#.#......#...#...#....#.#......#...#...#....#.#",
        "#...#.....##......#...#...#.....##......#...#...#.....##......#...#...#.....##......#...#...#.....##",
        "#...#......#..........#...#......#..........#...#......#..........#...#......#..........#...#......#",
        "####################################################################################################",
    ]
    examples[name] = (sol_cost, sol_hist, sol_solutions, w, h, prices, plan)

    def get_example(self):
        return self.examples[EXAMPLE]


@dataclass(frozen=True)
class Piece:
    name: str
    points: FrozenSet[Point]
    price: int
    piece_type: int
    _hash: int  # Add a private attribute to store the pre-calculated hash

    def __init__(self, name: str, points: Set[Point], price: int, piece_type: int, histogram: Tuple[int, ...]):
        object.__setattr__(self, "points", frozenset(points))
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "price", price)
        object.__setattr__(self, "piece_type", piece_type)
        object.__setattr__(self, "histogram", histogram)
        object.__setattr__(self, "_hash", hash(self.points))

    def __eq__(self, other):
        return self.points == other.points

    def __repr__(self) -> str:
        return f"{self.name} at {min(self.points)}"

    def __hash__(self):
        return self._hash

    def place(self, p: Point):
        piece_hash = self._hash  # Use precomputed hash instead of recomputing

        if piece_hash in PIECE_LOOKUP and p in PIECE_LOOKUP[piece_hash]:
            return PIECE_LOOKUP[piece_hash][p]
        if PIECE_LOOKUP.get(piece_hash) is None:
            PIECE_LOOKUP[piece_hash] = {}

        new_points = {(x + p[0], y + p[1]) for x, y in self.points}
        new_piece = Piece(self.name, new_points, self.price, self.piece_type, self.histogram)

        PIECE_LOOKUP[piece_hash][p] = new_piece
        return new_piece

    def print_piece(self):
        row_mid = 2
        col_mid = 2

        points = [(x[0] + row_mid, x[1] + col_mid) for x in self.points]
        for row in range(7):
            for col in range(7):
                p = row, col
                if p in points:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")

    def get_normalized_points(self):
        min_point = min(self.points)
        res = frozenset((r - min_point[0], c - min_point[1]) for r, c in self.points)
        return res


class FreeSpace:
    def __init__(self, points: Set[Point]):
        self.points = points
        self.placement_map = None

    def copy(self) -> "FreeSpace":  # Ensure placement_map sets are copied
        new_instance = FreeSpace(self.points.copy())  # Copy points set
        # Deep copy placement map if it exists
        if self.placement_map is not None:
            # Use set copy for inner sets
            new_instance.placement_map = {k: v.copy() for k, v in self.placement_map.items()}
        else:
            new_instance.placement_map = None
        return new_instance  # [source: 45]

    def contains(self, other: frozenset) -> bool:
        return other.issubset(self.points)

    def reset_placement_map(self):
        """Does a first initialization of the placement map"""
        placement_map = defaultdict(set)
        for start_point in self.points:
            for piece in PIECES:
                placed_piece = piece.place(start_point)
                if placed_piece.points.issubset(self.points):
                    for p in placed_piece.points:
                        placement_map[p].add(placed_piece)
        self.placement_map = placement_map

    def get_next_placed_pieces_candidates(self):
        placement_map = self.placement_map

        # Find first entry in placement map that has the least amount of pieces (greater than 0)
        min_val = min(len(val) for val in placement_map.values() if len(val) > 0)
        points_with_min_val = [key for key, val in placement_map.items() if len(val) == min_val]
        first_point_with_min_val = min(points_with_min_val)
        candidate_pieces = placement_map[first_point_with_min_val]
        candidate_pieces = list(candidate_pieces)
        candidate_pieces.sort(key=lambda x: x.price)

        if not candidate_pieces:
            print("ERROR, THIS SHOULD NOT HAPPEN")

        return candidate_pieces

    def estimated_remaining_costs(self) -> int:
        return len(self.points) // 4 * PIECES[0].price

    def get_free_space_signature(self) -> int:
        """Generates a hashable signature for the free space."""
        return hash(frozenset(self.get_normalized_points()))

    def get_normalization_vector(self) -> Point:
        if not self.points:
            return (0, 0)
        return min(self.points)

    def get_normalized_transformations(self) -> List[FrozenSet[Point]]:
        normalized_points = self.get_normalized_points()
        transformations = {normalized_points}
        for _ in range(3):
            normalized_points = frozenset((-c, r) for r, c in normalized_points)
            turned_free_space = FreeSpace(normalized_points)
            transformations.add(turned_free_space.get_normalized_points())
        return transformations

    def get_normalized_points(self):
        if not self.points:
            return frozenset()
        min_point = self.get_normalization_vector()
        res = frozenset((r - min_point[0], c - min_point[1]) for r, c in self.points)
        return res

    def is_subset(self, other: "FreeSpace") -> bool:
        return self.points.issubset(other.points)

    def is_not_multiple_of_4(self) -> bool:
        return len(self.points) % 4 != 0

    def print(self):
        num_rows = H  # Use global H # [source: 52]
        num_cols = W  # Use global W
        RED = "\033[91m"
        RESETCOL = "\x1b[0m"
        for r in range(num_rows):
            for c in range(num_cols):
                p = r, c
                if p in self.points:
                    print(RED + "." + RESETCOL, end="")  # Show free points clearly # [source: 53]
                elif p in board_dict:
                    if board_dict[p] == ".":
                        print("o", end="")
                    else:
                        print(board_dict[p], end="")
            print("")  # End border
        print(f"Free points: {len(self.points)}")  # Show count
        print("")

    def segment_in_islands(self) -> List["FreeSpace"]:
        def find_first_connected_island(points: Set[Point]) -> Set[Point]:
            if not points:
                return set()
            start_point = next(iter(points))
            visited = set()
            queue = deque([start_point])
            while queue:
                p = queue.popleft()
                if p in points and p not in visited:
                    visited.add(p)
                    r, c = p
                    for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                        neighbor = (nr, nc)
                        if neighbor in points:
                            queue.append(neighbor)
            return visited

        islands = []
        remaining_points = self.points.copy()  # Work on a copy

        # Get a reference to the parent's placement map *before* segmenting
        parent_placement_map = self.placement_map

        if parent_placement_map is None:
            print("Warning: Parent placement map is None during segmentation.")
            pass  # Or raise error

        while remaining_points:
            island_points = find_first_connected_island(remaining_points)
            if not island_points:
                break

            new_island = FreeSpace(island_points)

            # --- Build island's placement map by filtering parent map ---
            new_island.placement_map = defaultdict(set)  # Initialize empty map
            candidate_pieces: Set[Piece] = set()

            # 1. Collect all pieces touching the island area from the parent map
            if parent_placement_map:  # Check again if parent map exists
                for p in island_points:
                    if p in parent_placement_map:
                        candidate_pieces.update(parent_placement_map[p])

            # 2. Filter candidates and populate the new map
            for piece in candidate_pieces:
                # Check if the piece is fully contained within this island
                if piece.points.issubset(island_points):
                    # If yes, add it to the new map for all points it covers
                    for p_in_piece in piece.points:
                        # No need to check if p_in_piece is in island_points again,
                        # because we already know the whole piece is.
                        new_island.placement_map[p_in_piece].add(piece)

            islands.append(new_island)
            remaining_points -= island_points

        islands.sort(key=lambda x: len(x.points))  # Sort by size
        return islands

    def size(self) -> int:
        return len(self.points)

    def subtract(self, other: Set[Point]):
        self.points -= other
        for point in other:
            if point in self.placement_map:
                pieces_to_remove = self.placement_map[point].copy()
                for piece in pieces_to_remove:
                    for p in piece.points:
                        if p in self.placement_map:
                            self.placement_map[p].discard(piece)
                del self.placement_map[point]

    def union(self, other: Set[Point]):
        """Incrementally add `other` points back and update `placement_map`"""
        self.points.update(other)  # Use update for sets

        # Initialize placement_map for newly added points
        for p in other:
            if p not in self.placement_map:
                self.placement_map[p] = set()

        #  Calculate points to check for potential start_points
        # We only need to check points that are *actually free* in the updated space
        potential_start_points = calculate_neighborhood(other)
        valid_start_points = potential_start_points.intersection(self.points)  # Ensure start point is free

        # 4. Iterate only through potential start_points in the neighborhood
        for start_point in valid_start_points:
            for piece in PIECES:  # PIECES should be accessible (e.g., global)
                placed_piece = piece.place(start_point)

                if placed_piece.points.issubset(self.points):
                    for p in placed_piece.points:
                        if p in self.placement_map:
                            self.placement_map[p].add(placed_piece)


def myPrint(*args, end: str = "\n") -> None:
    # print(*args, file=sys.stderr, flush=True, end=end)
    if LOGGING:
        logging.debug(*args)


def debug_print(free_points, piece):
    num_rows = H  # Use global H # [source: 52]
    num_cols = W  # Use global W
    RED = "\033[91m"
    RESETCOL = "\x1b[0m"
    for r in range(num_rows):
        for c in range(num_cols):
            p = r, c
            if p in piece.points:
                print(RED + "O" + RESETCOL, end="")
            elif p in free_points.points:
                print(RED + "." + RESETCOL, end="")  # Show free points clearly # [source: 53]
            elif p in board_dict:
                if board_dict[p] == ".":
                    print("o", end="")
                else:
                    print(board_dict[p], end="")
        print("")  # End border
    print(f"Free points: {len(free_points.points)}")  # Show count
    print("")


def get_cost(histogram: Tuple[int, ...]) -> int:
    return sum(histogram[i] * PRICES[i] for i in range(7))


def calculate_neighborhood(points_to_add: Set[Point]) -> Set[Point]:
    """Calculates the set of points within a given Manhattan distance."""
    neighborhood_points: Set[Point] = set()
    board_width = W
    board_height = H
    max_dist = 4

    for r, c in points_to_add:
        # Iterate through rows within distance
        for dr in range(-max_dist, max_dist + 1):
            rem_dist = max_dist - abs(dr)
            for dc in range(-rem_dist, rem_dist + 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < board_height and 0 <= nc < board_width:
                    neighborhood_points.add((nr, nc))
    return neighborhood_points


def update_best_cost(best_cost: int, cost_so_far: int, solution) -> int:
    if solution == "No solution" or solution == "Not explored":
        return best_cost
    best_cost = min(best_cost, get_cost(solution) + cost_so_far)
    return best_cost


def get_start_parameters(print_input: bool = False) -> Tuple[FreeSpace, int, int, Dict[Point, str]]:
    global PIECES, PRICES

    w, h = 0, 0
    prices = []
    plan = []

    if HOME_PC:
        sol_cost, sol_hist, sol_solutions, w, h, prices, plan = Examples().get_example()
        print(f"\n{sol_cost}  {sol_hist}  {sol_solutions}")

    else:
        w, h = [int(i) for i in input().split()]
        prices = [float(i) for i in input().split()]
        plan = []
        for i in range(h):
            plan.append(input())

    prices = [round(x * 100) for x in prices]
    PRICES = prices

    PIECES = []
    for name, piece_type, points, histogram in RAW_PIECES:
        new_piece = Piece(
            name=name,
            points=set(points),  # Pass as set initially
            price=prices[piece_type],
            piece_type=piece_type,
            histogram=histogram,
        )
        PIECES.append(new_piece)
    PIECES.sort(key=lambda piece: piece.price)  # [source: 70]

    # Build initial CACHE
    for piece in PIECES:
        CACHE[piece.get_normalized_points()] = (piece.histogram, 1)

    # Create initial board dictionary and free points set
    initial_board_dict = dict()
    free_points_set = set()
    for r in range(h):
        for c in range(w):
            p = r, c
            char = plan[r][c]
            initial_board_dict[p] = char
            if char == ".":
                free_points_set.add(p)

    # Create initial FreeSpace object
    initial_free_space = FreeSpace(free_points_set)  # Pass the mutable set

    return initial_free_space, w, h, initial_board_dict


def update_cache(normalized_points: FrozenSet[Point], value: Tuple[str, int]):
    transformations = {normalized_points}
    for _ in range(3):
        normalized_points = frozenset((-c, r) for r, c in normalized_points)
        turned_free_space = FreeSpace(normalized_points)
        transformations.add(turned_free_space.get_normalized_points())
    for transformation in transformations:
        CACHE[transformation] = value


def dfs(free_points: FreeSpace, cost_so_far: int, best_cost: int, level):
    normalized_points = free_points.get_normalized_points()
    all_solutions = []

    skip_to_end = False

    if a == free_points.points:
        True

    # Memoization; if there is solution or no solution skip to end, if preivously not explored, decide if we explore this time based on pruning
    if normalized_points in CACHE:
        best_solution, num_solutions = CACHE[normalized_points]
        if best_solution != "No solution" and best_solution != "Not explored":
            skip_to_end = True
        elif best_solution == "No solution":
            skip_to_end = True
        elif best_solution == "Not explored":
            if PRUNE:
                if cost_so_far + free_points.estimated_remaining_costs() > best_cost:
                    skip_to_end = True

    # If any island is too small, abort
    islands = free_points.segment_in_islands()
    if any(island.is_not_multiple_of_4() for island in islands):
        update_cache(normalized_points, ("No solution", 0))
        return best_cost

    # Multiple islands
    if not skip_to_end and len(islands) > 1:
        for island in islands:
            # cost_of_all_solved_islands = sum(get_cost(x[0]) for x in all_solutions)
            # updated_cost_so_far = cost_so_far + cost_of_all_solved_islands
            # laid_pieces_so_far = sum(x[1] for x in all_solutions)
            # remaining_pieces = (free_points.size() // 4) - laid_pieces_so_far
            # estimated_min_cost = updated_cost_so_far + (remaining_pieces * PIECES[0].price)
            # if PRUNE:
            # if estimated_min_cost > best_cost + 1:  # Not worth exploring more islands; abort
            # return "Not explored", 0, best_cost

            if a == free_points.points:
                True

            _ = dfs(island, 0, LARGE_NUM, level + 1)
            returned_solution, returned_num = CACHE[island.get_normalized_points()]
            if returned_solution == "Not explored":
                print("   " * level + "ERROR: This should not happen")

            if returned_solution == "No solution":
                update_cache(normalized_points, ("No solution", 0))
                myPrint("   " * level + f"Aborted multiple islands due to no solution {island.points}")
                return best_cost

            all_solutions.append((returned_solution, returned_num))
        myPrint("   " * level + f"Consolidating Solutions for {len(all_solutions)} islands {island.points}")
        for x in all_solutions:
            myPrint("   " * level + f" - {x}")
        histogram_collection = [x[0] for x in all_solutions]
        best_solution = tuple(sum(x) for x in zip(*histogram_collection))
        num_solutions = math.prod([x[1] for x in all_solutions])
        myPrint("   " * level + f"Best solution: {best_solution}")

    # One island
    elif not skip_to_end and len(islands) == 1:
        all_sources = []
        island = islands[0]  # Use the island object

        if a == free_points.points:
            True

        candidate_list = island.get_next_placed_pieces_candidates()
        for n, placed_piece in enumerate(candidate_list):
            # MAIN !
            island.subtract(placed_piece.points)
            best_cost = dfs(island, cost_so_far + placed_piece.price, best_cost, level + 1)
            all_sources.append(set(x for x in island.points))
            returned_solution, returned_num = CACHE[island.get_normalized_points()]
            island.union(placed_piece.points)

            # Unify piece and solution if solution found; add to all_solutions
            if returned_solution != "No solution" and returned_solution != "Not explored":
                returned_solution = tuple(sum(x) for x in zip(placed_piece.histogram, returned_solution))
            all_solutions.append((returned_solution, returned_num))

        if a == free_points.points:
            True

        myPrint("   " * level + f"Consolidating Solutions for {free_points.points}")
        for x, y in zip(all_solutions, all_sources):
            myPrint("   " * level + f" - {x} von {y}")

        # Impossible, no solutions, prepare to store "No Solution" in cache
        if all([x[0] == "No solution" for x in all_solutions]):
            best_solution = "No solution"
            num_solutions = 0

        # We didn't explore space (expensive) or no solution, CACHE not explored yet (for later)
        elif all([x[0] == "No solution" or x[0] == "Not explored" for x in all_solutions]):
            # elif any([x[0] == "Not explored" for x in all_solutions]):
            best_solution = "Not explored"
            num_solutions = 0

        else:
            all_solutions = [x for x in all_solutions if x[0] != "No solution" and x[0] != "Not explored"]
            min_cost = min(get_cost(sol) for sol, _ in all_solutions)
            all_solutions = [x for x in all_solutions if get_cost(x[0]) == min_cost]
            best_solution = all_solutions[0][0]
            num_solutions = sum(sol[1] for sol in all_solutions)  # Sum counts for min cost solutions
            myPrint("   " * level + f"Best solution: {best_solution}")

    # Update best cost and cache
    best_cost = update_best_cost(best_cost, cost_so_far, best_solution)
    update_cache(normalized_points, (best_solution, num_solutions))

    return best_cost


# ************************************************************************************
# --- Global Variables ---
# EXAMPLE = "Studio 1"
# EXAMPLE = "Studio 2"
# EXAMPLE = "One Bedroom"
# EXAMPLE = "One Bedroom 2"
# EXAMPLE = "Two Bedroom"
# EXAMPLE = "Many Possibilities"
EXAMPLE = "Many Possibilities Single"
# EXAMPLE = "Conformity"
# EXAMPLE = "Conformity 2"
# EXAMPLE = "Conformity 3"
# EXAMPLE = "Tetris"
# EXAMPLE = "Random"
# EXAMPLE = "Random 2"
# EXAMPLE = "Random 3"
# EXAMPLE = "Orientation N-S"

PRUNE = True
LOGGING = False
DEBUG = False
a = {(2, 4), (2, 3), (2, 2), (3, 2)}


# DIFFERENT_KEYS = joblib.load("_different_keys.ext")

start_time = time.time()
LARGE_NUM = 10000000000
W, H = 0, 0
HOME_PC = True
PIECES = []
PRICES = []
CACHE = {}
PIECE_LOOKUP = {}

free_points_board, W, H, board_dict = get_start_parameters(print_input=False)
free_points_board.reset_placement_map()

best_cost = dfs(free_points_board, 0, LARGE_NUM, 0)
best_solution, num_solutions = CACHE[free_points_board.get_normalized_points()]


if HOME_PC:
    print(f"{best_cost/100:.2f}", end="  ")
    print(*[x for x in best_solution], sep=" ", end="  ")
    print(num_solutions)

else:
    print(f"{best_cost/100:.2f}")
    print(*[x for x in best_solution], sep=" ")
    print(num_solutions)
# joblib.dump(CACHE, "_CACHE2.ext")

# ************************************************************************************
# PIECES = [I     Vier  T     L     J    Z     S]
# prices = [7151, 7549, 4869, 9290, 634, 7282, 7065]
