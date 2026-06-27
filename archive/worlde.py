import sys
import os
from typing import Any, Tuple

HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


def get_input() -> dict[str, Any]:
    GS = {}
    if HOME_PC:
        GS["test"] = ["ABCSDE"]
    else:
        _ = int(input())  # Number of words in the word set
        result = [word for word in input().split()]
    return result


def build_word_made_of_most_frequent_letters(word_list: list[str]) -> str:
    word_length = len(word_list[0])
    new_word = ""

    for i in range(word_length):
        letter_frequencies = {}

        for word in word_list:
            letter = word[i]
            letter_frequencies[letter] = letter_frequencies.get(letter, 0) + 1

        most_frequent_letter = max(letter_frequencies, key=letter_frequencies.get)
        new_word += most_frequent_letter

    return new_word


# ********************************************************

word_list = get_input()


while True:
    feedback = [int(i) for i in input().split()]
    if feedback[0] != 0:
        for i, (code, letter) in enumerate(zip(feedback, new_word)):
            if code == 1:
                word_list = [word for word in word_list if letter not in word]
            elif feedback[i] == 2:
                word_list = [word for word in word_list if letter in word and word[i] != letter]
            elif feedback[i] == 3:
                word_list = [word for word in word_list if word[i] == letter]

    new_word = build_word_made_of_most_frequent_letters(word_list)
    print(new_word)
