with open('input.txt') as file:
    input = [int(line) for line in file.read().rstrip('\n').split('\n')]

def next_secret(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216

    return(secret)

# Part 1
sum_sec = 0
for inp in input:
    secret = inp
    for i in range(2000):
        secret = next_secret(secret)

    sum_sec += secret

print(sum_sec)

# Part 2

# Fill a dictionary for every preceding sequence of changes
banana_with_changes = {}

# Add possible banana's with all monkeys
for inp in input:

    secret = inp

    # Initialize the old prize
    old_prize = secret % 10
    
    # Keep track of last 4 changes
    last_changes = []
    
    # Keep track of changes for which banana's where already bought
    already_bought = set()
    
    for i in range(2000):
        # Get the next secret number
        secret = next_secret(secret)

        # Get prize 
        new_prize = secret % 10

        # Add to list with last changes
        last_changes.append(new_prize - old_prize)
        
        # Add number of banana's to dictionary if there are 4 last changes
        if (len(last_changes) == 4):
            # Make the list hashable for the dictionary
            key = ','.join([str(i) for i in last_changes])

            # Only possible to buy if not yet bought with sequence at this monkey
            if (key not in already_bought):
                # Add the  prize to the dictionary at the key
                banana_with_changes[key] = banana_with_changes.get(key, 0) + new_prize
                # Add the key to the set of sequences where you already bought
                already_bought.add(key)

            # Remove the first of the last changes from the list
            last_changes = last_changes[1:]
        
        # Set old prize is new prize
        old_prize = new_prize
print('Maximum amount of bananas is:', max(banana_with_changes.values()))