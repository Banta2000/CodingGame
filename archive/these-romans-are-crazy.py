import sys
import math

mapper = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    90: "XC",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I",
}


def convert_to_roman(num):
    res = ""
    while num > 0:
        for key in sorted(mapper.keys(), reverse=True):
            if num >= key:
                res += mapper[key]
                num -= key
                break
    return res


inverse_mapper = {v: k for k, v in mapper.items()}


def convert_to_int(roman):
    num = 0
    i = 0
    while i < len(roman):
        if i + 1 < len(roman) and roman[i : i + 2] in inverse_mapper:
            num += inverse_mapper[roman[i : i + 2]]
            i += 2
        else:
            num += inverse_mapper[roman[i]]
            i += 1
    return num


# n = int(input())
# nums = [int(input()) for _ in range(n)]

# converted_nums = [(num, convert_to_roman(num)) for num in nums]
# converted_nums.sort(key=lambda x: x[1])
# sorted_nums = [num for num, _ in converted_nums]
# print(" ".join(map(str, sorted_nums)))


# rom_1 = input()
# rom_2 = input()
