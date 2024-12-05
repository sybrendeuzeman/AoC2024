import numpy as np
from itertools import compress

input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

# Get input into two array and list
with open('input.txt') as f:
    input = f.read()

input_rules = input.split('\n\n')[0]
input_updates = input.split('\n\n')[1]

array_rules = np.asarray(
    [
        [int(rule.split('|')[0]), int(rule.split('|')[1])]
        for rule
        in input_rules.split('\n')
    ]
)

list_updates = [
    [
        int(number)
        for number
        in update.split(',')
    ]
    for update
    in input_updates.rstrip('\n').split('\n')
]

# Problem 1

# Check for one rule and one update.
def check_rule(array_rules_row, update):
    # Set variable for readable code.
    first = array_rules_row[0] 
    second = array_rules_row[1]

    # Check whether rule is satisfied.
    if (first in update) and (second in update):
        return update.index(first)  < update.index(second)
    else:
        return True
    
def check_update(array_rules, update):
    # Check all rules with function check_rule for array.
    check_array = np.apply_along_axis(check_rule, 1, array_rules, update = update)
    
    # Only return update if all checks are succesful.
    if np.all(check_array):
        return update   
    
# Make a list with updates that follow all rules.
correct_updates = [
    check_update(array_rules, update)
    for update
    in list_updates
]

# Calculate the sum of the middle values of correct updates.
total_middle = sum(
    [   
        update[len(update) // 2]
        for update
        in correct_updates
        if update
    ]
)

print(f'Sum of middle value of correct updates is: {total_middle}')

# Problem 2
# Check the update and return the 'check_array'
def check_update_array(array_rules, update):
    check_array = np.apply_along_axis(check_rule, 1, array_rules, update = update)
    return check_array

# Correct update for one rule
def correct_update_rule(array_rules, update, check_array):
    # Find first rule in list that needs to be corrected
    rule_to_correct = array_rules[np.logical_not(check_array)][ 0,:]
    
    # Correct the rule; the correction is on immediately on the list
    update[update.index(rule_to_correct[0])] = rule_to_correct[1]
    update[update.index(rule_to_correct[1])] = rule_to_correct[0]

    return update

def correct_update(array_rules, update):
    # Initially check the update
    check_array = check_update_array(array_rules, update)
    
    # Set variable corrected with information if the update is corrected to be returned
    corrected = not np.all(check_array)
    

    while not np.all(check_array):
        # Update the first rule
        update = correct_update_rule(array_rules, update, check_array)
        # Make check array
        check_array = check_update_array(array_rules, update)
    
    return corrected

# Make list; correct the list_position and return list with true / false.
corrected_updates = [
    correct_update(array_rules, update)
    for update
    in list_updates
]

# Find total middle values of corrected updates.
total_corrected_updates = sum(
    [
        update[len(update)//2]
        for update
        in compress(list_updates, corrected_updates)
    ]
)
print(f"The total value of middle values of corrected updates is: {total_corrected_updates}.")



