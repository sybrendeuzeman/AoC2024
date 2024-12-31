import numpy as np

with open('input.txt') as file:
    input = [line for line in [key.split('\n') for key in file.read().split('\n\n')]]


keys = []
locks = []


for key_lock in input:
    sign_check = key_lock[0][0]

    serial_l = [-1] * len(key_lock[0])
    for line in key_lock:
        for i in range(len(line)):
            serial_l[i] += line[i] == '#'

    serial = ''.join([str(i) for i in serial_l])

    if sign_check == '#':
        locks.append(serial_l)
    elif sign_check == '.':
        keys.append(serial_l)
    
keys_array = np.array(keys)

lock_key_combos = 0
for lock in locks:
    lock_key_combos += np.sum(np.all(keys_array + np.array(lock) <= 5, axis = 1))

print(lock_key_combos)