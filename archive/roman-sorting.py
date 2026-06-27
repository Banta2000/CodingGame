num = 323
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


n = int(input())
nums = [int(input()) for _ in range(n)]

converted_nums = [(num, convert_to_roman(num)) for num in nums]
converted_nums.sort(key=lambda x: x[1])
sorted_nums = [num for num, _ in converted_nums]
print(" ".join(map(str, sorted_nums)))
