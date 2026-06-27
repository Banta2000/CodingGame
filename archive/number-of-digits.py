from typing import Any, Tuple, List

Point = Tuple[int, int]
Board = dict[Point, Any]


def get_start_parameters(start_data: str | None = None):
    n = int(input())
    k = int(input())
    return n, k


def is_relevant_number(n: int) -> bool:
    # Checks if the number is x000
    s = str(n)[1:]
    comp = "0" * len(s)
    return s == comp


def count_relevant_numbers(n: int, k: int) -> int:
    # Counts number of k in n
    digits = [x for x in str(n)]
    k_str = str(k)
    return digits.count(k_str)


def count_up_to_that_number(num_cap: int, num_to_find: int) -> int:
    # Efficiently counts how many times digit num_to_find appears from 0 to num_cap inclusive
    d = num_to_find
    n = num_cap
    if n < 0:
        return 0
    total = 0
    factor = 1
    while factor <= n:
        higher = n // (factor * 10)
        current = (n // factor) % 10
        lower = n % factor
        if d != 0:
            total += higher * factor
            if current > d:
                total += factor
            elif current == d:
                total += lower + 1
        else:
            if higher > 0:
                total += (higher - 1) * factor
                if current == 0:
                    total += lower + 1
                else:
                    total += factor
        factor *= 10
    # Include the single '0' present in the number 0 itself
    if d == 0:
        total += 1
    return total


def count_up_to_that_number_cached(target_num: int, num_to_find: int, CACHE) -> int:
    # Delegate to the exact formula; keeps signature for compatibility
    return count_up_to_that_number(target_num, num_to_find)


def first_digit(n: int) -> int:
    return int(str(n)[0])


def check_test_case(test_case):
    CAP_NUMBER, NUM_TO_FIND, EXPECTED = test_case
    res = count_up_to_that_number(CAP_NUMBER, NUM_TO_FIND)
    print(f"{CAP_NUMBER=} {NUM_TO_FIND=} {EXPECTED=} {res=}")


def next_number(n: int) -> int:
    # Returns the next number that is x000
    s = str(n)
    if s[0] == "9":
        return int("1" + "0" * len(s))
    return int(str(int(s[0]) + 1) + "0" * (len(s) - 1))


def next_smaller(n: int, CACHE) -> int:
    keys = sorted(list(CACHE.keys()), reverse=True)
    for k in keys:
        if k <= n:
            return k
    return 0


def initialize_cache(CAP_NUMBER, NUM_TO_FIND) -> dict[int, int]:
    CACHE = {}
    CACHE_KEY = 100
    for i in range(CACHE_KEY + 1):
        if is_relevant_number(i):
            CACHE[i] = count_up_to_that_number(i, NUM_TO_FIND)

    while True:
        CACHE_KEY = next_number(CACHE_KEY)
        if CACHE_KEY > CAP_NUMBER:
            break
        NEW_RES = count_up_to_that_number_cached(CACHE_KEY, NUM_TO_FIND, CACHE)
        CACHE[CACHE_KEY] = NEW_RES

    return CACHE


# ********************************************************
test_cases = [
    [12, 2, 2],
    [0, 3, 0],
    [219, 5, 42],
    [4218, 4, 1461],
    [10000, 6, 4000],
    [248919, 7, 119682],
    [841772, 8, 458220],
    [1283048, 9, 732904],
    [824883294, 1, 767944060],
]

USE_STDIN = False  # set to True for CodinGame
if USE_STDIN:
    CAP_NUMBER, NUM_TO_FIND = get_start_parameters()
else:
    # Default to the last test case when running locally
    CAP_NUMBER, NUM_TO_FIND, _ = test_cases[2]

# for i in range(10001):
#     res = count_up_to_that_number(i, NUM_TO_FIND)
#     if is_relevant_number(i):
#         print(i, res)


# Quick self-checks using provided test_cases
for cap, digit, expected in test_cases:
    got = count_up_to_that_number(cap, digit)
    # Uncomment to see PASS/FAIL lines
    # print(f"cap={cap} digit={digit} expected={expected} got={got} -> {'OK' if got==expected else 'FAIL'}")

# Compute and print the final answer for the chosen CAP_NUMBER/NUM_TO_FIND
print(count_up_to_that_number(CAP_NUMBER, NUM_TO_FIND))
