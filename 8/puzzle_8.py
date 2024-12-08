
import numpy as np
with open('input.txt') as file:
    board = np.array([[a for a in line[0:-1]] for line in file])

characters = np.unique(board).tolist()
characters.remove('.')

# Part 1:

set_positions = set()
for character in characters:
    sites = np.array(np.where(board == character)).transpose()

    for i in range(0,sites.shape[0]):
        sites_c = np.delete(sites, i, axis=0)
        positions = (sites_c - sites[i]) + sites_c
        set_positions.update(
            [
                f'{position[0]},{position[1]}'
                for position 
                in positions
                if np.all(position >= np.array([0,0])) and np.all(position < board.shape)
            ]
        )

count = len(set_positions)

print(count)

# Part 2:
max_iter = np.max(board.shape)


set_positions = set()
for character in characters:
    sites = np.array(np.where(board == character)).transpose()

    for i in range(0,sites.shape[0]):
        sites_c = np.delete(sites, i, axis=0)
        for mul in range(0, max_iter):
            positions = mul * (sites_c - sites[i]) + sites_c
            set_positions.update(
                [
                    f'{position[0]},{position[1]}'
                    for position 
                    in positions
                    if np.all(position >= np.array([0,0])) and np.all(position < board.shape)
                ]
            )

count = len(set_positions)

print(count)