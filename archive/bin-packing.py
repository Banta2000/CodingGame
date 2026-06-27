import sys
import os
from typing import Any, Tuple
import copy
from itertools import combinations

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters() -> Game:
    if HOME_PC:
        test_cases_collection = [
            {"num_bins": 1, "items": [6, 5, 4, 3, 2, 1]},
            {"num_bins": 2, "items": [3, 3]},
            {"num_bins": 2, "items": [50, 20, 20, 20, 10]},
            {"num_bins": 3, "items": [150, 140, 130, 120, 110, 100]},
            {"num_bins": 4, "items": [100, 100, 100, 50, 50]},
            {"num_bins": 5, "items": [17, 17, 13, 8, 7, 7, 5, 4, 3, 2, 2]},
            {"num_bins": 2, "items": [38, 37, 36, 27, 22]},
            {"num_bins": 3, "items": [25, 22, 19, 15, 10, 2]},
            {"num_bins": 4, "items": [39, 34, 33, 28, 27, 20, 19, 18, 2]},
            {"num_bins": 5, "items": [38, 36, 31, 31, 28, 22, 21, 3]},
            {"num_bins": 3, "items": [205, 168, 145, 101, 100, 95, 68, 65, 39, 36, 29, 25, 11]},
            {"num_bins": 4, "items": [383, 311, 296, 234, 201, 152, 59, 52, 43, 41, 38, 32, 29, 26, 17]},
        ]

    else:
        num_test_cases = int(input())
        test_cases_collection = []
        for _ in range(num_test_cases):
            line = [int(x) for x in input().split()]
            num_bins = line[0]
            items = line[2:]
            items_sorted = sorted(items, reverse=True)
            test_case = {"num_bins": num_bins, "items": items_sorted}
            test_cases_collection.append(test_case)

    # for x in test_cases_collection:
    # myPrint(x)

    return test_cases_collection


# Try all combinations of numbers to find one that sums to the target
def find_first_combination_that_equals_a_number(num_lst, target):
    for r in range(1, len(num_lst) + 1):  # Lengths of combinations (1 to len(num_lst))
        for comb in combinations(num_lst, r):
            if sum(comb) == target:
                return list(comb)
    return None


def can_list_of_items_be_divided_into_num_bins(num_bins, items):
    total_sum = sum(items)
    if total_sum % num_bins != 0:
        return False  # Can't divide if the total isn't divisible by the number of bins

    target_sum = total_sum // num_bins
    items.sort(reverse=True)  # Sorting helps optimize combination search

    for _ in range(num_bins):
        combination = find_first_combination_that_equals_a_number(items, target_sum)
        if combination is None:
            return False
        # Remove elements in the combination from the original list
        for num in combination:
            items.remove(num)

    return True


def can_list_of_items_be_divided_into_num_bins2(num_bins, items):
    total_sum = sum(items)
    if total_sum % num_bins != 0:
        return False  # Cannot divide if the total isn't divisible by the number of bins

    target_sum = total_sum // num_bins
    items.sort(reverse=True)  # Sorting helps optimize the search by using larger numbers first
    used = [False] * len(items)  # Track which items have been used

    def backtrack(bin_idx, current_sum):
        # Base case: If all bins are filled successfully, we're done
        if bin_idx == num_bins:
            return True

        # If the current bin is filled, move to the next bin
        if current_sum == target_sum:
            return backtrack(bin_idx + 1, 0)

        # Try each unused item
        for i in range(len(items)):
            if not used[i] and current_sum + items[i] <= target_sum:
                # Choose the item
                used[i] = True
                if backtrack(bin_idx, current_sum + items[i]):
                    return True
                # Backtrack: Undo the choice
                used[i] = False

        return False  # No valid configuration found for this bin

    # Start the backtracking process with the first bin
    return backtrack(0, 0)


def can_list_be_evenly_divided(num_bins, items):
    total_sum = sum(items)
    if total_sum % num_bins != 0:
        return False  # If the total isn't divisible by num_bins, it's impossible

    target_sum = total_sum // num_bins
    items.sort(reverse=True)  # Sorting helps optimize the search
    bins = [0] * num_bins  # Track the sum of items in each bin

    def backtrack(idx):
        if idx == len(items):
            # Check if all bins have the target sum
            return all(b == target_sum for b in bins)

        # Try placing the current item into each bin
        for i in range(num_bins):
            if bins[i] + items[idx] <= target_sum:
                # Place item in bin
                bins[i] += items[idx]
                if backtrack(idx + 1):
                    return True
                # Backtrack
                bins[i] -= items[idx]

            # Optimization: If this bin is empty and we can't use it, no point trying other empty bins
            if bins[i] == 0:
                break

        return False

    return backtrack(0)


# ********************************************************

test_cases_collection = get_start_parameters()
original = copy.deepcopy(test_cases_collection)

result = [
    can_list_be_evenly_divided(case["num_bins"], case["items"]) for case in test_cases_collection
]
result = ["yes" if x else "no" for x in result]

for case, res in zip(original, result):
    myPrint("Case:", case)
    myPrint("Sum", sum(case["items"]), "Target", sum(case["items"]) // case["num_bins"])
    print(res)
