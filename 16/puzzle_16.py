import numpy as np

with open('input_.txt') as file:
    board = np.array([[a for a in line[0:-1]] for line in file])

# Part 1

board_play = np.ones(shape = board.shape) * np.inf

board_play[np.where(board == '#')] = -1
board_play[np.where(board == 'S')] = -2
board_play[np.where(board == 'E')] = -3

start_position = np.argwhere(board == 'S')[0]

drcs = np.array([
    [0,1],
    [1,0],
    [0,-1],
    [-1,0]
])
min_points = np.inf

def maze_solver(pos, drc,points, pos_visited, drcs = drcs):
    global min_points

    moves = [ 'fwd', 'tr', 'tl']

    board_play[pos[0], pos[1]] = points

    l_points = []

    for move in moves:
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

        if board_play[pos_new[0], pos_new[1]]  == -1:
            continue

        if board_play[pos_new[0], pos_new[1]] == -3:
            l_points.append(points + extra_points)
            return l_points

        if board_play[pos_new[0], pos_new[1]] < points:
            continue

        if points + extra_points > min_points:
            continue

        l_points.extend(maze_solver(pos_new, drc_new, points + extra_points, pos_visited))
        #print(board_play)
    return l_points      

solutions = maze_solver(start_position, 2, 0, [])
            
        
# Part 2

board_play = np.ones(shape = board.shape) * np.inf

board_play[np.where(board == '#')] = -1
board_play[np.where(board == 'S')] = -2
board_play[np.where(board == 'E')] = -3

start_position = np.argwhere(board == 'S')[0]

drcs = np.array([
    [0,1],
    [1,0],
    [0,-1],
    [-1,0]
])

min_points = np.inf

def maze_solver(pos, drc,points, pos_visited, drcs = drcs):
    global min_points
    moves = ['fwd', 'tr', 'tl']
    
    l_visited = []
    l_points = []

    for move in moves:
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

        if board_play[pos_new[0], pos_new[1]]  == -1:
            continue

        if board_play[pos_new[0], pos_new[1]] == -3:
            l_points.append(points + extra_points)
            min_points = min(points + extra_points, min_points)
            l_visited.append(pos_visited + f'{pos_new[0]},{pos_new[1]}')
            return l_points, l_visited

        if board_play[pos_new[0], pos_new[1]] < points + extra_points:
            continue

        if points + extra_points > min_points:
            continue
        
        board_play[pos[0], pos[1]] = points + extra_points

        l_points_n, l_visited_n = maze_solver(pos_new, drc_new, points + extra_points, pos_visited + f'{pos_new[0]},{pos_new[1]}; ')
        l_points.extend(l_points_n)
        l_visited.extend(l_visited_n)
        
        #print(board_play)
    return l_points, l_visited

solutions, sol_visited = maze_solver(start_position, 0, 0, f'{start_position[0]},{start_position[1]}; ')

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