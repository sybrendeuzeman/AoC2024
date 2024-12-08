import numpy as np

# Open board
with open('input.txt') as file:
    board = np.array([[a for a in line[0:-1]] for line in file])

# Get characters to check without '.'
characters = np.unique(board).tolist()
characters.remove('.')

# Part 1:
# Use set to keep positions with antinode
set_positions = set()

# Find antinode positions per character
for character in characters:
    # Find the places on the board with the character
    sites = np.array(np.where(board == character)).transpose()

    # Find position of antinodes originating from site i
    for i in range(0,sites.shape[0]):
        # Find antenna positions without position i
        sites_c = np.delete(sites, i, axis=0)
        
        # Find antinode positions
        positions = (sites_c - sites[i]) + sites_c
        
        # Update set with positions within bounds
        # String to make position hashable
        set_positions.update(
            [
                f'{position[0]},{position[1]}'
                for position 
                in positions
                if np.all(position >= np.array([0,0])) and np.all(position < board.shape)
            ]
        )

# Find length of set positions as solution
count = len(set_positions)
print('The number of antinode positions is:', count)

# Part 2:
# Find the max number of iterations, i.e. max dimension of the board
max_iter = np.max(board.shape)

# Use set to keep positions with antinode
set_positions = set()

# Find antinode positions per character
for character in characters:
    # Find the positions on the board with the character
    sites = np.array(np.where(board == character)).transpose()

    # Find position of antinodes originating from site i
    for i in range(0,sites.shape[0]):
        # Loop 1 until max iter to be sure all antinode positions are found
        for mul in range(1, max_iter):
            # Multiply step to find antinode position
            positions = mul * (sites - sites[i]) + sites
            
            # Add to set after checking whether position is within bounds
            set_positions.update(
                [
                    f'{position[0]},{position[1]}'
                    for position 
                    in positions
                    if np.all(position >= np.array([0,0])) and np.all(position < board.shape)
                ]
            )

# Count number of antinode positions
count = len(set_positions)
print('The number of antinode positions with resonance is:', count)