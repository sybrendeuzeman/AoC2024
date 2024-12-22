import numpy as np

with open('input.txt') as file:
    input = [line for line in file.read().rstrip('\n').split('\n')]

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

# Part 1

def path_N(seq):
    r1 = ''
    start = 'A'
    for end in seq:
        r1e = path_r2(start, end)
        r1 = r1 + r1e
        start = end
    return r1
    

def path_r2(start, end):
    travel = locs_numpad[end] - locs_numpad[start]

    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    r2_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    r2_hor =  mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    r1_vert = ''
    start_l = 'A'
    for end_l in r2_vert:
        r1_vert = r1_vert + path_r1(start_l, end_l)
        start_l = end_l

    r1_hor = ''
    start_l = 'A'
    for end_l in r2_hor:
        r1_hor = r1_hor + path_r1(start_l, end_l)
        start_l = end_l

    if (locs_numpad[start][1] == 0) and (locs_numpad[end][0] == 3):
        return r1_hor
    elif (locs_numpad[start][0] == 3) and (locs_numpad[end][1] == 0):
        return r1_vert
    else:
        if len(r1_hor) <= len(r1_vert):
            return r1_hor
        else:
            return r1_vert

def path_r1(start, end):
    travel = locs_keypad[end] - locs_keypad[start]

    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    r1_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    r1_hor = mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    r1_vert_t = ''
    start = 'A'
    for end in r1_vert:
        r1_vert_t += path_h(start, end)
        start = end

    r1_hor_t = ''
    start = 'A'
    for end in r1_hor:
        r1_hor_t += path_h(start, end)
        start = end

    if (locs_keypad[end][1] == 0) and (locs_keypad[start][0] == 0):
        return r1_vert_t
    elif (locs_keypad[start][1] == 0) and (locs_keypad[end][0] == 0):
        return r1_hor_t
    else:
        if len(r1_hor_t) < len(r1_vert_t):
            return r1_hor_t
        else:
            return r1_vert_t


def path_h(start, end):
    travel = locs_keypad[end] - locs_keypad[start]

    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    h_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    h_hor = mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    if (locs_keypad[end][1] == 0) and (locs_keypad[start][0] == 0):
        return h_vert
    elif (locs_keypad[start][1] == 0) and (locs_keypad[end][0] == 0):
        return h_hor
    else:
        if len(h_hor) <= len(h_vert):
            return h_hor
        else:
            return h_vert

sol = 0
for line in input:
    r1 = path_N(line)
    print(line, ':', len(r1))
    sol += len(r1) * int(line[:3])

print(sol)

# Part 2

dict_moves = {}
for i in locs_keypad.keys():
    for j in locs_keypad.keys():
        dict_moves[i+j] = path_h(i, j)

dict_moves_iter = dict_moves.copy()
for i in range(1):
    dict_moves_2 = {}
    for i in dict_moves:
        seq = 'A' + dict_moves_iter[i]
        new_seq = ''
        for j in range(len(seq)-1):
            new_seq  += dict_moves[seq[j:j+2]]
        
        dict_moves_2[i] = new_seq
    dict_moves_iter = dict_moves_2.copy()


def path_N(seq):
    r1 = 0
    start = 'A'
    for end in seq:
        r1e = path_r2(start, end)
        r1 = r1 + r1e
        start = end
    return r1

def path_r2(start, end):
    travel = locs_numpad[end] - locs_numpad[start]

    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    r2_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    r2_hor =  mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    # Horizontal
    seq = 'A' + r2_hor

    r1_hor_dict = {}
    for j in range(len(seq)-1):
        r1_hor_dict[seq[j:j+2]] = r1_hor_dict.get(seq[j:j+2], 0) + 1

    for i in range(2):
        r1_hor_dict_new = {}
        for key in r1_hor_dict:
            seq = 'A' + key
            for j in range(len(seq)-1):
                r1_hor_dict_new[seq[j:j+2]] = r1_hor_dict_new.get(seq[j:j+2], 0) + r1_hor_dict[key]

        r1_hor_dict = r1_hor_dict_new.copy()

    sum_hor = sum(r1_hor_dict.values())

    # Vertical
    seq = 'A' + r2_vert

    r1_vert_dict = {}
    for j in range(len(seq)-1):
        r1_vert_dict[seq[j:j+2]] = r1_vert_dict.get(seq[j:j+2], 0) + 1

    for i in range(1):
        r1_vert_dict_new = {}
        for key in r1_vert_dict:
            seq = 'A' + key
            for j in range(len(seq)-1):
                r1_vert_dict_new[seq[j:j+2]] = r1_vert_dict_new.get(seq[j:j+2], 0) + r1_vert_dict[key]

        r1_vert_dict = r1_vert_dict_new.copy()    
    
    sum_vert = sum(r1_vert_dict.values())


    if (locs_numpad[start][1] == 0) and (locs_numpad[end][0] == 3):
        return sum_hor
    elif (locs_numpad[start][0] == 3) and (locs_numpad[end][1] == 0):
        return sum_vert
    else:
        if sum_hor <= sum_vert:
            return sum_hor
        else:
            return sum_vert