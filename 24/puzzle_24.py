import re


with open('input.txt') as file:
    input = [block for block in file.read().rstrip('\n').split('\n\n')]

# Define functions for dictionary
def funcAND(inp1, inp2):
    return inp1 and inp2

def funcOR(inp1, inp2):
    return inp1 or inp2

def funcXOR(inp1, inp2):
    return inp1 ^ inp2

# Make dictionary to translate function calls
transFunc = {
    'AND' : funcAND,
    'OR' : funcOR,
    'XOR' : funcXOR
}

# Part 1

mem = dict([(line.split(': ')[0], int(line.split(': ')[1])) for line in input[0].split('\n')])
pattern_inst = r'([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)'
insts = [re.match(pattern_inst, line).groups() for line in input[1].split('\n')]


while len(insts) > 0:
    delete = []
    for i, inst in enumerate(insts):
        # Check existence of inputs
        if not((inst[0] in mem) and (inst[2] in mem)):
            continue
                
        mem[inst[3]] = transFunc[inst[1]](mem[inst[0]], mem[inst[2]])
        delete.append(i)

    for j in sorted(delete, reverse=True):
        del insts[j]

sol = 0
for mem_pos in mem:
    if mem_pos.startswith('z'):
        sol += pow(2, int(mem_pos[1:])) * mem[mem_pos]

print('Solution is:', sol)

# Part 2

def find_circuit(inp1, inp2, inst):
    name1 = mem_trans[inp1]
    name2 = mem_trans[inp2]


    in_inst = [
        ins[3]
        for ins    
        in insts
        if (ins[0] == name1 and ins[1] == inst and ins[2] == name2) or (ins[2] == name1 and ins[1] == inst and ins[0] == name2)
    ]

    return in_inst


mem = dict([[line.split(': ')[0], int(line.split(': ')[1])] for line in input[0].split('\n')])
pattern_inst = r'([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z0-9]+)'
insts = [list(re.match(pattern_inst, line).groups()) for line in input[1].split('\n')]

mem_state = {}


# Making a de-obfuscation dictionary;
# Checking correctness and correcting where necessary

registers_swapped = set()

# Initialization with the inputs and 00
mem_trans = dict([(line.split(': ')[0], line.split(': ')[0]) for line in input[0].split('\n')])
mem_trans['z00'] = find_circuit('x00', 'y00', 'XOR')[0]
mem_trans['c01'] = find_circuit('x00', 'y00', 'AND')[0]

# 
for i in range(1,45):
    i_end = str(i).zfill(2)
    
    # List with inputs for find_circuits function
    l_comps = [
        [f'xy_XOR_{i_end}', f'x{i_end}', f'y{i_end}', 'XOR'],
        [f'xy_AND_{i_end}', f'x{i_end}', f'y{i_end}', 'AND'],
        [f'c_AND_{i_end}', f'xy_XOR_{i_end}', f'c{i_end}', 'AND'],
        [f'c{str(i+1).zfill(2)}', f'c_AND_{i_end}', f'xy_AND_{i_end}', 'OR'],
        [f'z{i_end}', f'xy_XOR_{i_end}', f'c{i_end}', 'XOR'],
    ]

    for comp in l_comps:
        # Try to find the circuit
        reg_name = find_circuit(comp[1], comp[2], comp[3])
        
        # If the circuit is found, set the name to the translation dictionary
        if len(reg_name) == 1:
            mem_trans[comp[0]] = reg_name[0]
        # Give a warning when multiple registers are possible
        # This case luckily didn't happen...
        elif len(reg_name) > 1:
            print('Multiple registers possible...')
            print(comp)
            print(reg_name)
        # If no registers are found, go into correction mode
        elif len(reg_name) == 0:

            # Save a state of the memory for debugging purposes
            mem_state[comp[0]] = [
                mem_trans.copy(),
                insts.copy()
            ]
            print('No registers found:', comp)

            # Get candidates for the swap from the first element
            l_swap_comp1 = [
                ins 
                for ins 
                in insts 
                if (ins[0] == mem_trans[comp[1]] and ins[1] == comp[3]) or\
                    (ins[2] == mem_trans[comp[1]] and ins[1] == comp[3])
            ]
            print('Swap list 1:', l_swap_comp1)

            # Get candidates for the swap from the second element
            l_swap_comp2 = [
                ins 
                for ins 
                in insts 
                if (ins[0] == mem_trans[comp[2]] and ins[1] == comp[3]) or\
                    (ins[2] == mem_trans[comp[2]] and ins[1] == comp[3])
            ]
            print('Swap list 2:', l_swap_comp2)
            
            # Find registers to swap from the candidate swap list that contains more than 1 element
            # In all cases, there was only 1 such candidate
            if len(l_swap_comp1) > 0:
                swap1 = mem_trans[comp[2]]
                # In case the first comp element gave a list, we need to swap the second comp element
                
                # If the first element was equal to the first comp-element, set second element for swap
                # Otherwise set first element up for a swap
                if l_swap_comp1[0][0] == mem_trans[comp[1]]:
                    swap2 = l_swap_comp1[0][2]
                else:
                    swap2 = l_swap_comp1[0][0]

                # Set the last element as the register for the value we wanted to find
                register_to_set = l_swap_comp1[0][3]
            elif len(l_swap_comp2) > 0:
                # In case the second comp element gave a list, we need to swap the first comp element
                swap1 = mem_trans[comp[1]]

                # Check whether first element was equal to second comp element
                # Set swap accordingly
                if l_swap_comp2[0][0] == mem_trans[comp[2]]:
                    swap2 = l_swap_comp2[0][2]
                else:
                    swap2 = l_swap_comp2[0][0]

                # Set register name for this one equal to the last element of the row
                register_to_set = l_swap_comp2[0][3]

            # Go over the instructions to find swap1 and swap2 and change these
            for i, ins in enumerate(insts):
                if ins[3] == swap2:
                    print(i, ':' , insts[i][3], 'for', swap1)
                    insts[i][3] = swap1
                elif ins[3] == swap1:
                    print(i, ':' , insts[i][3], 'for', swap2)
                    insts[i][3] = swap2

            # Go over the translation dictionary and change the appropiate keys in the mem_trans
            for key in mem_trans:
                if mem_trans[key] == swap2:
                    mem_trans[key] = swap1
                elif mem_trans[key] == swap1:
                    mem_trans[key] = swap2
            
            # Set the register to this value
            mem_trans[comp[0]] = register_to_set

            # Add the swap-values to the set for later use/
            registers_swapped.add(swap1)
            registers_swapped.add(swap2)


print(','.join(sorted(registers_swapped)))