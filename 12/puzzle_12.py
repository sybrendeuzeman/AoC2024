import numpy as np

with open('input.txt') as file:
    board = np.array([[ord(a) for a in line[0:-1]] for line in file])

# Part 1

border_ud = np.diff(board, axis = 0, append = 0) != 0
border_du = np.flipud(np.diff(np.flipud(board), axis = 0, append = 0)) != 0
border_lr = np.diff(board, axis = 1, append = 0) != 0
border_rl = np.fliplr(np.diff(np.fliplr(board), axis = 1, append = 0))  != 0

borders = border_ud.astype(int) + border_du.astype(int) + border_lr.astype(int) + border_rl.astype(int)


x = 0
y = 0
region = 1

board_region = np.zeros(board.shape, dtype = int)

for y in range(board.shape[0]):
    letter = 0
    region += 1
    for x in range(0,board.shape[1]):
        region += (board[x,y] != letter)
        board_region[x,y] = region
        letter = board[x,y]
        if y > 0:
            if (board[x, y-1] == letter):
                board_region[np.where(board_region == board_region[x,y-1])] = region

total_cost = 0
for region in np.unique(board_region):
    positions = np.where(board_region == region)
    
    print('Region', region, 'Area:', len(positions[0]), 'Borders:', sum(borders[positions]))

    total_cost += sum(borders[positions]) * len(positions[0])
    print('Total cost: ', total_cost)

# Part 2

# Up down for fences to the left
board_fence_ud_left = np.zeros(board.shape, dtype = int)
for y in range(board.shape[0]):
    letter = 0
    not_yet_set = True
    for x in range(0,board.shape[1]):
        
        different = True

        if y > 0:
            different = board[x, y - 1] != board[x,y]


        if board[x,y] != letter:
            not_yet_set = True
        elif not different:
            not_yet_set = True
        

        if not_yet_set and different:
            board_fence_ud_left[x,y] = 1
            not_yet_set = False

        letter = board[x,y]

# Up down for fences to the right
board_fence_ud_right = np.zeros(board.shape, dtype = int)
for y in range(board.shape[0]):
    letter = 0
    not_yet_set = True
    for x in range(0,board.shape[1]):
        
        different = True

        if y < board.shape[1]-1:
            different = board[x, y + 1] != board[x,y]


        if board[x,y] != letter:
            not_yet_set = True

        elif not different:
            not_yet_set = True

        if not_yet_set and different:
            board_fence_ud_right[x,y] = 1
            not_yet_set = False

        letter = board[x,y]


# left right for fences up
board_fence_lr_up = np.zeros(board.shape, dtype = int)
for x in range(board.shape[0]):
    letter = 0
    not_yet_set = True
    for y in range(0,board.shape[1]):
        
        different = True

        if x > 0:
            different = board[x - 1, y] != board[x,y]


        if board[x,y] != letter:
            not_yet_set = True
        elif not different:
            not_yet_set = True

        if not_yet_set and different:
            board_fence_lr_up[x,y] = 1
            not_yet_set = False

        letter = board[x,y]

# left right for fences down
board_fence_lr_down= np.zeros(board.shape, dtype = int)
for x in range(board.shape[0]):
    letter = 0
    not_yet_set = True
    for y in range(0,board.shape[1]):
        
        different = True

        if x < board.shape[0] - 1 :
            different = board[x + 1, y] != board[x,y]


        if board[x,y] != letter:
            not_yet_set = True
        elif not different:
            not_yet_set = True

        if not_yet_set and different:
            board_fence_lr_down[x,y] = 1
            not_yet_set = False

        letter = board[x,y]

board_fences = board_fence_ud_left+board_fence_ud_right+board_fence_lr_up+board_fence_lr_down


total_cost = 0
for region in np.unique(board_region):
    positions = np.where(board_region == region)
    
    print('Region', region, 'Area:', len(positions[0]), 'Borders:', sum(board_fences[positions]))

    total_cost += sum(board_fences[positions]) * len(positions[0])
print('Total cost with discount: ', total_cost)
