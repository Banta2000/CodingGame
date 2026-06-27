def getLetter(h, l, rows, letter):
    letter = letter.upper()
    letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?".find(letter)
    if letter == -1:
        letter = 26
    start = letter * l
    end = start + l
    return [x[start:end] for x in rows]


def addLetterToString(letter, string):
    for i in range(len(string)):
        string[i] += letter[i]
    return string


def solve(h, l, e, rows):
    result = ["" for _ in range(h)]
    for letter in e:
        ascii_letter = getLetter(h, l, rows, letter)
        result = addLetterToString(ascii_letter, result)
    for x in result:
        print(x)


# ********************************************************

# l = int(input())
# h = int(input())
# t = input()
# rows = []
# for i in range(h):
#     rows.append(input())


l, h, t = 4, 5, "M@NH@TT@N"
rows = [
    " #  ##   ## ##  ### ###  ## # # ###  ## # # #   # # ###  #  ##   #  ##   ## ### # # # # # # # # # # ### ### ",
    "# # # # #   # # #   #   #   # #  #    # # # #   ### # # # # # # # # # # #    #  # # # # # # # # # #   #   # ",
    "### ##  #   # # ##  ##  # # ###  #    # ##  #   ### # # # # ##  # # ##   #   #  # # # # ###  #   #   #   ## ",
    "# # # # #   # # #   #   # # # #  #  # # # # #   # # # # # # #    ## # #   #  #  # # # # ### # #  #  #       ",
    "# # ##   ## ##  ### #    ## # # ###  #  # # ### # # # #  #  #     # # # ##   #  ###  #  # # # #  #  ###  #  ",
]


solve(h, l, t, rows)
