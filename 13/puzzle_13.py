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
    
    mat_buttons = np.array(
        [
            [int(input[0]), int(input[2])],
            [int(input[1]), int(input[3])]
        ]
    )

    mat_puzzle = np.array(
        [
            int(input[4]),
            int(input[5])
        ]
    )

    array_prices = np.array(
        [
            [3,1]
        ]

    )

    mat_sol = np.linalg.solve(mat_buttons, mat_puzzle)
    print(mat_sol)

    is_sol_integer = np.allclose(mat_sol, mat_sol.round()) 
    is_sol_above_0 = np.all(mat_sol >= 0)
    is_sol_under_100 = np.all(mat_sol <= 100)
    print('Above 0:', is_sol_above_0)
    print('Integer:', is_sol_integer)
    print('Under 100:', is_sol_under_100)
    
    total_tokens += np.sum(array_prices * mat_sol)*is_sol_integer*is_sol_under_100*is_sol_above_0

print('Total amount of tokens is:', total_tokens)

# Part 2
total_tokens = 0
for machine in machines:
    print(machine)
    input = re.search(pattern, machine).groups()
    
    mat_buttons = np.array(
        [
            [int(input[0]), int(input[2])],
            [int(input[1]), int(input[3])]
        ]
    )

    mat_puzzle = np.array(
        [
            int(input[4]) + 10000000000000,
            int(input[5]) + 10000000000000
        ]
    )

    array_prices = np.array(
        [
            [3,1]
        ]

    )

    mat_sol = np.linalg.solve(mat_buttons, mat_puzzle)
    print('A', mat_sol[0], 'B', mat_sol[1])

    is_sol_integer = np.allclose(mat_sol - mat_sol.round()+1, 1, rtol = 0.001, atol = 0.001) 
    is_sol_above_0 = np.all(mat_sol >= 0)
    print('Above 0:', is_sol_above_0)
    print('Transform:', mat_sol - mat_sol.round()+1)
    print('Integer:', is_sol_integer)
    
    total_tokens += np.sum(array_prices * mat_sol)*is_sol_integer*is_sol_above_0

print('Total amount of tokens is:', total_tokens)