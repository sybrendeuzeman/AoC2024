import numpy as np

# Import data
with open('input.txt') as f:
    input = f.read()

input_array = np.asarray(
    [
        list(line)
        for line
        in input.rstrip('\n').split('\n')
    ]
)

# Define function to check a single position
def check_position(position, input_array):
    # Define list of letters to check
    letters = ['X', 'M', 'A', 'S']

    # Define directions
    directions = np.asarray(
        [
            (1, 0),
            (1, 1),
            (1,-1),
            (0, 1),
            (0, -1),
            (-1, 1),
            (-1, 0),
            (-1, -1)
        ]
    )

    # Check for all letters whether they exist in any direction
    for letter in letters:
        # Check array of positions first and remove out of bound positions
        check_bounds = np.logical_and(position < input_array.shape, position >= (0,0)).all(axis = 1)   
        position = position[check_bounds]

        # Resize to solve initialization problem
        directions = directions[list(np.resize(check_bounds, directions.shape[0]))]
        
        # If all positions are out of bound return 0
        if not np.any(check_bounds):
            return 0
        
        # Get an array with whether the position is the right letter
        check_array = np.apply_along_axis(get_letter, 1, position, input_array = input_array) == letter
        
        # If any letter is right, continue search
        if np.any(check_array):
            # Only keep positions and directions with right letter            
            position = position[check_array]
            directions = directions[list(np.resize(check_array, directions.shape[0]))]
            
            # Find new positions by adding the directions
            position = position + directions
        else:
        # Return 0 if no correct letter is found
            return 0
    # If all letters are found, return the number of times this happened    
    return sum(check_array)        



def get_letter(position_row, input_array):
    # Small function to find the letter in a position
    return input_array[position_row[0], position_row[1]]


# Run function on all indices of the input_array
n,m = input_array.shape
out = np.empty((n, m), dtype=int)
for i_row in range(n):
    for i_column in range(m):
        position = np.asarray([(i_row,i_column)])
        out[i_row, i_column] = check_position(position, input_array)

# Print the number of XMAS's in the puzzle
print(f'The number of times XMAS is found in the puzzle is: {np.sum(out)}')


# Problem 2: 
# Function to check at a position if it contains an X-MAS
def check_position_mas(position, input_array):
    # Start by checking whether the position is an A
    check_A =input_array[position[0], position[1]]== 'A'
    if not check_A:
        return 0

    # Define the two directions to be checked
    list_direction_lists = (
        (
            np.asarray((-1,-1)), 
            np.asarray((1,1))
            ),
        (
            np.asarray((1,-1)), 
            np.asarray((-1,1))
            )
    )

    # Go over all directions to be check in right order
    for direction_list in list_direction_lists:
        # Set list of letters that the directions have to contain
        list_check = ['M', 'S']

        # Go over the directions in the list
        for direction in direction_list:
            # Set position
            pos_diag = position + direction
            
            # Check whether position is within bounds
            if not np.logical_and(pos_diag < input_array.shape, pos_diag >= (0,0)).all():
                return 0
            
            # Get letter that is found
            letter = input_array[pos_diag[0], pos_diag[1]]
            
            # Check if letter is in list and otherwise return 0
            if letter not in list_check:
                return 0
            
            # Remove letter from list, prevent duplicates
            list_check.remove(letter)
    # Return 1 if all loops where successful.
    return 1

# Run function on all indices of the input_array
n,m = input_array.shape
out_mas = np.empty((n, m), dtype=int)
for i_row in range(n):
    for i_column in range(m):
        position = np.asarray((i_row,i_column))
        out_mas[i_row, i_column] = check_position_mas(position, input_array)

print(f'The number of times an X-MAS is found in the puzzle is: {np.sum(out_mas)}.')

