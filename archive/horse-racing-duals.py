import sys
import math


n = int(input())
l = [int(input()) for _ in range(n)]
l.sort()

if len(l) == 2:
    print(l[1] - l[0])
    sys.exit()

res = []
for i in range(1, len(l) - 1):
    a = l[i] - l[i - 1]
    b = l[i + 1] - l[i]
    res.append(min(a, b))

print(min(res))
