import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation

# Define grid size
R, C = 45, 45


matrix = np.full((R, C), ' ')

# Seed the initial state
seeds = [
    (0, 2), (1, 0), (1, 2), (2, 1), (2, 2),
    (11, 2), (12, 0), (12, 2), (13, 1), (13, 2),
    (7, 5), (8, 5), (8, 7), (9, 5), (9, 6),
    (33, 2), (33, 3), (33, 4), (32, 4), (33, 3),
    (15, 14), (14, 14), (13, 14), (12, 14), (11, 14), (10, 14),
    (24, 2), (24, 3), (24, 4), (23, 4), (22, 3),
    (41, 2), (41, 3), (41, 4), (40, 4), (39, 3),
    (41, 20), (41, 21), (41, 22), (40, 22), (39, 21),
    (40, 0), (40, 1), (40, 4), (40, 5), (40, 6), (40, 7), (40, 8), (40, 9), (40, 12), (40, 13), (40, 14), (40, 16), (40, 17), (40, 18), (40, 19)
]

for x, y in seeds:
    matrix[x, y] = 'O'


def generate_next_generation(matrix):
    next_matrix = matrix.copy()
    for x in range(R):
        for y in range(C):
            count = count_neighbors(x, y, matrix)
            current = matrix[x, y]

            if current == 'X':
                if count['X'] < 2 or count['X'] > 3:
                    next_matrix[x, y] = ' '
            elif current == 'O':
                if count['X'] == 3:
                    next_matrix[x, y] = 'X'
    return next_matrix


def count_neighbors(x, y, matrix):
    xneighbors = 0
    yneighbors = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            x_coord, y_coord = (x + dx) % C, (y + dy) % R
            if matrix[x_coord, y_coord] == 'X':
                xneighbors += 1
            elif matrix[x_coord, y_coord] == 'O':
                yneighbors += 1
    return {'X': xneighbors, 'O': yneighbors}


initialize_matrix(R, C)


fig, ax = plt.subplots()


def update(frame):
    global matrix
    matrix = generate_next_generation(matrix)
    ax.cla()
    sns.heatmap((matrix == 'X').astype(int), cmap='Blues', cbar=False, ax=ax, square=True, annot=False, xticklabels=False, yticklabels=False)
Create the ani


ani = FuncAnimation(fig, update, frames=100, repeat=False)

plt.show()

ani.save('game_of_life.gif', writer='imagemagick', fps=5)
