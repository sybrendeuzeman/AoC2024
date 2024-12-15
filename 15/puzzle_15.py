import numpy as np

with open('input.txt') as file:
    input = file.read()

# Part 1
board = np.array([[a for a in line] for line in input.split('\n\n')[0].split('\n')])

sequence = [a for a in input.split('\n\n')[1].replace('\n', '')]

dict_dirs = {
    '>' : np.array([0,1]),
    '<' : np.array([0,-1]),
    '^' : np.array([-1,0]),
    'v' : np.array([1,0])
}

position = np.argwhere(board == '@')[0]

for drc in sequence:
    direction = dict_dirs[drc]
    print(board)
    print('Direction:', drc)
    

    pos_check = position + direction
    count_boxes = 0
    
    while board[pos_check[0], pos_check[1]] == 'O':
        count_boxes += 1
        pos_check += direction

    if board[pos_check[0], pos_check[1]] == '.':
        while count_boxes > 0:
            board[pos_check[0], pos_check[1]] = 'O'
            pos_check -= direction
            count_boxes -= 1

        board[pos_check[0], pos_check[1]] = '@'
        board[position[0], position[1]] = '.'

        position += direction

sum_locations = np.sum(np.argwhere(board == 'O') * np.array([100,1]))


print('Sum of locations is:', sum_locations)

# Part 2

board_line = []
for line in input.split('\n\n')[0].split('\n'):
    row_line = ''
    for a in line:
        if a == '@':
            row_line += '@.'
        elif a == 'O':
            row_line += '[]'
        else:
            row_line += 2*a
    board_line.append(row_line)
board = np.array([[a for a in line] for line in board_line])

sequence = [a for a in input.split('\n\n')[1].replace('\n', '')]

dict_dirs = {
    '>' : np.array([0,1]),
    '<' : np.array([0,-1]),
    '^' : np.array([-1,0]),
    'v' : np.array([1,0])
}

position = np.argwhere(board == '@')[0]

for drc in sequence:
    direction = dict_dirs[drc]
    #[print(''.join(row)) for row in board]
    #print('Direction:', drc)

    # Modes for up-down and left-right need different methods of moving
    if drc in ['^', 'v']:

        # Set up the initial array to check:
        pos_check = np.array([position + direction])
        if board[pos_check[0][0], pos_check[0][1]] == '[':
            pos_check = np.vstack([pos_check, np.array([pos_check[0][0], pos_check[0][1] + 1])])
        elif board[pos_check[0][0], pos_check[0][1]] == ']':
            pos_check = np.vstack([pos_check, np.array([pos_check[0][0], pos_check[0][1] - 1])])
        list_chars = [board[pos[0], pos[1]] for pos in pos_check]

        list_path_blocks = []
        # Continue as long as there is a box and there is no wall
        while ('[' in list_chars or ']' in list_chars) and not ('#') in list_chars:
            # Add the last array to the list to keep track of the boxes
            list_path_blocks.append(pos_check)
            
            # Get a new check-array (fill a list and change to array later)
            new_pos_check = []

            # Check what is in the next positions from the initial positions
            # Only add if it is a box or a wall
            for pos in pos_check + direction:
                if board[pos[0], pos[1]] == '[':
                    new_pos_check.extend([[pos[0], pos[1]], [pos[0], pos[1] + 1]])
                elif board[pos[0], pos[1]] == ']':
                    new_pos_check.extend([[pos[0], pos[1]], [pos[0], pos[1] - 1]])
                elif board[pos[0], pos[1]] == '#':
                    new_pos_check.append([pos[0], pos[1]])
            # Make pos_check from list and only keep unique values
            pos_check = np.unique(np.array(new_pos_check), axis=0)
            
            # Make char list for check whether to continue
            list_chars = [board[pos[0], pos[1]] for pos in pos_check]

        # Only continue if there was no wall at last check
        if not ('#') in list_chars:
            # Move boxes if there is a box move list
            while len(list_path_blocks) > 0:
                # Start at the end and move forward
                blocks_to_move = list_path_blocks[len(list_path_blocks) - 1]
                
                # Move block for block
                for block in blocks_to_move:
                    pos_mov = block + direction
                    board[pos_mov[0], pos_mov[1]] = board[block[0], block[1]]
                    board[block[0], block[1]] = '.'
                
                # Delete last blocks to be moved
                del list_path_blocks[len(list_path_blocks) - 1]
            # Place the robot at new position
            pos_new = position + direction
            board[pos_new[0], pos_new[1]] = '@'
            board[position[0], position[1]] = '.'

            # Move position to the position of the new robot.
            position += direction

    if drc in ['>', '<']:
        # Set-up the check
        pos_check = position + direction
        count_boxes = 0     

        # Check how many boxes there are
        while board[pos_check[0], pos_check[1]] in ['[',']']:
            count_boxes += 2
            pos_check += 2*direction

        # Move boxes and robot only if there is no wall
        if board[pos_check[0], pos_check[1]] == '.':
            # Replace the char in front with the char behind
            while count_boxes > 0:
                prev_position = pos_check - direction
                board[pos_check[0], pos_check[1]] = board[prev_position[0], prev_position[1]]
                pos_check = prev_position
                count_boxes -= 1

            # Place the robot at the next position
            board[pos_check[0], pos_check[1]] = '@'
            board[position[0], position[1]] = '.'
            
            # Move the position for the next direction
            position += direction

#[print(''.join(row)) for row in board]

sum_locations = np.sum(np.argwhere(board == '[') * np.array([100,1]))
print('Sum of locations is:', sum_locations)