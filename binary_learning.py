def b2s(num: int, len: int = 6) -> str:
    # Returns binary string representation of a int
    return bin(num)[2:].zfill(len)


def decompose_bin(num: int):
    # Returns a list of hot encodings for a bit
    # 01011 -> [1, 10, 1000]
    res = []
    incrementing = 1
    while incrementing <= num:
        if incrementing & num:
            res.append(incrementing)
        incrementing = incrementing << 1
    for n in res:
        print(b2s(n))


a = 0b1100
b = 0b1010

print("AND")
print(b2s(a))
print(b2s(b))
print(b2s(a & b))
print()


print("OR")
print(b2s(a))
print(b2s(b))
print(b2s(a | b))
print()

print("XOR")
print(b2s(a))
print(b2s(b))
print(b2s(a ^ b))
print()

print("Flip 2nd")
print(b2s(a))
print(b2s(a ^ (1 << 2)))
print()

print("Differences")
print(b2s(a))
print(b2s(b))
print(b2s(a ^ b))
print()

print("Number of Bits")
print(b2s(a))
print(a.bit_count())
print()

print("Shifting Right")
print(b2s(a))
print(b2s(a >> 1))
print(b2s(a >> 2))
print(b2s(a >> 3))
print()

print("Decompose", b2s(29))
decompose_bin(29)
print()

print("First Bit")
a = 0b10101000
print(b2s(a))
print(a.bit_length() - 1)
print()


# Create a mask for bit n: mask = 1 << n
# Mark bit n as visited: visited |= (1 << n)
# Check if bit n == 1 (check if visited): if visited & (1 << n):
# Unvisit node n (backtracking): visited &= ~(1 << n)
# Flip node n: state ^= (1 << n)
# Find differences: state_1 ^ state_2
# Validating a transition in O(1) time
# if (my_keys & REQUIRED_KEYS) == REQUIRED_KEYS:
# Number of 1's in state: num.bit.count()
# Set all 1 bits up to (but excluding) n: (1 << n) - 1). Ex n = 3: 0b111
# Clear all low bits up to n: state &= ~((1 << n) - 1)
# Index of highest set bit: state.bit_length() - 1, Ex: 0b10101000 -> 7
# Index of lowest set bit: (state & -state).bit_length() - 1, Ex: 0b10101000 -> 3
# Clear lowest set bit: state &= (state - 1). Ex: 0b10101000 -> 0b10100000
# c.bit_length() - 1
# Set all bits up to n: (1 << (n + 1)) - 1. Ex n = 3: 0b1111
