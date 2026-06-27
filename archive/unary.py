HOME_PC = True
import sys
from itertools import groupby



def myPrint(lst):
    print("Debug messages...", lst, file=sys.stderr, flush=True)


def get_input():
    return True


def break_up_string(s):
    return ["".join(group) for _, group in groupby(s)]


def encode(s):
    result = ""
    if s[0] == "0":
        result += "00 "
    else:
        result += "0 "
    result += "0" * len(s)
    return result


# ********************************************************

if HOME_PC:
    myInput = "CC"
else:
    myInput = input()


myInput = [x for x in myInput]
myInput = "".join([bin(ord(char))[2:].zfill(7) for char in myInput])
myInput = break_up_string(myInput)

myInput = [encode(e) for e in myInput]
print(" ".join(myInput))
