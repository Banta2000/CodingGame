import matplotlib.pyplot as plt

# Points data
points = [(34, 5), (-36, 1), (4, 7), (-52, 5), (-61, 3), (44, 3), (27, 3), (59, 5)]

radius = 7

fig, ax = plt.subplots()

# Extract x and y coordinates
x_coords, y_coords = zip(*points)

# Plot the points
ax.scatter(x_coords, y_coords, color="blue", label="Points")

# Draw circles around each point
for x, y in points:
    circle = plt.Circle((x, y), radius, color="red", fill=False, linestyle="--")
    ax.add_patch(circle)

# Adjust plot limits to see all circles
all_x = [x - radius for x, _ in points] + [x + radius for x, _ in points]
all_y = [y - radius for _, y in points] + [y + radius for _, y in points]
ax.set_xlim(min(all_x) - 5, max(all_x) + 5)
ax.set_ylim(min(all_y) - 5, max(all_y) + 5)

ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Points with Circles (Radius=7)")
ax.grid(True)
ax.legend()

plt.savefig("points_plot.png")
print("Plot saved to points_plot.png")
