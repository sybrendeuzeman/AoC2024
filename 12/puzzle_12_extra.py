import numpy as np

with open('input.txt') as file:
    board = np.array([[ord(a) for a in line[0:-1]] for line in file])

# Part 1
# Find fences using the change in number in different directions
border_ud = np.diff(board, axis = 0, append = 0) != 0
border_du = np.flipud(np.diff(np.flipud(board), axis = 0, append = 0)) != 0
border_lr = np.diff(board, axis = 1, append = 0) != 0
border_rl = np.fliplr(np.diff(np.fliplr(board), axis = 1, append = 0))  != 0

borders = border_ud.astype(int) + border_du.astype(int) + border_lr.astype(int) + border_rl.astype(int)


# Find the regions on the board
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
            # Set whole region to the left equal to current region if the letter is equal
            if (board[x, y-1] == letter):
                board_region[np.where(board_region == board_region[x,y-1])] = region

total_cost = 0
for region in np.unique(board_region):
    positions = np.where(board_region == region)
    total_cost += sum(borders[positions]) * len(positions[0])
    print('Total cost: ', total_cost)

# Part 2

def get_borders(board):
    board_fences = np.zeros(board.shape, dtype = int)
    for x in range(board.shape[1]):
        letter = 0
        for y in range(0,board.shape[0]):

            # Check whether the element to the left is different from the current letter
            # In case x = 0 (border), set always different
            if x > 0:
                different = board[y, x - 1] != board[y,x]
            else:
                different = True

            # A fence needs to be places either after change of letter or if to the left there 
            # was an equal crop
            if board[y,x] != letter:
                not_yet_set = True
            elif not different:
                not_yet_set = True
            
            # Set a fence if both a fence was not yet set and the letter to the left is 0.
            if not_yet_set and different:
                board_fences[y,x] = 1
                not_yet_set = False

            letter = board[y,x]
    return board_fences

# Get fences is all directions by rotating the board
board_fence_ud_left = get_borders(board)
board_fence_ud_right = np.fliplr(get_borders(np.fliplr(board)))
board_fence_lr_up = np.rot90(get_borders(np.rot90(board)),axes=(1,0))
board_fence_lr_down = np.rot90(get_borders(np.rot90(board,axes=(1,0))))

# Add all fences together
board_fences = board_fence_ud_left + board_fence_ud_right + board_fence_lr_up + board_fence_lr_down


total_cost = 0
for region in np.unique(board_region):
    positions = np.where(board_region == region)
    total_cost += sum(board_fences[positions]) * len(positions[0])
print('Total cost with discount: ', total_cost)
