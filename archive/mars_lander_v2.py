# BEGINNE BEZEL KURVEN ZU VERSTEHEN
# CHANGE INSTRUCTIONS TO BE +1 0, -1 for tilt and for power


HOME_PC = 1
X_AXIS = [0, 7000]
Y_AXIS = [0, 3000]
LAND_POINTS = [(0, 100), (1000, 500), (1500, 1500), (3000, 1000), (4000, 150), (5500, 150), (6999, 800)]
LANDING_THRESHOLD = 30
DNA_SIZE = 100
POPULATION_SIZE = 200
BEST_PERCENTAGE = 0.05
MUTATION_RATE = 0.1


import sys
import math
import os
import heapq
import matplotlib.pyplot as plt
import copy
import random


os.system("cls" if os.name == "nt" else "clear")


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

    def __str__(self):
        score = Scorer.score(self)
        return f"Pos: {[round(x) for x in self.pos]}, Vel: {[round(x) for x in self.vel]}, Fuel: {round(self.fuel)}, Rotate: {round(self.rotate)}, Power: {round(self.power)}, Score: {score}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def __gt__(self, other):
        return self.get_value() > other.get_value()

    def __eq__(self, other):
        return self.get_value() == other.get_value()

    def apply_instruction_and_advance(self, instruction):
        # 1. Apply instructions to tilt and power
        rotate, power = instruction

        self.rotate += 15 * rotate
        self.rotate = max(min(self.rotate, 90), -90)

        self.power += power
        self.power = max(min(self.power, 4), 0)

        # 2. Apply tilt, power and gravity to velocity and fuel
        self.vel = (
            self.vel[0] + self.power * -1 * math.sin(math.radians(self.rotate)),
            self.vel[1] + self.power * math.cos(math.radians(self.rotate)) - 3.711,
        )

        self.fuel -= self.power

        # 3. Apply velocity to position
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.steps += 1

    def apply_instruction_and_advance2(self, instruction):
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

    def get_options(self):
        rotate_options = []
        if -75 <= self.rotate:
            rotate_options.append(-1)
        rotate_options.append(0)
        if self.rotate <= 75:
            rotate_options.append(1)

        power_options = []
        if 0 < self.power:
            power_options.append(-1)
        power_options.append(0)
        if self.power < 4:
            power_options.append(1)
        options = [(x, y) for x in rotate_options for y in power_options]
        return options

    # TODO Recheck points
    def get_value(self, debug=False):
        points = Scorer.score(self, debug=debug)

        # position_points = abs(self.pos[0] - self.LZ[0]) + abs(self.pos[1] - self.LZ[1])
        # if self.is_within_LZ_x():
        #     position_points /= 10

        # position_points = int(position_points)

        # velocity_points = 5 * (abs(self.vel[0]) + 10 * abs(self.vel[1]))
        # if self.is_within_speed():
        #     velocity_points /= 10

        # velocity_points = int(velocity_points)

        # full_points = position_points + velocity_points

        # if explain:
        #     print("Pos", f"{position_points:,.0f}", end="     ")
        #     print("Vel", f"{velocity_points:,.0f}", end="    ")
        #     print("InLZX", self.is_within_LZ_x(), end="     ")
        #     print("Speed", self.is_within_speed(), end="     ")
        #     print("Crash", self.is_crashed(), end="    ")
        #     print("Succ", self.is_success(), end="    ")
        #     print("Speed", self.vel, end="    ")
        #     print("Total", f"{full_points:,.0f}")
        return points

    # TODO Recheck
    def is_success(self):
        points = Scorer.score(self)
        return points == (100, 100, 100, 100)
        # X_CLOSE = self.LZ_X[0] <= self.pos[0] <= self.LZ_X[1]
        # Y_CLOSE = abs(self.pos[1] - self.LZ[1]) < LANDING_THRESHOLD
        # CLOSE_ENOUGH = X_CLOSE and Y_CLOSE
        # RIGHT_TILT = self.rotate == 0
        # SLOW_VERT = abs(self.vel[1]) <= 40
        # SLOW_HORZ = abs(self.vel[0]) <= 20
        # return CLOSE_ENOUGH and RIGHT_TILT and SLOW_VERT and SLOW_HORZ

    def is_flight_over(self):
        x, y = self.pos

        # Check for Outer Bounds
        WITHIN_BOUNDS = X_AXIS[0] <= x <= X_AXIS[1] and Y_AXIS[0] <= y <= Y_AXIS[1]
        OUTSIDE_OF_BOUNDS = not WITHIN_BOUNDS

        # Check for below horizon
        BELOW_HORIZON = y < HORIZON[int(x)]

        return OUTSIDE_OF_BOUNDS or BELOW_HORIZON

    def is_within_LZ_x(self):
        return self.LZ_X[0] <= self.pos[0] <= self.LZ_X[1]

    def is_within_vel_x_and_y(self):
        return abs(self.vel[0]) < 20 and abs(self.vel[1]) < 40

    def hash(self):
        res = (int(self.pos[0]), int(self.pos[1]), int(self.vel[0]), int(self.vel[1]), self.rotate, self.power)
        res = (int(self.pos[0]), int(self.pos[1]), int(self.vel[0]), int(self.vel[1]))
        return res


class DNA:
    def __init__(self, start_dna=None):
        if start_dna:
            self.dna = start_dna
        else:
            self.dna = []
            for _ in range(DNA_SIZE):
                angle = random.choice([-1, 0, 1])
                power = random.choice([-1, 0, 1])
                self.dna.append((angle, power))

    def get_endpoint(self, start_point, debug=False):
        _, endpoint = self.get_x_y_trail_and_endpoint(start_point, debug=debug)
        return endpoint

    def get_value(self, start_point, debug=False):
        endpoint = self.get_endpoint(start_point)
        value = endpoint.get_value(debug=debug)
        return value

    def get_x_y_trail_and_endpoint(self, start_point, debug=False):
        end_point = copy.copy(start_point)
        trail = []
        for instruction in self.dna:
            end_point.apply_instruction_and_advance(instruction)
            trail.append(end_point.pos)
            if debug:
                print(end_point)
            if end_point.is_flight_over():
                break
        return trail, end_point

    def get_mutation(self):
        result = []
        for i in range(DNA_SIZE):
            r = random.random()
            if r < MUTATION_RATE:
                angle = random.choice([-1, 0, 1])
                power = random.choice([-1, 0, 1])
                result.append((angle, power))
            else:
                result.append(self.dna[i])
        result_DNA = DNA()
        result_DNA.dna = result
        return result_DNA

    def plot(self, start_point):
        trail, _ = self.get_x_y_trail_and_endpoint(start_point)
        value = self.get_value(start_point, debug=True)
        print(f"Value: {value}")
        plot_single_trail_of_points(trail, show_plot=True)


class Population:
    def __init__(self, start_point):
        self.DNAs = [DNA() for _ in range(POPULATION_SIZE)]
        self.start_point = start_point

    def sort_by_value(self):
        self.DNAs.sort(key=lambda x: x.get_value(self.start_point))

    def trim_the_best(self):
        keep_how_many = int(POPULATION_SIZE * BEST_PERCENTAGE)
        self.DNAs = self.DNAs[-keep_how_many:]

    def mutate(self):
        result = []

        # Mutation by taking one candidate at a time and creating num_offsprings mutated offsprings from it
        # OFFSPRINGS = POPULATION_SIZE // len(self.DNAs)
        # for candidate in self.DNAs:
        #     for _ in range(OFFSPRINGS):
        #         result.append(candidate.get_mutation())

        # Mutation by two random candidates, mixing their dna, and mutating that result
        for _ in range(POPULATION_SIZE):
            c1 = random.choice(self.DNAs)
            c2 = random.choice(self.DNAs)
            temp_dna = []
            for i in range(DNA_SIZE):
                r = random.random()
                if r < 0.5:
                    temp_dna.append(c1.dna[i])
                else:
                    temp_dna.append(c2.dna[i])
            candidate = DNA(temp_dna)
            candidate = candidate.get_mutation()
            result.append(candidate)

        self.DNAs = result

    def plot(self):
        start_point = self.start_point
        list_of_DNAs = self.DNAs
        list_of_trails = [dna.get_x_y_trail_and_endpoint(start_point)[0] for dna in list_of_DNAs]
        list_of_fitness_values = [dna.get_value(start_point) for dna in list_of_DNAs]

        # # Normalize Fitness
        # min_fitness = min(list_of_fitness_values)
        # max_fitness = max(list_of_fitness_values)
        # list_of_fitness_values = [
        #     (fitness - min_fitness) / (max_fitness - min_fitness) for fitness in list_of_fitness_values
        # ]

        # # Generate a gradient of colors based on fitness
        # colors = [(fitness_value, 0, 0) for fitness_value in list_of_fitness_values]
        colors = ["blue" for _ in list_of_fitness_values]

        for trail, color in zip(list_of_trails, colors):
            plot_single_trail_of_points(trail, show_plot=False, color=color)
        plt.show()

    def get_best_DNA(self):
        return self.DNAs[0]

    def get_best_endpoint(self):
        return self.get_best_DNA().get_endpoint(self.start_point)


class Scorer:
    def __init__(self, start_point, LZ_X, LZ_Y, LZ):
        self.start_point = copy.copy(start_point)
        self.LZ_X = LZ_X
        self.LZ_Y = LZ_Y
        self.LZ = LZ
        self.max_dist = abs(LZ[0] - start_point.pos[0]) + abs(LZ[1] - start_point.pos[1])
        self.max_dist_only_x = abs(LZ[0] - start_point.pos[0]) + 100
        self.max_dist_only_y = abs(LZ[1] - start_point.pos[1]) + 100
        self.threshold_dist = abs(LZ_X[0] - LZ_X[1]) // 2
        self.max_vel_x = 50
        self.threshold_vel_x = 15
        self.max_vel_y = 120
        self.threshold_vel_y = 30
        self.max_score = 1000

    def map_to_target_range(self, value, input_min, input_max):
        # Handle the case where the input range is inverted
        inverted = input_max < input_min
        if inverted:
            input_min, input_max = input_max, input_min  # Swap to make the logic uniform

        # Clamp values outside the input range
        if value <= input_min:
            return 0 if not inverted else self.max_score
        elif value >= input_max:
            return self.max_score if not inverted else 0

        # Calculate the relative position of the value within the input range
        relative_position = (value - input_min) / (input_max - input_min)

        # Map the relative position to the target range (0 to self.max_score)
        mapped_value = relative_position * self.max_score

        # Adjust for inverted ranges
        r = mapped_value if not inverted else self.max_score - mapped_value
        return int(r)

    def score_x_distance(self, point, with_landing_zone=False):
        # The score is normalized from 0 to self.max_score

        # Use the manhattan distance to the landing zone
        # dist = abs(point.pos[0] - self.LZ[0]) + abs(point.pos[1] - self.LZ[1])
        # return self.max_dist - dist
        # res = self.map_to_target_range(dist, self.max_dist, 0)

        # Use only the X distance to the center of the landing zone
        dist = round(abs(point.pos[0] - self.LZ[0]))
        # dist = self.max_dist_only_x - dist
        # res = self.map_to_target_range(dist, self.max_dist_only_x, 0)

        # If we have the flag landing_zone, then we give self.max_score points to every point that is within the landing zone
        if with_landing_zone and self.LZ_X[0] <= point.pos[0] <= self.LZ_X[1]:
            dist = 0
        return dist

    def score_y_distance(self, point, with_landing_zone=False):
        dist = abs(point.pos[1] - self.LZ[1])
        # dist = self.max_dist_only_x - dist

        res = round(dist)

        if with_landing_zone and abs(point.pos[1] - self.LZ[1]) < LANDING_THRESHOLD:
            res = 0
        return res

    def score_y_velocity(self, point, with_threshold=False):
        # The score is normalized from 0 to self.max_score
        vel = round(abs(point.vel[1]))
        # res = self.map_to_target_range(vel_y, self.max_vel_y, 0)

        # If we have the flag, then we give self.max_score points to every point that is under the threshold
        # if with_threshold and vel_y <= self.threshold_vel_y:
        # res = self.max_score
        return vel

    def score_x_velocity(self, point, with_threshold=False):
        # The score is normalized from 0 to self.max_score
        vel_x = abs(point.vel[0])
        res = self.map_to_target_range(vel_x, self.max_vel_x, 0)

        # If we have the flag, then we give self.max_score points to every point that is under the threshold
        if with_threshold and vel_x <= self.threshold_vel_x:
            res = self.max_score
        return res

    def score_angle(self, point):
        # The score is normalized from 0 to self.max_score
        angle = abs(point.rotate)
        res = self.map_to_target_range(angle, 90, 0)
        return res

    def score(self, point, debug=False):
        invert = -1

        score_x_distance = self.score_x_distance(point, with_landing_zone=True)
        score_y_distance = self.score_y_distance(point, with_landing_zone=True)
        score_y_velocity = self.score_y_velocity(point, with_threshold=True)
        score_x_velocity = self.score_x_velocity(point, with_threshold=True)
        # score_angle = self.score_angle(point)
        result = (
            score_x_distance,
            point.steps,
            score_y_distance,
            score_y_velocity,
            # invert * score_x_velocity,
        )
        return result


def myPrint(lst):
    print("Debug messages...", lst, file=sys.stderr, flush=True)


def extract_LZ(land_points):
    for i in range(len(land_points) - 1):
        if land_points[i][1] == land_points[i + 1][1]:
            LZ_X = [land_points[i][0], land_points[i + 1][0]]
            LZ_Y = land_points[i][1]
            LZ_CENTER_X = (LZ_X[0] + LZ_X[1]) // 2
            LZ = (LZ_CENTER_X, LZ_Y)
    return LZ_X, LZ_Y, LZ


def map_value(value, from_min, from_max, to_min, to_max):
    if value < from_min:
        return int(to_min)
    if value > from_max:
        return int(to_max)
    return int(to_min + (value - from_min) * (to_max - to_min) / (from_max - from_min))


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


def plot_single_trail_of_points(points, show_plot=True, color="blue"):
    # Plot the points
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
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


def calculate_priority(p, LZ):
    return abs(p.pos[0] - LZ[0]) + abs(p.pos[1] - LZ[1]) + abs(p.vel[0]) + abs(p.vel[1])


def a_star_pathfinding(p):
    stack, history = [], []
    visited = set()
    heapq.heappush(stack, (p, history))

    counter = 1

    while stack:
        current_point, current_history = heapq.heappop(stack)

        # Plot the selected point
        # plot_single_trail_of_points([current_point.pos], show_plot=False, color="red")
        # plt.pause(0.001)
        # plt.draw()
        # print(current_point)

        if current_point.hash() in visited:
            continue
        visited.add(current_point.hash())

        if current_point.is_success():
            print("SUCCESS")
            return current_history

        options = current_point.get_options()
        for option in options:
            new_point = copy.copy(current_point)
            new_point.apply_instruction_and_advance(option)

            if new_point.hash() in [x.hash() for x, _ in stack] or new_point.is_flight_over():
                continue

            new_history = current_history.copy() + [option]

            if new_point.pos[0] >= 4000:
                True

            heapq.heappush(stack, (new_point, new_history))

        counter += 1
        if counter > 150:
            break

    print(len(visited))

    return heapq.heappop(stack)


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


# INIT ********************************************************

land_points = get_land_points()
LZ_X, LZ_Y, LZ = extract_LZ(land_points)
HORIZON = calculate_horizon(land_points)
start_point = Point(x=2500, y=2700, x_vel=0, y_vel=0, fuel=5501, rotate=0, power=0)
Scorer = Scorer(start_point, LZ_X, LZ_Y, LZ)

# INIT END ********************************************************


# population = Population(start_point)

# # # while True:
# for _ in range(100):
#     population.sort_by_value()
#     population.trim_the_best()
#     population.sort_by_value()
#     population.plot()
#     population.mutate()
#     population.plot()


# population.sort_by_value()
# population.trim_the_best()

# endPoints = [dna.get_endpoint(start_point) for dna in population.DNAs]
# for endPoint in endPoints:
#     print(endPoint)
# population.plot()


#     # b = population.get_best_landing_point().get_value(explain=True)
#     if population.get_best_landing_point().is_success():
#         break

# population.plot()
# best_DNA = population.get_best_DNA()

# test_point = copy.copy(start_point)
# test_point.apply_DNA(best_DNA.dna, document=True)


# for x in best_DNA.dna:
#     print(x, ",")


# trail_history = best_DNA.get_trail(start_point)
# plot_single_trail_of_points(trail_history)


# PATHFINDING START *****************************************

# bestpoint, bestdna = a_star_pathfinding(start_point)
# bestdna = DNA(bestdna)
# bestdna.plot(start_point)

# PATHFINDING END *******************************************


def dist_after_t(v0, t, a):
    res = t * (v0 + 0.5 * (t + 1) * a)
    return res


def t_to_travers_s(v0, a, d):
    res = (-v0 + math.sqrt(v0**2 + 2 * a * d)) / a
    return res


def v_after_t(v0, t, a):
    res = v0 + t * a
    return res


def angle_needed_to_land(start_point, LZ):
    x, y = start_point.pos
    x_LZ, y_LZ = LZ
    dx = abs(x_LZ - x)
    dy = abs(y_LZ - y)
    angle = abs(math.degrees(math.atan2(dy, dx)) - 90)
    if x_LZ < x:
        angle = -angle
    return angle


CLOSE_ENOUGH_DIST = abs(LZ[1] - start_point.pos[0]) * math.cos(15)
print(CLOSE_ENOUGH_DIST)
CLOSE_ENOUGH_X = [LZ[0] - CLOSE_ENOUGH_DIST, LZ[0] + CLOSE_ENOUGH_DIST]
print(CLOSE_ENOUGH_X)


counter = 0
while (CLOSE_ENOUGH_X[0] < start_point.pos[0] < CLOSE_ENOUGH_X[1]) == False:
    start_point.apply_instruction_and_advance2((-15, 4))
    plot_single_trail_of_points([start_point.pos], show_plot=False, color="red")
    plt.pause(0.001)
    plt.draw()
    print(start_point)
    counter += 1
    if counter > 50:
        break
    # print(start_point)


# for _ in range(1000):
#     x, y = start_point.pos
#     start_point.pos = (x+10, y)
#     print([int(x) for x in start_point.pos], angle_needed_to_land(start_point, LZ))
