# Print the binary stream with alternating colors for alternating numbers
# Underneath it, print the the indexes from 0 - 9; repeating


def get_input():
    n = int(input())
    data = [input() for _ in range(n)]
    return [int(b, 2) for b in data]


def print_binary_sequence(how_many_numbers):
    COLS = {0: "\033[94m", 1: "\033[91m"}  # Blue for 0  # Red for 1
    for i in range(how_many_numbers):
        col = COLS[i % 2]
        num = bin(i)[2:]
        print(f"{col}{num}", end="")
    print("\033[0m")
    for i in range(50):
        num = i % 10
        print(num, end="")
    print()


def starting_index_for_x_digits():
    digit_index = 2
    num_digits = 0
    while True:
        num_digits += 1
        if num_digits != 1:
            num_with_x_digits = 2 ** (num_digits - 1)
            digit_index += num_with_x_digits * num_digits
        yield num_digits + 1, digit_index


def find_digits_size_and_start_index_for_n_index(n):
    # In the stream of binary numbers, looks for what section the index n is in
    # Section means "what is the size (number of digits) of binary numbers"
    # Returns the size of binary numbers and the starting index of that section"
    # Return: size, starting_index
    gen = starting_index_for_x_digits()
    old_size, old_start_index = next(gen)
    while True:
        new_size, new_start_index = next(gen)
        if new_start_index > n:
            return old_size, old_start_index
        old_size, old_start_index = new_size, new_start_index


def get_result_for_index(target_index):
    if target_index == 0:
        return 0
    if target_index == 1:
        return 1
    num_digits, start_index = find_digits_size_and_start_index_for_n_index(target_index)
    # The relevant section begins at start_index and consists of numbers with num_digits size

    offset_index = target_index - start_index

    # At which'th number in the section does the target_index fall?
    whichth_number = offset_index // num_digits

    # What is the offset of the target_index within that number?
    offset_within_number = offset_index % num_digits

    # Binary representation of the 'th number in the section
    start_hex_with_n_digits = 2 ** (num_digits - 1)
    number = start_hex_with_n_digits + whichth_number
    binary_representation = bin(number)[2:]
    return str(binary_representation[offset_within_number])


# ***********************************************
# print_binary_sequence(18)
# target_index = 10
# res = get_result_for_index(10)
data = get_input()
for target_index in data:
    res = get_result_for_index(target_index)
    print(res)
