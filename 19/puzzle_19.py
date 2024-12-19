import pandas as pd

with open('input.txt') as file:
    input = file.read().split('\n\n')

towels = input[0].split(', ')
patterns = input[1].rstrip('\n').split('\n')

pattern = patterns[0]



def check_pattern(pattern, towels = towels):
    towel_combs = set(towels)
    while True:
        # Get combination of towels possible
        towel_combs = [
            towel_comb + towel 
            for towel
            in towels
            for towel_comb
            in towel_combs
        ]

        # Check towels still valid
        towel_combs = {
            towel_comb
            for towel_comb
            in towel_combs
            if pattern.startswith(towel_comb)
        }

        # End if no towel combination is valid
        if len(towel_combs) == 0:
            return False
        
        # Return True if a towel combination is the pattern
        if pattern in towel_combs:
            return True

number_possible_patterns = 0    
for pattern in patterns:
    number_possible_patterns += check_pattern(pattern)

print('The number of possible patterns is', number_possible_patterns)

def get_new_patterns(towel_comb, towels):
    return [
            towel_comb + towel 
            for towel
            in towels
        ]

def check_pattern(pattern, towels = towels):
    df = pd.DataFrame()
    df['towel_comb'] = towels
    df['Number combinations'] = 1


    count_valid_patterns = 0
    while True:
        
        
        # Get combination of towels possible
        df['towel_comb'] = df['towel_comb'].apply(get_new_patterns, towels = towels)
        
        df = df.explode('towel_comb').groupby('towel_comb').agg('sum').reset_index()
        df = df.loc[df['towel_comb'].apply(pattern.startswith)]

        count_valid_patterns += sum(df.loc[df['towel_comb'] == pattern]['Number combinations'])

        if len(df) == 0:
            return count_valid_patterns

number_valid_combo = 0    
i = 0
for pattern in patterns:
    print(i, ':', len(patterns))
    number_valid_combo += check_pattern(pattern)
    i += 1

print('The number of possible patterns is', number_valid_combo)