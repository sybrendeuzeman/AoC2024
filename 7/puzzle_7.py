

def check_potential_solution(list_numbers, solution_test):
    list_partial_solutions = [list_numbers[0]]
    for number in list_numbers[1:len(list_numbers)]:
        list_add = [
            partial + number
            for partial
            in list_partial_solutions
            if partial <= solution_test
        ]

        list_multiplication = [
            partial * number
            for partial
            in list_partial_solutions
            if partial <= solution_test
        ]

        list_partial_solutions = list_add + list_multiplication
    return solution_test in list_partial_solutions

total_solutions = 0
with open('input.txt') as file:
    for line in file:
        solution_test = int(line.split(': ')[0])
        list_numbers = [int(number_str) for number_str in line.split(': ')[1].split(' ')]

        check = check_potential_solution(list_numbers, solution_test)
        if check:
            total_solutions += solution_test

print('Total sum of correct solutions:', total_solutions)