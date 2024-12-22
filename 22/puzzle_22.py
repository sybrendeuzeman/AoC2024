with open('input_test2.txt') as file:
    input = [int(line) for line in file.read().rstrip('\n').split('\n')]

def next_secret(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216

    return(secret)

sum_sec = 0
for inp in input:
    secret = inp
    for i in range(2000):
        secret = next_secret(secret)

    sum_sec += secret

print(sum_sec)

# Part 2
banana_with_changes = {}


for inp in input:

    secret = inp
    old_prize = secret % 10
    last_changes = []
    already_bought = set()
    
    for i in range(2000):
        secret = next_secret(secret)
        new_prize = secret % 10

        last_changes.append(new_prize - old_prize)
        
        if (len(last_changes) == 4):
            key = ','.join([str(i) for i in last_changes])
            if (key not in already_bought):
                banana_with_changes[key] = banana_with_changes.get(key, 0) + new_prize
                already_bought.add(key)
            last_changes = last_changes[1:]
        elif len(last_changes) >= 4:
            print('Last changes not')

        old_prize = new_prize
print('Maximum amount of bananas is:', max(banana_with_changes.values()))\