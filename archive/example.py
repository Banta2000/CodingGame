# Define two sets
set_a = {1, 2, 3}
set_b = {1, 2, 3, 4, 5}

# Check if set_a is a subset of set_b
is_subset = set_a.issubset(set_b)
print(is_subset)  # Output: True

# Check if set_b is a subset of set_a
is_subset = set_b.issubset(set_a)
print(is_subset)  # Output: False

# Another example with different sets
set_c = {1, 2, 6}
is_subset = set_c.issubset(set_b)
print(is_subset)  # Output: False
