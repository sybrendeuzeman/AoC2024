import re
import numpy as np
import glob

with open('input.txt') as file:
    list_robot = file.read().rstrip('\n').split('\n')

# Part 1
n_seconds = 100
dim_x = 101
dim_y = 103

pattern_robot_init = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'

dict_end_pos = {
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    7 : 0,
    8 : 0,
    9 : 0,
    10 : 0
}
for robot in list_robot:
    match_robot = re.match(pattern_robot_init, robot).groups()

    pos_x = int(match_robot[0])
    pos_y = int(match_robot[1])
    vel_x = int(match_robot[2])
    vel_y = int(match_robot[3])
   
    x = (pos_x + vel_x * n_seconds) % dim_x
    y = (pos_y + vel_y * n_seconds) % dim_y

    quadrant= 2*(x < dim_x//2) + 4*(x > dim_x // 2) + 5*(y < dim_y//2) + 6*(y > dim_y // 2)
    
    dict_end_pos[quadrant] += 1

    print(robot, '\nx:', x, 'y:', y, 'quad', quadrant)

safety_factor = dict_end_pos[7] * dict_end_pos[8] * dict_end_pos[9] * dict_end_pos[10]
print('The safety factor is:', safety_factor)


# Part 2:

list_special_pattern = [
    69 + i * 101
    for i
    in range(0,100)
]

for i in list_special_pattern:
    card = np.empty((dim_x, dim_y), dtype='str')
    card[:] = ' '
    
    for robot in list_robot:
        match_robot = re.match(pattern_robot_init, robot).groups()

        pos_x = int(match_robot[0])
        pos_y = int(match_robot[1])
        vel_x = int(match_robot[2])
        vel_y = int(match_robot[3])
    
        x = (pos_x + vel_x * i) % dim_x
        y = (pos_y + vel_y * i) % dim_y

        card[x,y] = 'X'


    np.savetxt(f'cards/{i}.txt', card, fmt='%s', delimiter='')

