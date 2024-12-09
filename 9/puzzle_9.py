import numpy as np

with open('input.txt') as file:
    input = file.read().rstrip('\n')

# Part 1:
# Build memory array, -1 is empty
mem = np.array([], dtype=int)
for i in range(len(input)):
    mem = np.append(mem, np.repeat((1- i % 2) * (i//2) + (i%2) * -1, int(input[i])))

# Find positions for filled memory and empty memory
mem_filled = np.where(mem > -1)[0][::-1]
mem_empty = np.where(mem == -1)[0]

# Check which values to place in empty spaces
length_array = min(len(mem_filled), len(mem_empty))
to_fill = mem_filled[0:length_array] > mem_empty[0:length_array]

# Set files in the empty space
mem[mem_empty[0:length_array][to_fill]] = mem[mem_filled[0:length_array][to_fill]]
# Set old file space free
mem[mem_filled[0:length_array][to_fill]] = -1

# Get positions of filled memory and calculate the checksum
final_filled = np.where(mem > -1)
checksum = np.sum(mem[final_filled] * final_filled)

print('Checksum:', checksum)

# Part 2:

# Make memory array
mem = np.array([], dtype=int)
for i in range(len(input)):
    mem = np.append(mem, np.repeat((1- i % 2) * (i//2) - (i%2) * (1), int(input[i])))

# Track programs checked
programs_checked = []

values_program = np.unique(mem[mem >= 0])

for i in range(len(values_program)-1, -1, -1):
    # Find an array with different values in memory
    value_memoryblocks = mem[
        np.where(
        np.diff(mem, prepend=-1)
        )[0]
    ]

    # Find an array with different lengths of blocks in memory
    length_memoryblocks = np.diff(
        np.where(
            np.diff(mem, prepend=-1)
        )[0],
        append = len(mem)
    )

    value_program = values_program[i]
    
    # Find the length and value of the program
    length_program = length_memoryblocks[value_memoryblocks == value_program][-1]

    # Find spot to place program
    cond = np.logical_and(value_memoryblocks == -1, length_memoryblocks >= length_program)
    # Make sure program is not placed after the current position
    cond = cond[:min(np.where(value_memoryblocks == value_program)[0])]

    # If memory location is found, write to location and clear location of program
    if any(cond):
        mem[np.where(mem == value_program)[0]] = -1
        
        pos_start = sum(length_memoryblocks[:np.where(cond)[0][0]])
        pos_end = pos_start + length_program
        mem[pos_start:pos_end] = value_program

# Get positions of filled memory and calculate the checksum
final_filled = np.where(mem >= 0)
checksum = np.sum((mem[final_filled]) * final_filled)

print('Checksum with other compression', checksum)
