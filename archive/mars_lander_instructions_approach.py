HOME_PC = 1
X_AXIS = [0, 7000]
Y_AXIS = [0, 3000]
LAND_POINTS = [(0, 100), (1000, 500), (1500, 1500), (3000, 1000), (4000, 150), (5500, 150), (6999, 800)]
LANDING_THRESHOLD = 30

import math
import sys
import matplotlib.pyplot as plt
import copy


def myPrint(lst):
    print("Debug messages...", lst, file=sys.stderr, flush=True)


def get_land_points():
    if HOME_PC:
        return LAND_POINTS
    else:
        surface_n = int(input())
        land_points = []
        for _ in range(surface_n):
            land_x, land_y = [int(j) for j in input().split()]
            land_points.append((land_x, land_y))
        return land_points


def extract_LZ(land_points):
    for i in range(len(land_points) - 1):
        if land_points[i][1] == land_points[i + 1][1]:
            LZ_X = [land_points[i][0], land_points[i + 1][0]]
            LZ_Y = land_points[i][1]
            LZ_CENTER_X = (LZ_X[0] + LZ_X[1]) // 2
            LZ = (LZ_CENTER_X, LZ_Y)
    return LZ, LZ_X


class Point:
    def __init__(self, x=0, y=0, x_vel=0, y_vel=0, fuel=1000, rotate=0, power=0):
        self.pos = (x, y)
        self.vel = (x_vel, y_vel)
        self.fuel = fuel
        self.rotate = rotate
        self.power = power
        self.LZ = LZ
        self.LZ_X = LZ_X
        self.steps = 0
        self.history = []

    def __str__(self):
        return f"Pos: {[round(x) for x in self.pos]}, Vel: {[round(x) for x in self.vel]}, Fuel: {round(self.fuel)}, Rotate: {round(self.rotate)}, Power: {round(self.power)}"

    def __repr__(self):
        return self.__str__()

    def apply_instruction_and_advance(self, instruction):
        self.history.append(self.pos)

        # 1. Apply instructions to tilt and power
        rotate, power = instruction
        self.rotate = rotate
        self.power = power

        # 2. Apply tilt, power and gravity to velocity and fuel
        self.vel = (
            self.vel[0] + self.power * -1 * math.sin(math.radians(self.rotate)),
            self.vel[1] + self.power * math.cos(math.radians(self.rotate)) - 3.711,
        )

        self.fuel -= self.power

        # 3. Apply velocity to position
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.steps += 1

    def is_flight_over(self):
        x, y = self.pos
        WITHIN_BOUNDS = X_AXIS[0] <= x <= X_AXIS[1] and Y_AXIS[0] <= y <= Y_AXIS[1]
        OUTSIDE_OF_BOUNDS = not WITHIN_BOUNDS
        BELOW_HORIZON = y < HORIZON[int(x)]
        return OUTSIDE_OF_BOUNDS or BELOW_HORIZON

    def is_within_LZ_x(self):
        return self.LZ_X[0] <= self.pos[0] <= self.LZ_X[1]

    def is_within_vel_x_and_y(self):
        return abs(self.vel[0]) < 20 and abs(self.vel[1]) < 40

    def where_crash_if_descend(self):
        point = copy.deepcopy(self)
        while True:
            point.apply_instruction_and_advance((0, 3))
            if point.is_flight_over():
                break
        return point

    def descend_lands_in_LZ(self):
        landing_point = self.where_crash_if_descend()
        return landing_point.is_within_LZ_x()

    def plot_history(self):
        x_coords = [p[0] for p in self.history]
        y_coords = [p[1] for p in self.history]
        plt.scatter(x_coords, y_coords, s=10)

        # Plot the horizon
        line_X = [point[0] for point in LAND_POINTS]
        line_Y = [point[1] for point in LAND_POINTS]
        plt.plot(line_X, line_Y)

        # Set the axis limits
        plt.xlim(*X_AXIS)
        plt.ylim(*Y_AXIS)

        # Show the plot
        plt.show()


def calculate_horizon(land_points):
    def get_horizon_line(p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        X = [x for x in range(x1, x2)]

        if y1 == y2:
            Y = [y1 for _ in range(x1, x2)]

        else:
            m = (y2 - y1) / (x2 - x1)
            Y = [m * (x - x1) + y1 for x in X]
        return Y

    Y = []
    for i in range(len(land_points) - 1):
        p_start = land_points[i]
        p_end = land_points[i + 1]
        Y += get_horizon_line(p_start, p_end)
    return Y


def plot_single_point(point, show_plot=True, color="blue"):
    plt.scatter(point.pos[0], point.pos[0], s=10, c=color)

    # Plot the horizon
    line_X = [point[0] for point in LAND_POINTS]
    line_Y = [point[1] for point in LAND_POINTS]
    plt.plot(line_X, line_Y)

    # Set the axis limits
    plt.xlim(*X_AXIS)
    plt.ylim(*Y_AXIS)

    # Show the plot
    if show_plot:
        plt.show()


def plot_points_list(points, show_plot=True, color="blue"):
    # Plot the points
    x_coords = [point.pos[0] for point in points]
    y_coords = [point.pos[1] for point in points]
    plt.scatter(x_coords, y_coords, s=10, c=color)

    # Plot the horizon
    line_X = [point[0] for point in LAND_POINTS]
    line_Y = [point[1] for point in LAND_POINTS]
    plt.plot(line_X, line_Y)

    # Set the axis limits
    plt.xlim(*X_AXIS)
    plt.ylim(*Y_AXIS)

    # Show the plot
    if show_plot:
        plt.show()


# ******************************************************************************

land_points = get_land_points()
LZ, LZ_X = extract_LZ(land_points)
HORIZON = calculate_horizon(land_points)

point = Point(x=2500, y=2700, x_vel=0, y_vel=0, fuel=5501, rotate=0, power=0)

while point.descend_lands_in_LZ() == False:
    point.apply_instruction_and_advance((-15, 4))

point.plot_history()

while point.is_flight_over() == False:
    point.apply_instruction_and_advance((0, 3))

point.plot_history()

# plot_points_list(points)

# trail, landing_point = start_point.where_crash_if_descend()

# plot_points_list(trail)


# HOOVER_UP = "0 4"
# HOOVER_DOWN = "0 3"

# FLY_LIGHT_RIGHT = "-15 4"
# FLY_STRONG_RIGHT = "-30 4"
# FLY_LIGHT_LEFT = "15 4"
# FLY_STRONG_LEFT = "30 4"


# while True:
#     x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]

#     LEFT_OF_LZ = x <= LZ[0]
#     RIGHT_OF_LZ = x >= LZ[0]

#     FLYING_LEFT = h_speed <= 0
#     FLYING_RIGHT = h_speed >= 0
#     FLYING_TO_LZ = (LEFT_OF_LZ and FLYING_RIGHT) or (RIGHT_OF_LZ and FLYING_LEFT)

#     DIST_TO_LZ_X = abs(LZ[0] - x)
#     DIST_TO_LZ_Y = abs(LZ[1] - y)

#     DESCENT_DIST = abs(abs(LZ[1] - y) * math.cos(15))
#     DESCENT_AREA = [LZ[0] - DESCENT_DIST, LZ[0] + DESCENT_DIST]

#     IN_DESCENT_AREA = DESCENT_AREA[0] <= x <= DESCENT_AREA[1]
#     OUT_DESCENT_AREA = not IN_DESCENT_AREA

#     IN_CORRIDOR = DIST_TO_LZ_X < 300

#     # DIST_TO_LZ = MID_LZ - x
#     # IN_LZ = LZ_X[0] <= x <= LZ_X[1]
#     # OUT_OF_LZ = not IN_LZ

#     SINKING_TOO_FAST = v_speed < -30

#     # CLOSE_TO_FLOOR = abs(y - LZ_Y) < 100
#     ABSOLUTE_H_SPEED = abs(h_speed)
#     H_SPEED_STRONG_TOO_HIGH = 40 < ABSOLUTE_H_SPEED
#     H_SPEED_LIGHT_TOO_HIGH = 20 < ABSOLUTE_H_SPEED < 40

#     # CORRECTION_SIGN = -1 if FLYING_TO_LZ else 1

#     # required_speed = DIST_TO_LZ // 40
#     # required_change_of_speed = required_speed - h_speed
#     # myPrint(
#     #     [
#     #         "Dist to LZ",
#     #         DIST_TO_LZ,
#     #         "My Speed",
#     #         h_speed,
#     #         "Required Speed",
#     #         required_speed,
#     #         "Required Change",
#     #         required_change_of_speed,
#     #     ]
#     # )

#     if H_SPEED_STRONG_TOO_HIGH:
#         myPrint("H_SPEED_STRONG_TOO_HIGH")
#         if FLYING_RIGHT:
#             print(FLY_STRONG_LEFT)
#         else:
#             print(FLY_STRONG_RIGHT)
#         continue

#     if H_SPEED_LIGHT_TOO_HIGH:
#         myPrint("H_SPEED_LIGHT_TOO_HIGH")
#         if FLYING_RIGHT:
#             print(FLY_LIGHT_LEFT)
#         else:
#             print(FLY_LIGHT_RIGHT)
#         continue

#     if SINKING_TOO_FAST:
#         myPrint("SINKING_TOO_FAST")
#         print(HOOVER_UP)
#         continue

#     if IN_CORRIDOR:
#         myPrint("In corridor")
#         print(HOOVER_UP)
#         continue

#     if IN_DESCENT_AREA:
#         myPrint("In descent area")
#         if LEFT_OF_LZ:
#             print("-0 3")
#         else:
#             print("0 3")
#         continue

#     if OUT_DESCENT_AREA:
#         myPrint("Approaching descent area")
#         if LEFT_OF_LZ:
#             print("-15 4")
#         else:
#             print("15 4")
#         continue


#     angle = map_value(abs(required_change_of_speed), 0, 20, 0, 90)
#     angle = angle if required_change_of_speed <= 0 else -angle

#     if OUT_OF_LZ:
#         myPrint("Outside of LZ")
#         print(str(angle) + " 4")
#         continue

#     if IN_LZ:
#         myPrint("In LZ")

#         if CLOSE_TO_FLOOR:
#             myPrint("Close to floor")
#             print("0 4")
#             continue

#         if not CLOSE_TO_FLOOR:
#             myPrint("Not close to floor")

#             if SINKING_TOO_FAST:
#                 myPrint("Sinking to fast")
#                 print(str(angle) + " 4")
#                 continue

#             if not SINKING_TOO_FAST:
#                 myPrint("Sinking at good speed")
#                 print(str(angle) + " 3")
#                 continue

#     if OUT_OF_LZ:
#         myPrint("Outside of LZ")

#         if ABSOLUTE_H_SPEED < 20:
#             myPrint("Not moving enough")
#             print("-90 4")
#             continue

#         if ABSOLUTE_H_SPEED >= 20:
#             myPrint("Moving")
#             angle = map_value(abs(h_speed), 20, 60, 0, 90) * CORRECTION_SIGN
#             print(str(-angle) + " 4")
#             continue

#     if IN_LZ:
#         myPrint("In LZ")

#         if CLOSE_TO_FLOOR:
#             myPrint("Close to floor, straightening")
#             print("0 4")
#             continue

#         if not CLOSE_TO_FLOOR:
#             myPrint("Not close to floor")

#             if ABSOLUTE_H_SPEED > 10:
#                 myPrint("Horizontal Speed to strong")

#                 angle = 90 * CORRECTION_SIGN
#                 print(str(angle) + " 4")
#                 continue

#             if ABSOLUTE_H_SPEED < 10:
#                 myPrint("Horizontal Speed Okay")
#                 print("0 4")
#                 continue

# if SINKING_TOO_FAST:
#     myPrint("Sinking too fast")
#     print("0 4")
#     continue

# if LEFT_OF_LZ:
#     myPrint("Left of LZ")
#     print("-20 3")
#     continue

# if RIGHT_OF_LZ:
#     myPrint("Right of LZ")
#     print("20 3")
#     continue
