
# Function to find potential solutions and check to the solution to be tested
def check_potential_solution(list_numbers, solution_test):
    # Initialize list
    list_partial_solutions = [list_numbers[0]]
    
    # Go through list of numbers and make new partial solution
    for number in list_numbers[1:len(list_numbers)]:
        # Add number to the list
        list_add = [
            partial + number
            for partial
            in list_partial_solutions
            if partial <= solution_test # Check if partial is not already over the solution_test
        ]

        # Multiply with number
        list_multiplication = [
            partial * number
            for partial
            in list_partial_solutions
            if partial <= solution_test # Check if partial is not already over the solution_test
        ]

        list_partial_solutions = list_add + list_multiplication # add lists together
    # Return boolean whether solution test is in the list with partial solutions
    return solution_test in list_partial_solutions

# Initialize aggregator
total_solutions = 0
with open('input.txt') as file:
    for line in file:

        # Set solution test and list_numbers
        solution_test = int(line.split(': ')[0])
        list_numbers = [int(number_str) for number_str in line.split(': ')[1].split(' ')]

        # Check whether there is a solution
        check = check_potential_solution(list_numbers, solution_test)
        
        # If there is a solution add to aggregator
        if check:
            total_solutions += solution_test

print('Total sum of correct solutions:', total_solutions)