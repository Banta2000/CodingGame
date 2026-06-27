import sys


def get_prefix(s: str, line_num: int) -> str:
    prefix = s[:line_num]
    repeating_char = s[line_num-1]
    return prefix, repeating_char

def build_line(s:str, line_num: int) -> str:
    prefix, repeating_char = get_prefix(s, line_num)
    midrow = repeating_char * WIDTH
    midrow += repeating_char * 2*(len(s) - len(prefix))
    midrow += repeating_char * 2
    midrow = prefix + midrow + prefix[::-1]
    return midrow


def build_empty_line(s:str) -> str:
    return s + "  " + WIDTH * " " + s[::-1]


def build_header(s:str) -> str:
    header = []
    for i in range(1, len(s)+1):
        header.append(build_line(s, i))
    header.append(build_empty_line(s))
    return header

def build_footer(s:str) -> str:
    return build_header(s)[::-1]


def build_body(s:str, image:list) -> str:
    body = []
    for line in image:
        r = s + " " + line + " " + s[::-1]
        body.append(r)
    return body


LOCAL = True

if LOCAL:
    WIDTH = 1
    IMAGE = ["#"]
    BORDER = "#"
else:
    BORDER = input()  # the ASCII art pattern to use to frame the picture
    h, WIDTH = [int(i) for i in input().split()]
    IMAGE = []
    for i in range(h):
        line = input()  # the ASCII art picture line by line
        IMAGE.append(line)
        print(line, file=sys.stderr, flush=True)
    print(BORDER, file=sys.stderr, flush=True)


header = build_header(BORDER)
footer = build_footer(BORDER)
body = build_body(BORDER, IMAGE)

r = header + body + footer
for line in r:
    print(line)
