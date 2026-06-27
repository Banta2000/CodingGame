import sys
import os
from typing import Any, Tuple

Game = dict[str, Any]
HOME_PC: bool = os.getenv("HOME_PC") == "true"
HOME_PC = True


# Modified printing
def myPrint(*args: Tuple[Any, ...], end: str = "\n") -> None:
    print(*args, file=sys.stderr, flush=True, end=end)


# Get Game Start Parameters
def get_start_parameters(print_input=False) -> Game:
    if HOME_PC:
        LU = {"A": 24, "B": 8, "C": 48}
        circuit = "[ ( A B ) [ C A ] ]"
        # circuit = "( Alef [ ( Bet Bet Bet ) ( Vet [ ( Vet Vet ) ( Vet [ Bet Bet ] ) ] ) ] )"
        # circuit = "[ ( [ Star ( Star Star ) ] [ Star ( Star Star ) ] Star ) ( [ Star ( Star Star ) ] [ Star ( Star Star ) ] Star ) ]"
    else:
        n = int(input())
        LU = {}
        for i in range(n):
            inputs = input().split()
            name = inputs[0]
            r = int(inputs[1])
            LU[name] = r
        circuit = input()
        
    if print_input:
        myPrint(LU, circuit)

    circuit = circuit.split(" ")
    for i in range(len(circuit)):
        if circuit[i] in LU:
            circuit[i] = LU[circuit[i]]
    return circuit


# Return the input parsed into its main subnodes
def parse_in_subnodes(lst: list) -> list:
    r = []
    i = 1
    while i < len(lst) - 1:
        if lst[i] not in ["[", "("]:
            r.append(lst[i])
        else:
            end = find_end_of_bracket(lst, i)
            t = lst[i : end + 1]
            r.append(t)
            i = end
        i += 1
    return r


def find_end_of_bracket(lst: list, start: int) -> int:
    count = 0
    for i in range(start, len(lst)):
        if lst[i] in ["[", "("]:
            count += 1
        elif lst[i] in ["]", ")"]:
            count -= 1
        if count == 0:
            return i
    return -1


def solve(circuit: list) -> int:
    if isinstance(circuit, int):
        return circuit
    mode = "parallel" if circuit[0] == "[" else "series"
    subnodes = parse_in_subnodes(circuit)
    subnodes = [solve(node) for node in subnodes]
    if mode == "series":
        return sum(subnodes)
    else:
        subnodes = [1/x for x in subnodes]
        return 1/sum(subnodes)

# ********************************************************

circuit = get_start_parameters(print_input=True)
r = solve(circuit)
r = round(r, 1)
print(f"{r:.1f}")
