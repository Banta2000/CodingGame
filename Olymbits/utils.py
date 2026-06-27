def extract_user_actions():
    f = "extract_user_actions.txt"
    open(f)
    data = open(f).read()
    data = [line for line in data.split("\n") if line in ["UP", "LEFT", "RIGHT", "DOWN"]]

    # Checksum, number of actions % 3
    if len(data) % 3 != 0:
        print("ERROR: Incorrect number of actions")

    lookUp = {"UP": "U", "LEFT": "L", "RIGHT": "R", "DOWN": "D"}
    data = [lookUp[x] for x in data]

    p1 = [e for i, e in enumerate(data) if i % 3 == 0]
    p2 = [e for i, e in enumerate(data) if i % 3 == 1]
    p3 = [e for i, e in enumerate(data) if i % 3 == 2]
    return [p1, p2, p3]


def extract_patter_from_file(filename, pattern):
    open(filename)
    data = open(filename).read()
    data = [line for line in data.split("\n") if pattern in line]
    return data


data = extract_patter_from_file("todel.txt", "0 0 0 0 0 0 0")
for x in data:
    print(x)
