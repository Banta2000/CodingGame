import sys
import os
from typing import Any, Tuple, List

HOME_PC: bool = os.getenv("HOME_PC") == "True"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Get Game Start Parameters
def get_start_parameters():
    if HOME_PC:
        operation = "ENCODE"
        pseudo_random_number = 4
        rotors = ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ"]
        message = "AAA"

        operation = "ENCODE"
        pseudo_random_number = 7
        rotors = ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "EKMFLGDQVZNTOWYHXUSPAIBRCJ"]
        message = "WEATHERREPORTWINDYTODAY"
    else:
        operation = input()
        pseudo_random_number = int(input())
        rotors = [input() for _ in range(3)]
        message = input()

    return operation, pseudo_random_number, rotors, message


def cesar_shift_encode(message, num):
    res = ""
    anchor = ord("A")
    for i, char in enumerate(message):
        char = ord(char) - anchor + num + i
        char = char % 26
        char = chr(char + anchor)
        res += char
    return res


def cesar_shift_decode(message, num):
    res = ""
    anchor = ord("A")
    for i, char in enumerate(message):
        char = ord(char) - anchor - num - i
        char = char % 26
        char = chr(char + anchor)
        res += char
    return res


def rotor_encode(message, rotor):
    res = ""
    for char in message:
        alphabet_index = ord(char) - ord("A")
        res += rotor[alphabet_index]
    return res


def rotor_decode(message, rotor):
    res = ""
    for char in message:
        rotor_index = rotor.index(char)
        res += ABC[rotor_index]
    return res


# ********************************************************


operation, pseudo_random_number, rotors, message = get_start_parameters()

if operation == "ENCODE":
    message = cesar_shift_encode(message, pseudo_random_number)
    message = rotor_encode(message, rotors[0])
    message = rotor_encode(message, rotors[1])
    message = rotor_encode(message, rotors[2])
elif operation == "DECODE":
    message = rotor_decode(message, rotors[2])
    message = rotor_decode(message, rotors[1])
    message = rotor_decode(message, rotors[0])
    message = cesar_shift_decode(message, pseudo_random_number)

print(message)
