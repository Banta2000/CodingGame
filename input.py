f = open('input.txt', 'r')
pieces = []
for _ in range(33):
    tmp = []
    for _ in range(6):
        tmp.append(f.readline()[:-1])
    pieces.append(tmp)
