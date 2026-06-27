import sys
import os
import math
from typing import Any, Tuple

GameState = dict[str, Any]

HOME_PC: bool = os.getenv("HOME_PC") == "true"


def myPrint(*args: Tuple[Any, ...]) -> None:
    print(*args, file=sys.stderr, flush=True)


class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"{int(self.x)} {int(self.y)}"

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def abs(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def left_turn(self):
        return Vector(-self.y, self.x)

    def right_turn(self):
        return Vector(self.y, -self.x)

    def scalar_mult(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # def __mul__(self, other: Vector) -> Vector:
    #     return Vector(self.x * other.x, self.y * other.y)

    # def __truediv__(self, other: Vector) -> Vector:
    #     return Vector(self.x / other.x, self.y / other.y)

    # def __ne__(self, other: Vector) -> bool:
    #     return self.x != other.x or self.y != other.y

    # def __lt__(self, other: Vector) -> bool:
    #     return self.x < other.x and self.y < other.y

    # def __le__(self, other: Vector) -> bool:
    #     return self.x <= other.x and self.y <= other.y

    # def __gt__(self, other: Vector) -> bool:
    #     return self.x > other.x and self.y > other.y

    # def __ge__(self, other: Vector) -> bool:
    #     return self.x >= other.x and self.y >= other.y

    # def __hash__(self) -> int:
    #     return hash((self.x, self.y))

    # def __abs__(self) -> Vector:
    #     return Vector(abs(self.x), abs(self.y))


def get_initial_GS() -> GameState:
    GS = {}
    if HOME_PC:
        GS["CAT_SPEED"] = 10
    else:
        GS["CAT_SPEED"] = int(input())
        myPrint(f"CAT_SPEED = {GS['CAT_SPEED']}")

    GS["MOUSE_SPEED"] = 10
    return GS


def update_GS(GS: GameState) -> None:
    if HOME_PC:
        if "mouse" not in GS:
            GS["mouse"] = Vector(15, 15)
        else:
            GS["mouse"] = GS["mouse"]
        if "cat" not in GS:
            GS["cat"] = Vector(5, 5)
        else:
            GS["cat"] = GS["cat"]
    else:
        mouse_x, mouse_y, cat_x, cat_y = [int(i) for i in input().split()]
        GS["mouse"] = Vector(mouse_x, mouse_y)
        GS["cat"] = Vector(cat_x, cat_y)
    return GS


# a and b are clock hands; return "right" if b is right of a, "left" otherwise
def approaching_side(a: Vector, b: Vector) -> float:
    angle = math.atan2(b.y, b.x) - math.atan2(a.y, a.x)
    if angle > math.pi:
        angle -= 2 * math.pi
    elif angle < -math.pi:
        angle += 2 * math.pi
    r = math.degrees(angle)
    if r < 0:
        return "Left"
    return "Right"


# ********************************************************

GS = get_initial_GS()

start_point_mouse = Vector(100, 0)
start_point_cat = Vector(500, 0)
center = Vector(0, 0)

phase = 0


SWITCH = True
v0 = Vector(-5, 0)
v1 = Vector(0, 5)
v2 = Vector(0, -5)


i = 0
while True:
    update_GS(GS)
    mouse: Vector = GS["mouse"]
    cat: Vector = GS["cat"]

    if phase == 0 and mouse == center:
        phase = 1

    if phase == 1 and mouse.abs() > 100:
        phase = 2

    myPrint("Phase:", phase)

    if phase == 0:
        next_target = center

    jump_vector = Vector(0, 0)
    if phase == 1:
        myPrint("Approaching Side", approaching_side(cat, mouse))
        if approaching_side(cat, mouse) == "Right":
            jump_vector = cat.right_turn()
        else:
            jump_vector = cat.left_turn()

        next_target = mouse + jump_vector - cat

    if phase == 2:
        next_target = mouse.scalar_mult(2)

    print(next_target)

    # x_vector = Vector(GS["mouse"].x, 0)
    # if SWITCH:
    #     next_target = x_vector + v0 + v1
    # else:
    #     next_target = x_vector + v0 + v2
    # SWITCH = not SWITCH
