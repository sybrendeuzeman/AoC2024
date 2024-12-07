import numpy as np

# Input
input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

with open('input.txt') as f:
    input = f.read()

array_input = np.array(
    [[c for c in line] for line in input.rstrip('\n').split('\n')]
)

# Function to get array indices between two positions
def index_range(position, new_position):
    if (position[0] == new_position[0]):
        if position[1] < new_position[1]:
            return (new_position[0], range(position[1], new_position[1]+1))
        if position[1] > new_position[1]:
            return (new_position[0], range(position[1], new_position[1]-1, -1))
    if (position[1] == new_position[1]):
        if position[0] < new_position[0]:
            return (range(position[0], new_position[0]+1), new_position[1])
        if position[0] > new_position[0]:
            return (range(position[0], new_position[0]-1, -1), new_position[1])

# Part 1:
# Set some variables
dim = np.shape(array_input)
dirs = [
    np.array([-1,0]),
    np.array([0,1]),
    np.array([1,0]),
    np.array([0,-1]),
]

# Initialize problem
counter = 0
grid_solve = array_input.copy()

# Find starting position
position = np.array([np.where(grid_solve == '^')[0][0], np.where(grid_solve == '^')[1][0]])

while True:
    # Get the direction
    dir = dirs[counter]
    
    # Get the position of the end of the line to be checked
    position_end_line = np.minimum(
        np.maximum(
            dim*dir + position, 
            np.array([0,0])
        ), 
        np.array(dim) - 1
    )
    
    # Get the line in characters and find position of #
    line = ''.join(grid_solve[index_range(position, position_end_line)])
    block_after = line.find('#')

    # If no blockade, the problem is solved!
    if block_after == -1:
        grid_solve[index_range(position, position_end_line)] = 'X'
        break

    # Get the new position
    new_position = position + dir * (block_after-1)
    
    # Set X from the old position to the new position
    grid_solve[index_range(position, new_position)] = 'X'
    
    # Set new position as position
    position = new_position
    # Counter until 3, then start at 0
    counter = (counter + 1) % 4

print(f'Total number of distinct positions is: {np.sum(grid_solve == 'X')}')

# Part 2:
def check_loop_grid(position_blockade):
    # Make a copy of the grid
    grid_solve = array_input.copy()
    
    # Set the blockade at the position.
    # If already set or starting position, this position does not provide a blockade
    if grid_solve[position_blockade[0], position_blockade[1]] in ['#', '^']:            
        return 0
    else:
        grid_solve[position_blockade[0], position_blockade[1]] = '#'

    # Set empty grids to find if position was previously traveled from direction
    grid_walks = [
        np.empty(array_input.shape, dtype = str),
        np.empty(array_input.shape, dtype = str),
        np.empty(array_input.shape, dtype = str),
        np.empty(array_input.shape, dtype = str),
    ]

    # Get initial position
    position = np.array([np.where(grid_solve == '^')[0][0], np.where(grid_solve == '^')[1][0]])

    # Set counter to 0
    counter = 0
    while True:
        # Get direction
        dir = dirs[counter]
        
        # Get position to end of line
        position_end_line = np.minimum(
            np.maximum(
                dim* dir + position, 
                np.array([0,0])
            ), 
            np.array(dim) - 1
        )
        
        # Find in characters a blockade
        line = ''.join(grid_solve[index_range(position, position_end_line)])
        block_after = line.find('#')

        # If no blockade, the grid did not end in a loop
        if block_after == -1:
            return 0
        
        # Set new position
        new_position = position + dir * (block_after - 1)

        # Check if grid was previously walked from direction
        if grid_walks[counter][new_position[0], new_position[1]] == 'X':
            return 1
        # Set marker that guard had previously walked from direction
        grid_walks[counter][new_position[0], new_position[1]] = 'X'

        # Set new position as position
        position = new_position
        # Set counter
        counter = (counter + 1) % 4

potential_blockades = np.empty(array_input.shape, dtype = str)

for i_row in range(0,array_input.shape[0]):
    for i_column in range(0,array_input.shape[1]):
        if check_loop_grid([i_row, i_column]) == 1:
            potential_blockades[i_row, i_column] = 'X'

print(f'Total potential blockades is: {np.sum(potential_blockades == 'X')}')