import itertools


def concatenate_circles(c1, c2):
    r1 = c1["radius"]
    r2 = c2["radius"]
    d = (r1 + r2) ** 2 - (r1 - r2) ** 2
    d = d**0.5
    c2["center"] = (c1["center"][0] + d, r2)


def full_length(lst):
    start = min([x["center"][0] - x["radius"] for x in lst])
    end = max([x["center"][0] + x["radius"] for x in lst])
    return end - start


def test_circle(lst):
    lst[0]["center"] = (0, lst[0]["radius"])
    for i in range(0, len(lst) - 1):
        a = lst[i]
        b = lst[i + 1]
        concatenate_circles(a, b)
    return full_length(lst)


# test_radius = [900, 970, 567, 965]
# test_radius = [3, 3, 3, 3]
# test_radius = [13, 8, 2, 1, 3, 1, 5, 2]
test_radius = [3, 380, 135, 150, 542, 93, 10]

CIRCLES = []
for radius in test_radius:
    t = {"center": (0, radius), "radius": radius}
    CIRCLES.append(t)

permutations = list(itertools.permutations(CIRCLES))

r = [test_circle(perm) for perm in permutations]
r = min(r)
print(r)

for perm in permutations:
    if test_circle(perm) == r:
        print(test_circle(perm))
        for x in perm:
            print(x)
        break



# https://www.desmos.com/calculator/jti4dp20np