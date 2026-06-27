from typing import Any, Tuple, List

SAMPLES: dict[str, list[str]] = {
    "data1": ["1", "1", "3 1"],
    "data2": ["4", "4", "3 2", "4 1", "7 6", "7 1"],
    "data3": [
        "2",
        "4",
        "3 1",
        "3 2",
        "4 0",
        "4 0",
    ],
}


from typing import Optional


def get_start_parameters(start_data):
    def read_input(data):
        if data != None:
            line = data.pop(0)
            return line
        else:
            return input()

    data = SAMPLES[start_data] if start_data in SAMPLES else None

    r = int(read_input(data))
    v = int(read_input(data))
    VAULTS = [[int(j) for j in read_input(data).split()] for _ in range(v)]
    ROBBERS = {i: 0 for i in range(r)}
    return VAULTS, ROBBERS


def time_to_solve_one_tresor(total_chars: int, num_digits: int) -> int:
    num_vowels = total_chars - num_digits
    return (10**num_digits) * (5**num_vowels)


def get_free_robber_indes(robbers: dict[int, int]) -> int:
    # Returns the key of the robber with the least time
    min_val = min(robbers.values())
    for k, v in robbers.items():
        if v == min_val:
            return k


# ********************************************************

VAULTS, ROBBERS = get_start_parameters("data3")
for vault in VAULTS:
    time_needed = time_to_solve_one_tresor(vault[0], vault[1])
    free_robber = get_free_robber_indes(ROBBERS)
    ROBBERS[free_robber] += time_needed

print(max(ROBBERS.values()))



The Core Verification and Cloud reCAPTCHA have initiated an experiment to evaluate a new Hand Gesture verification method. This new anti-abuse method is being rolled out as an opt-in trial for 1,000 third-party websites utilizing the free tier of reCAPTCHA. 

In addition, YouTube has recently announced the availability of a new feature called "Likeness Detection", powered by Core Verifications. This tool, now in open beta for all creators in the YouTube Partner Program, is designed to empower and protect the creator community. The technology allows creators to easily detect, manage, and request the removal of unauthorized videos made with their facial likeness.
