
with open('input.txt', 'r') as f:
    list_reports = f.readlines()

list_report_numbers = [
    [
        int(number)
        for number
        in report.replace('\n', '').split(' ')
    ] 
    for report
    in list_reports
]


# Problem 1:
# Define function to check a single report
def check_report(report_numbers):
    # Set sign decr or incr
    if report_numbers[0] > report_numbers[1]:
        sign = -1
    elif report_numbers[0] < report_numbers[1]:
        sign = 1
    elif report_numbers[0] == report_numbers[1]:
        return False # No increase between first two integers
    else:
        raise Exception(f"Setting of sign had unexpected result for {report}")
    
    # Check sequence
    number_prev = report_numbers[0]
    for i in range(1,len(report_numbers)):
        number_curr = report_numbers[i]
        if sign*(number_curr - number_prev) in [1,2,3]:
            number_prev = number_curr
            continue # Check succeeded
        else:
            return False # Check failed, no need to check more
        

    return True # All checks succeeded.

# Check all reports
list_check_report = [
    check_report(report_numbers)
    for report_numbers
    in list_report_numbers
]

# Get number of succeeded checks
number_succeeded_checks = sum(list_check_report)

print(f'Number of succeeded checks: {number_succeeded_checks}')

#Problem 2:

# Wrapper to implement the dampener
def check_with_dampener(report_numbers):
    first_check = check_report(report_numbers)

    if first_check == True:
        return True
    
    for i_del in range(0,len(report_numbers)):
        report_temp = report_numbers[:]
        del report_temp[i_del]
        
        check_after_delete = check_report(report_temp)

        if check_after_delete == True:
            return True
        
    return False

# Get list with checks
list_check_dampened = [
    check_with_dampener(report_numbers)
    for report_numbers
    in list_report_numbers
]

number_succeeded_checks_dampened = sum(list_check_dampened)

print(f'Number of succeeded checks with dampener: {number_succeeded_checks_dampened}')
