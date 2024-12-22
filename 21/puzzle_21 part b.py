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


def path_h(start, end):
    # Find which part must be traveled
    travel = locs_keypad[end] - locs_keypad[start]

    # Set signs for horizontal en vertical paths
    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    # Make a vertical first and horizontal first path
    h_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    h_hor = mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    # Give the best path
    if (locs_keypad[end][1] == 0) and (locs_keypad[start][0] == 0):
        return h_vert
    elif (locs_keypad[start][1] == 0) and (locs_keypad[end][0] == 0):
        return h_hor
    else:
        if len(h_hor) <= len(h_vert):
            return h_hor
        else:
            return h_vert

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

def path_r2(start, end):
    travel = locs_numpad[end] - locs_numpad[start]

    mov_vert = 'v' if travel[0] > 0 else '^'
    mov_hor = '>' if travel[1] > 0 else '<'
    
    r2_vert = mov_vert * abs(travel[0]) + mov_hor * abs(travel[1]) + 'A'
    r2_hor =  mov_hor * abs(travel[1]) + mov_vert * abs(travel[0]) + 'A'

    dict_moves_hor = {r2_hor : 1}
    for i in range(25):
        dict_moves_hor = iter_new_dict(dict_moves_hor.copy())
    l_hor = 0
    for key in dict_moves_hor:
        l_hor += len(key) * dict_moves_hor[key]

    dict_moves_vert = {r2_vert : 1}
    for i in range(25):
        dict_moves_vert = iter_new_dict(dict_moves_vert.copy())
    l_vert = 0
    for key in dict_moves_vert:
        l_vert += len(key) * dict_moves_vert[key]

    if (locs_numpad[start][1] == 0) and (locs_numpad[end][0] == 3):
        return l_hor
    elif (locs_numpad[start][0] == 3) and (locs_numpad[end][1] == 0):
        return l_vert
    else:
        if l_hor < l_vert:
            return l_hor
        else:
            return l_vert
        
def path_N(seq):
    r1 = 0
    start = 'A'
    for end in seq:
        r1 += path_r2(start, end)
        start = end
    return r1


def get_new_seq(old_seq):
    start = 'A'
    new_seq = ''
    for end in old_seq:
        new_seq += path_h(start, end)
        start = end
    return new_seq


def iter_new_dict(dict_moves):
    dict_moves_new = {}
    for key in dict_moves:
        seq = get_new_seq(key)
        
        while len(seq) > 0:
            posA = seq.find('A')
            seq[:posA+1]

            dict_moves_new[seq[:posA+1]] = dict_moves_new.get(seq[:posA+1], 0) + dict_moves[key]

            seq =  seq[posA+1:]
    return dict_moves_new


sol = 0
for line in input:
    r1 = path_N(line)
    print(line, ':', r1)
    sol += r1 * int(line[:3])

print(sol)
