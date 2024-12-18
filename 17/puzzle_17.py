import re
with open('input.txt') as file:
    input = file.read().split('\n\n')

reg_init = dict(
    [
        (
            re.search(r'Register ([A-C]): (\d+)', register).groups()[0], 
            int(re.search(r'Register ([A-C]): (\d+)', register).groups()[1])
        )            
        for register
        in input[0].split('\n')
    ]
)

prog = [int(a) for a in input[1].split(' ')[1].split(',')]

# Part One:

def cv(com):
    if com <= 3:
        return com
    if com == 4:
        return reg['A']
    if com == 5:
        return reg['B']
    if com == 6:
        return reg['Ç']

p = 0
pointer_in_bound = True

reg = reg_init.copy()
#reg['A'] = 190384609508367

output = ''
while pointer_in_bound:
    get_instruction = prog[p]

    if prog[p] == 0: # adv
        reg['A'] = int(reg['A'] / pow(2, cv(prog[p + 1])))
        p += 2
    elif prog[p] == 1: # bxl
        reg['B'] = reg['B'] ^ prog[p+1]
        p += 2
    elif prog[p] == 2: # bst
        reg['B'] = cv(prog[p+1]) % 8
        p += 2
    elif prog[p] == 3: #jnz
        if reg['A'] != 0:
            p = prog[p + 1]
        else:
            p += 2
    elif prog[p] == 4: #bxc
        reg['B'] = reg['B'] ^ reg['C']
        p += 2
    elif prog[p] == 5: #out
        if output == '':
            output += str(cv(prog[p+1]) % 8)
        else:
            output += f',{cv(prog[p+1]) % 8}'
        p += 2
    elif prog[p] == 6: #bdv
        reg['B'] = int(reg['A'] / pow(2, cv(prog[p + 1])))
        p += 2
    elif prog[p] == 7: #bdv
        reg['C'] = int(reg['A'] / pow(2, cv(prog[p + 1])))
        p += 2

    pointer_in_bound = p < len(prog)
print(output)


# Part Two:

# The print from the machine is only dependent on A at the start of line of commands:
#0: b = a % 8
#1: b = b ^ 2 = (a % 8) ^ 2
#2: c = a / pow(2, b) = int(a / pow(2, (a % 8) ^ 2))
#3: b = b ^ c = ((a % 8) ^ 2) ^ (int(a / pow(2, (a % 8) ^ 2)))
#4: a = a / 8
#5: b = b ^ 7 = (((a % 8) ^ 2) ^ (int(a / pow(2, (a % 8) ^ 2)))) ^ 7
#6: print b % 8 = ((((a % 8) ^ 2) ^ (int(a / pow(2, (a % 8) ^ 2)))) ^ 7) % 8
#7: Move pointer to 0

def print_from_a(a):
    return ((((a % 8) ^ 2) ^ (int(a / pow(2, (a % 8) ^ 2)))) ^ 7)% 8

# At last print, a needs to be in range 1-8 to get a = 0 and stop at the end
pos_as = list(range(1,8))

for i in range(len(prog) - 1, 0, -1):
        
    new_pos_as = []
    # What print needs to be at the end
    target_b = prog[i]

    print(i, ':', len(pos_as), ':', target_b)

    # For all a's in list, check whether it returns the target_b
    # To get at a, the previous a needs to be between a * 8 and (a+1) * 8
    # Add these values to the list for the new round
    for pos_a in pos_as:
        if print_from_a(pos_a) == target_b:
            new_pos_as.extend(list(range(pos_a*8, (pos_a+1)*8)))

    # Set list for new round
    pos_as = new_pos_as


# Set a known to high number to initialize check
min_a = 152307687606693600

# Loop over all posibble answers, 
# Check whether it is a solution and keep minimum value
for pos_a in pos_as:
    if print_from_a(pos_a) == 2:
        min_a = min(pos_a, min_a)

print('Min A is:', min_a)