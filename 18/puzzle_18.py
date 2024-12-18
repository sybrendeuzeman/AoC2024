import numpy as np

with open('input.txt') as file:
    input = np.array([[int(a) for a in line[:-1].split(',')]for line in file])


board = np.empty([71,71], dtype = str) 
board[:] = '.'

# Part 1
for a in input[:2981]:
    board[a[1], a[0]] = '#'

pos = np.array([[0,0]])

dirs = np.array([
    [0,1],
    [0,-1],
    [1,0],
    [-1,0]
    ])

i = 0

while True:
    i += 1
    
    new_pos = np.vstack([p + dirs for p in pos])
    new_pos = np.unique(new_pos, axis = 0)
    
    new_pos = new_pos[np.all(new_pos < board.shape, axis = 1)]
    new_pos = new_pos[np.all(new_pos >= 0, axis = 1)]
    new_pos = new_pos[[board[pos[0], pos[1]] == '.' for pos in new_pos]]

    for p in new_pos:
        board[p[0], p[1]] = 'X'
    
    if np.any(np.all(new_pos == 70, axis = 1), axis = 0):
        break
    pos = new_pos
    
print(i)

# Part 2

def check_board(number_blocks, board_shape):
    board = np.empty([board_shape + 1,board_shape + 1], dtype = str) 
    board[:] = '.'


    for a in input[:number_blocks]:
        board[a[1], a[0]] = '#'

    pos = np.array([[0,0]])

    dirs = np.array([
        [0,1],
        [0,-1],
        [1,0],
        [-1,0]
        ])

    i = 0

    while True:
        i += 1
        new_pos = np.vstack([p + dirs for p in pos])
          
        new_pos = np.unique(new_pos, axis = 0)
        
        new_pos = new_pos[np.all(new_pos < board.shape, axis = 1)]
        new_pos = new_pos[np.all(new_pos >= 0, axis = 1)]
        new_pos = new_pos[[board[pos[0], pos[1]] == '.' for pos in new_pos]]

        for p in new_pos:
            board[p[0], p[1]] = 'X'
        
        if np.any(np.all(new_pos == board_shape, axis = 1), axis = 0):
            return False

        if len(new_pos)== 0:
            return True
        pos = new_pos



# Binary search for switch position
max_pos = len(input)
min_pos = 1

while min_pos < max_pos:
    mid_point = (min_pos + max_pos) // 2

    
    blocked = check_board(mid_point, board_shape=70)
    
    if blocked:
        max_pos = mid_point
    else:
        min_pos = mid_point + 1


print(f'{input[mid_point][0]},{input[mid_point][1]}')