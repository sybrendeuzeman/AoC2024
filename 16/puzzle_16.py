import numpy as np

with open('input.txt') as file:
    board = np.array([[a for a in line[0:-1]] for line in file])

# Part 1

# Make a board to play with using infinite values everywhere first
board_play = np.ones(shape = board.shape) * np.inf

# Replace the wall, starting point and endpoint with negative integers
board_play[np.where(board == '#')] = -1
board_play[np.where(board == 'S')] = -2
board_play[np.where(board == 'E')] = -3

start_position = np.argwhere(board == 'S')[0]

# Make a list of directions to loop through
drcs = np.array([
    [0,1],
    [1,0],
    [0,-1],
    [-1,0]
])

# Set a global points counter at infinity (all solutions are valid at first)
min_points = np.inf

def maze_solver(pos, drc,points, pos_visited, drcs = drcs):
    # Use a global minimum amount of points
    global min_points

    # Make list of movements to go through
    moves = [ 'fwd', 'tr', 'tl']


    # Set the position with the current number of points to check if arrived back at place
    board_play[pos[0], pos[1]] = points

    # Make a list for the points total
    l_points = []

    for move in moves:
        # Set different possible movement
        if move == 'tr':
            drc_new = (drc + 1) % 4 # Cycle through the list of 4 directions
            pos_new = np.array(pos + drcs[drc_new])
            extra_points = 1001
        if move == 'tl':
            drc_new = (drc - 1) % 4 # Cycle through the list of 4 directions
            pos_new = np.array(pos + drcs[drc_new])
            extra_points = 1001
        if move == 'fwd':
            pos_new = np.array(pos + drcs[drc])
            drc_new = drc
            extra_points = 1

        # Check if new position is a wall
        if board_play[pos_new[0], pos_new[1]]  == -1:
            continue

        # Check if end solution
        if board_play[pos_new[0], pos_new[1]] == -3:
            min_points = min(points + extra_points, min_points)
            l_points.append(points + extra_points)
            return l_points

        # Check if new position does not have less points than current
        if board_play[pos_new[0], pos_new[1]] < points:
            continue

        # Check if the current points total is not above the current minimum solution
        if points + extra_points > min_points:
            continue
        
        # Recurse and extend the list with new solutions
        l_points.extend(maze_solver(pos_new, drc_new, points + extra_points, pos_visited))
    return l_points      

solutions = maze_solver(start_position, 0, 0, [])
            
        
# Part 2
# Make a board to play with using infinite values everywhere first
board_play = np.ones(shape = board.shape) * np.inf

# Replace the wall, starting point and endpoint with negative integers
board_play[np.where(board == '#')] = -1
board_play[np.where(board == 'S')] = -2
board_play[np.where(board == 'E')] = -3

# Find starting position
start_position = np.argwhere(board == 'S')[0]

# Make a list of directions to loop through
drcs = np.array([
    [0,1],
    [1,0],
    [0,-1],
    [-1,0]
])

# Set a global points counter at infinity (all solutions are valid at first)
min_points = np.inf

def maze_solver(pos, drc,points, pos_visited, drcs = drcs):
    # Set different possible movement
    global min_points

    # Make list of movements to go through
    moves = ['fwd', 'tr', 'tl']
    
    # Make a list for the points total and visited locations
    l_visited = []
    l_points = []

    for move in moves:
        # Set different possible movement
        if move == 'tr':
            drc_new = (drc + 1) % 4
            pos_new = np.array(pos + drcs[drc_new])
            extra_points = 1001
        if move == 'tl':
            drc_new = (drc - 1) % 4
            pos_new = np.array(pos + drcs[drc_new])
            extra_points = 1001
        if move == 'fwd':
            pos_new = np.array(pos + drcs[drc])
            drc_new = drc
            extra_points = 1

        # Check if new position is a wall
        if board_play[pos_new[0], pos_new[1]]  == -1:
            continue
        
        # Check if end position
        if board_play[pos_new[0], pos_new[1]] == -3:
            l_points.append(points + extra_points)
            min_points = min(points + extra_points, min_points)
            l_visited.append(pos_visited + f'{pos_new[0]},{pos_new[1]}')
            return l_points, l_visited

        # Check if new position does not have less points than current
        if board_play[pos_new[0], pos_new[1]] < points + extra_points:
            continue

        # Check if the current points total is not above the current minimum solution
        if points + extra_points > min_points:
            continue
        
        # Set the position with the current number of points to check if arrived back at place
        board_play[pos[0], pos[1]] = points + extra_points

        # Recurse and extend the list with points and places visited
        l_points_n, l_visited_n = maze_solver(pos_new, drc_new, points + extra_points, pos_visited + f'{pos_new[0]},{pos_new[1]}; ')
        l_points.extend(l_points_n)
        l_visited.extend(l_visited_n)
        
    return l_points, l_visited

# Run the function
solutions, sol_visited = maze_solver(start_position, 0, 0, f'{start_position[0]},{start_position[1]}; ')

# Find the number of unique positions
positions = set()
for i_sol in np.where(np.array(solutions) == min(solutions))[0]:
    positions.update(
        [
            loc
            for loc
            in sol_visited[i_sol].split('; ')
        ]
    )        
total_spots = len(positions)
print(total_spots)