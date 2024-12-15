import numpy as np
import re

with open('input.txt') as file:
    machines = file.read().split('\n\n')
pattern = r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)'

# Part 1
total_tokens = 0
for machine in machines:
    print(machine)
    input = re.search(pattern, machine).groups()
    

    a = (int(input[3]) * int(input[4]) -  int(input[2]) * int(input[5]))
    b = (-int(input[1]) * int(input[4]) + int(input[0])* int(input[5]))

    det = int(input[0]) * int(input[3]) - int(input[2]) * int(input[1])

    is_sol_integer = a % det + b % det == 0

    print('Integer:', is_sol_integer)
    
    total_tokens += np.sum( (a // det)*3 + (b//det))*is_sol_integer

print('Total amount of tokens is:', total_tokens)

# Part 2
total_tokens = 0
for machine in machines:
    print(machine)
    input = re.search(pattern, machine).groups()
    

    a = int(input[3]) * (int(input[4]) + 10000000000000)-  int(input[2]) * (int(input[5]) + 10000000000000)
    b = -int(input[1]) * (int(input[4]) + 10000000000000) + int(input[0])* (int(input[5]) + 10000000000000)

    det = int(input[0]) * int(input[3]) - int(input[2]) * int(input[1])

    is_sol_integer = a % det + b % det == 0

    print('Integer:', is_sol_integer)
    
    total_tokens += np.sum( (a // det)*3 + (b//det))*is_sol_integer

print('Total amount of tokens is:', total_tokens)
