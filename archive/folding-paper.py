# order = input()
# side = input()

order = "DRUL"
side = "D"

order = [x for x in order]
U = 1
D = 1
L = 1
R = 1

for fold in order:
    if fold == "U":
        Un = 1
        Ln = L * 2
        Rn = R * 2
        Dn = D + U
    elif fold == "D":
        Dn = 1
        Ln = L * 2
        Rn = R * 2
        Un = U + D
    elif fold == "L":
        Ln = 1
        Un = U * 2
        Dn = D * 2
        Rn = R + L
    elif fold == "R":
        Rn = 1
        Un = U * 2
        Dn = D * 2
        Ln = L + R
    U, D, L, R = Un, Dn, Ln, Rn

sol = {"U": U, "D": D, "L": L, "R": R}
print(sol[side])
