import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input=False) -> Game:
    if HOME_PC:
        target_sum = 800
        items = [
            (900, "Nutri-Grain_Breakfast_Bar"),
            (850, "steak_200g"),
            (780, "soya_milk_vanilla_1LTR"),
            (760, "low-fat_cheese"),
            (650, "pork_200g"),
            (530, "lamb_250g"),
            (456, "Salted_Kaju_175_gms"),
            (380, "ham_100g"),
            (350, "quinoa_500g"),
            (250, "mustard_200g"),
            (230, "dark_chocolate_bar"),
            (220, "tomato_sauce_250ml"),
            (190, "pasta_500g"),
            (180, "milk_chocolate_bar"),
            (155, "pack_of_6_eggs"),
            (100, "pepper"),
        ]

    else:
        target_sum = int(input())
        n = int(input())
        items = []
        for _ in range(n):
            fname = input().split()
            name = "_".join(fname[:-1])
            price = int(fname[-1])
            items.append((price, name))

    items.sort(key=lambda x: x[0], reverse=True)

    if print_input:
        myPrint(target_sum)
        myPrint(items)

    return target_sum, items


# Return only the price of the items, sorted in descending order
def clean_items(items):
    items = [x[0] for x in items]
    return items


def find_num_combinations_to_attain_target(curr_sum: int, idx: int) -> int:
    global combinations
    for i in range(idx, len(items)):
        new_item = items[i]
        new_sum = curr_sum + new_item

        # If the item is too big, we break
        if new_sum > target_sum:
            continue

        # If the item fits in the bag, we check how many times we could add it (0 to 3)
        options = [curr_sum + new_item * j for j in range(1, 4)]
        options = [option for option in options if option <= target_sum]

        for option in options:
            # If the sum is equal to the target sum, we increment the combinations
            if option == target_sum:
                combinations += 1
                continue
            find_num_combinations_to_attain_target(option, i + 1)


# ********************************************************

target_sum, items = get_start_parameters(True)
items = clean_items(items)
combinations = 0
find_num_combinations_to_attain_target(0, 0)
print(combinations)
