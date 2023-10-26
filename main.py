import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

# Define grid size (customize these values)
R, C = 40, 40

# Define cell states
CELL_STATES = [' ', 'X', 'O', '#']  # Empty, Alive (X), Dead (O), Special (#)

# Global variables
generation = 0
matrix = None
paused = False

# Function to create an empty grid
def create_empty_matrix(R, C):
    return np.full((R, C), ' ')

# Function to create a random grid
def create_random_matrix(R, C):
    return np.random.choice(CELL_STATES, size=(R, C), p=[0.5, 0.25, 0.2, 0.05])

# Function to initialize the grid
def initialize_matrix(R, C):
    global matrix, generation
    matrix = create_random_matrix(R, C)
    generation = 0

# Function to toggle cell state on click
def toggle_cell(event):
    if matrix is not None:
        x, y = int(event.xdata), int(event.ydata)
        current_state = matrix[y, x]
        next_state = CELL_STATES[(CELL_STATES.index(current_state) + 1) % len(CELL_STATES)]
        matrix[y, x] = next_state
        show_matrix()

# Function to perform one generation
def perform_generation():
    global matrix, generation
    if matrix is not None:
        next_matrix = matrix.copy()
        for y in range(R):
            for x in range(C):
                count = count_neighbors(x, y, matrix)
                current = matrix[y, x]
                if current == 'X':
                    if count['X'] < 2 or count['X'] > 3:
                        next_matrix[y, x] = 'O'
                elif current == 'O':
                    if count['X'] == 3:
                        next_matrix[y, x] = 'X'
        matrix = next_matrix
        generation += 1
        show_matrix()

# Function to count neighbors for a given cell
def count_neighbors(x, y, matrix):
    xneighbors = 0
    yneighbors = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            x_coord, y_coord = (x + dx) % C, (y + dy) % R
            if matrix[y_coord, x_coord] == 'X':
                xneighbors += 1
            elif matrix[y_coord, x_coord] == 'O':
                yneighbors += 1
    return {'X': xneighbors, 'O': yneighbors}

# Function to display the grid
def show_matrix():
    plt.cla()
    plt.imshow(np.zeros((R, C), dtype=int), cmap='gray', vmin=0, vmax=len(CELL_STATES))
    plt.imshow(np.array([[CELL_STATES.index(cell) for cell in row] for row in matrix]), cmap='tab20', vmin=0, vmax=len(CELL_STATES))
    plt.title(f'Generation: {generation}')
    plt.draw()

# Function to handle the play/pause button
def toggle_play_pause(event):
    global paused
    paused = not paused
    if not paused:
        play_pause.label.set_text('Pause')
        animate.event_source.start()
    else:
        play_pause.label.set_text('Play')
        animate.event_source.stop()

# Function to handle the step forward button
def step_forward(event):
    perform_generation()

# Function to handle the step backward button
def step_backward(event):
    global matrix, generation
    if generation > 0:
        matrix = create_empty_matrix(R, C)
        for _ in range(generation - 1):
            perform_generation()

# Create a figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Create space for buttons

# Create buttons
ax_button = plt.axes([0.15, 0.01, 0.1, 0.05])
play_pause = Button(ax_button, 'Play')
play_pause.on_clicked(toggle_play_pause)

ax_button = plt.axes([0.26, 0.01, 0.1, 0.05])
step_button = Button(ax_button, 'Step')
step_button.on_clicked(step_forward)

ax_button = plt.axes([0.37, 0.01, 0.1, 0.05])
step_back_button = Button(ax_button, 'Step Back')
step_back_button.on_clicked(step_backward)

ax_button = plt.axes([0.48, 0.01, 0.1, 0.05])
reset_button = Button(ax_button, 'Reset')
reset_button.on_clicked(lambda x: initialize_matrix(R, C))
ax_button = plt.axes([0.59, 0.01, 0.1, 0.05])
toggle_button = Button(ax_button, 'Toggle')
toggle_button.on_clicked(lambda x: initialize_matrix(R, C))
ax_button = plt.axes([0.7, 0.01, 0.1, 0.05])
save_button = Button(ax_button, 'Save')
save_button.on_clicked(lambda x: save_animation())

# Initialize the matrix
initialize_matrix(R, C)

# Initialize the animation
animate = FuncAnimation(fig, show_matrix, frames=None, repeat=False, interval=500)

plt.show()
