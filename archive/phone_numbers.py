import sys


def myPrint(lst):
    print("Debug messages...", lst, file=sys.stderr, flush=True)


def count_keys(d):
    if not isinstance(d, dict) or not d:  # Base case: not a dict or empty dict
        return 0
    return len(d) + sum(
        count_keys(v) for v in d.values()
    )  # Count keys at current level + recursively count keys in nested dicts


def solve(telephones):
    root = {}

    for telephone in telephones:
        current = root
        for digit in telephone:
            if digit not in current:
                current[digit] = {}
            current = current[digit]

    print(count_keys(root))


# ********************************************************

# telephones = []
# n = int(input())
# for i in range(n):
#     telephones.append(input())

telephones = ["0412578440", "0412199803", "0468892011", "112", "15"]


solve(telephones)
