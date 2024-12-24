import numpy as np
import re

with open('input.txt') as file:
    input = [line.split('-') for line in file.read().rstrip('\n').split('\n')]


dict_conn = {}
for line in input:
    dict_conn[line[0]] = np.append(dict_conn.get(line[0], np.array([])), line[1])
    dict_conn[line[1]] = np.append(dict_conn.get(line[1], np.array([])), line[0])

# Part 1:
conns = set()
for key, value in dict_conn.items():
    for c in value:
        interconnected = np.intersect1d(value, dict_conn[c])

        for cc in interconnected:
            conn = ','.join(sorted((key, c, cc)))
            conns.add(conn)

print('The number of three interconnected computers is:', sum([(conn.startswith('t')) or (',t' in conn) for conn in conns]))


# Part 2:

def find_biggest_connect(comp):
    l = []
    for c in dict_conn[comp]:
        l.append([sorted([comp, c]), np.intersect1d(dict_conn[comp], dict_conn[c])])

    found = {
        ','.join(l0[0])
        for l0
        in l
    }

    cnt = True
    while cnt:
        cnt = False
        delete = []
        for i, extend in enumerate(l):
            if len(extend[1]) > 0:
                for c in extend[1]:
                    path_extended = sorted(extend[0] + [c])
                    join_path_extended = ','.join(path_extended)
                    if join_path_extended in found:
                        continue

                    intersect = np.intersect1d(extend[1], dict_conn[c])
                    
                    if len(intersect) > 0:
                        cnt = True
                    
                    l.append([path_extended, intersect])
                    found.add(join_path_extended)
                delete.append(i)
                
        for i in sorted(delete, reverse=True):
            del l[i]

    l.sort(key = lambda s: -len(s[0]))

    ret = ','.join(sorted(l[0][0]))

    return ret

biggest_until = ''
for i, comp in enumerate(dict_conn.keys()):
    print(i, ':',comp)
    comp_net = find_biggest_connect(comp)

    if len(comp_net) > len(biggest_until):
        biggest_until = comp_net

print(biggest_until)
    
