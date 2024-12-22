import numpy as np

with open('input.txt') as file:
    input = [line for line in file.read().rstrip('\n').split('\n')]


##################
# Initialization #
##################

locs_numpad = {
    '0' : np.array([3, 1]),
    '1' : np.array([2, 0]),
    '2' : np.array([2, 1]),
    '3' : np.array([2, 2]),
    '4' : np.array([1, 0]),
    '5' : np.array([1, 1]),
    '6' : np.array([1, 2]),
    '7' : np.array([0, 0]),
    '8' : np.array([0, 1]),
    '9' : np.array([0, 2]),
    'A' : np.array([3, 2])
}

locs_keypad = {
    '^' : np.array([0, 1]),
    'A' : np.array([0, 2]),
    '<' : np.array([1, 0]),
    'v' : np.array([1, 1]),
    '>' : np.array([1, 2])

}

def path_h(start, end):
    # Find which part must be traveled
    travel = locs_keypad[end] - locs_keypad[start]

    # Set signs for horizontal en vertical paths
    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    # Make a vertical first and horizontal first path
    h_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    h_hor = mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    # Return the possible paths preventing going over the empty space
    if (locs_keypad[end][1] == 0) and (locs_keypad[start][0] == 0):
        return [h_vert]
    elif (locs_keypad[start][1] == 0) and (locs_keypad[end][0] == 0):
        return [h_hor]
    elif h_vert == h_hor:
        return [h_vert]
    else:
        return [h_hor, h_vert]
    
def initialization_movements(start, end):
    # Find distance between the two pads
    travel = locs_numpad[end] - locs_numpad[start]

    # Set the movement in vertical and horizontal direction
    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    # Make a vertical and horizontal path
    r2_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    r2_hor =  mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    # Return both the vertical and horizontal paths
    return r2_vert, r2_hor


def get_seq_list(seq):
    # Make a list with lists of paths for a certain sequence
    list_seq = []

    # Previous sequence ended at 'A' (by design)
    start = 'A'

    # Go over the sequence and find the robot movements to make movement
    for end in seq:
        list_seq.append(path_h(start, end))
        start = end

    return list_seq

###########################################################################################
### Make a dictionary with minimum cost for each movement at different number of robots ###
###########################################################################################

# Make list of 
inputs = locs_numpad.keys()

# Go over all combinations of letters and add possible sequences to list
l_starts = []
for i in inputs:
    for j in inputs:
        l_starts.extend(initialization_movements(i,j))
starts = set(l_starts)

# Put in list and find the sequence for robot to type the sequence
dict_translate = {}
for start in starts:
    dict_translate[start] = get_seq_list(start)
# Checked: all movements are already contained in this list;
# No more movements needed to be added

# Build the 0'th order database as initialization for higher order movements
dict_0_order = {}
for move in dict_translate.keys():
    dict_0_order[move] = len(move)
l_moves = [dict_0_order]

# Iterate 25 times calculate the minimum number of movements needed at each order from the lower order
for i in range(25):
    # Get the last dictionary in the list
    dict_latest = l_moves[-1]
    
    dict_new = {}
    for key, value in dict_translate.items():
        min_moves = 0
        for part in value:
            # At every choice decide what is the cheapest path
            min_moves += min([dict_latest[p] for p in part])
        # Add minimum number of moves to the dictionary for the key
        dict_new[key] = min_moves

    # Add the key to the list
    l_moves.append(dict_new)

########################
## Final Calculations ##
########################

def moves_between_numbers(start, end, order):
    # Calculate the cheapest path between two letters

    # Find what needs to be traveled
    travel = locs_numpad[end] - locs_numpad[start]

    # Find the vertical and horizontal movements
    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    # Make the vertical and horizontal path
    r2_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    r2_hor =  mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    # Find the number of moves from the dictionary
    moves_vert = l_moves[order][r2_vert]
    moves_hor = l_moves[order][r2_hor]

    # Return the appropiate value, while checking for crossing the empty space
    if (locs_numpad[start][1] == 0) and (locs_numpad[end][0] == 3):
        return moves_hor
    elif (locs_numpad[start][0] == 3) and (locs_numpad[end][1] == 0):
        return moves_vert
    else:
        if moves_hor < moves_vert:
            return moves_hor
        else:
            return moves_vert
        
def moves_sequence(seq, order):
    moves = 0
    start = 'A'
    # Go over the sequence and calculate the minimum number of moves necessary
    for end in seq:
        moves += moves_between_numbers(start, end, order)
        start = end
    return moves

# Calculate the 'complexities'
sol = 0
for line in input:
    r1 = moves_sequence(line, 2)
    print(line, ':', r1)
    sol += r1 * int(line[:3])

print('Order 2 (part 1):', sol)


sol = 0
for line in input:
    r1 = moves_sequence(line, 25)
    print(line, ':', r1)
    sol += r1 * int(line[:3])

print('Order 25 (part 2):', sol)
