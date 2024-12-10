import numpy as np

with open('input.txt') as file:
    board = np.array([[int(a) for a in line[0:-1]] for line in file])

starting_positions = np.array(np.where(board == 0)).transpose()

dirs = np.array(
    [
        (0,1),
        (0,-1),
        (1,0),
        (-1,0)
    ])

dims = np.array(board.shape)
count = 0

# Part 1:
for starting_position in starting_positions:
    positions = np.array([starting_position])
    for i in range(1, 10):        
        positions = np.concatenate([
            position + dirs
            for position
            in positions
        ],axis=0)


        positions = positions[np.logical_and(positions < dims, positions >= 0).all(axis = 1)]
        positions = positions[
            np.array(
                [
                    board[position[0], position[1]]
                    for position
                    in positions
                ]
            ) == i]
        
    count += len(np.unique(positions, axis = 0))
print('Sum of scores:', count)

# Part 2:
count = 0
for starting_position in starting_positions:
    positions = np.array([starting_position])
    for i in range(1, 10):        
        positions = np.concatenate([
            position + dirs
            for position
            in positions
        ],axis=0)


        positions = positions[np.logical_and(positions < dims, positions >= 0).all(axis = 1)]
        positions = positions[
            np.array(
                [
                    board[position[0], position[1]]
                    for position
                    in positions
                ]
            ) == i]
        
    count += len(positions)
print('Sum of ratings:', count)