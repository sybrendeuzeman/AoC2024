import numpy as np
from collections import Counter

# Get input into an array
with open('input.txt') as file:
    board = np.array([[a for a in line[0:-1]] for line in file])

# Get board to keep track of path
board_steps = np.ones(board.shape, int) * - np.inf

# Get start position
pos_nt = np.argwhere(board == 'S')

# Get directions possible from every step
dirs = np.array([
    [0,1],
    [0,-1],
    [1,0],
    [-1,0]
    ])

# Initialize counter
i = 0

# Set length from starting point to 0
board_steps[pos_nt[0][0], pos_nt[0][1]] = 0


while True:
    i += 1
    
    # Set positions from start (maze solve)
    new_pos_nt = np.vstack([p + dirs for p in pos_nt])
    new_pos_nt = np.unique(new_pos_nt, axis = 0)
    new_pos_nt = new_pos_nt[np.all(new_pos_nt < board.shape, axis = 1)]
    new_pos_nt = new_pos_nt[np.all(new_pos_nt >= 0, axis = 1)]

    # Set positions to prevent going back
    pos_nt = new_pos_nt[[board[p[0], p[1]] == '.' for p in new_pos_nt]]
    for p in pos_nt:
        board[p[0], p[1]] = 'X'
        board_steps[p[0], p[1]] = i

    # Search for endpoint
    if np.any([board[p[0], p[1]] == 'E' for p in new_pos_nt]) > 0:
        # Set length to E as a final step.
        board_steps[np.where(board == 'E')] = i
        break

# Part 1
def find_shortcuts_ud(board_steps):
    # Find the shortcuts and how effective the shortcut is for shortcuts up-down

    # Find difference with two rows down
    board_shortcuts = board_steps[2:] - board_steps[:-2] - 2

    # Set irrelevant outputs to 0
    board_shortcuts[np.where(board_shortcuts  == np.inf)] = 0
    board_shortcuts[np.where(board_shortcuts  < 0)] = 0
    board_shortcuts[np.isnan(board_shortcuts)] = 0

    # Count the different shortcut lengths
    unique, counts = np.unique(board_shortcuts, return_counts=True)
    
    return dict(zip(unique, counts))

# Flip board few ways to find shortcuts in all directions
dicts_shortcuts = [
    find_shortcuts_ud(board_steps),
    find_shortcuts_ud(np.flipud(board_steps)),
    find_shortcuts_ud(np.rot90(board_steps, axes = (1,0))),
    find_shortcuts_ud(np.rot90(board_steps))
]


# Count the number of cheats over 100
counts = sum(map(Counter, dicts_shortcuts), Counter())
tot_cheats = 0
for l_cheat, n_cheat in counts.items():
    if l_cheat >= 100:

        tot_cheats += n_cheat

print(tot_cheats)

# Part 2

# Make a list of the visited positions in order
list_positions = []
for i in range(0, int(np.max(board_steps)) + 1):
    list_positions.append(np.argwhere(board_steps == float(i))[0])

# Use dict to keep track how many cheats of each length are possible
counter = {}

# Go over list to find the cheats
for i in range(0,len(list_positions)):
    # Only positions at least 100 steps away are potentially relevant
    for j in range(i+100, len(list_positions)):
        # Get distance between two points
        dist = abs(list_positions[i][0] - list_positions[j][0]) + abs(list_positions[i][1] - list_positions[j][1]) 
        # Find how much the shortcut would cheat away
        cheated = j - i - dist
        # Only keep the cheat if the distance is lower or equal to 20 en more than 100 picoseconds are cheated.
        if (dist <= 20) and (cheated >= 100):
            counter[cheated] = counter.get(cheated, 0) + 1

print(sum(counter.values()))