import re
import pandas as pd

with open('input.txt', 'r') as f:
    text_input = f.read()

# Problem 1
# Find all multiplications in the text input.
multiplications = re.findall(r'mul\((\d+),(\d+)\)', text_input)

# Calculate the sum of the multiplications.
sum_multiplications = sum(
    [
        int(multiplication[0]) * int(multiplication[1])
        for multiplication
        in multiplications
    ]
)

# Print the answer.
print(f'The sum of the multiplications is: {sum_multiplications}')


# Problem 2:
# Get all instructions (mul, do, don't)
multiplication_do_dont = re.findall(r'(mul)\((\d+),(\d+)\)|(don)\'t\(\)|(do)\(\)', text_input)

# Create dataframe from list
df_instructions = pd.DataFrame(multiplication_do_dont)

# Make one column for do and don't, fill the column and use fillna to fill the first rows.
df_instructions['do-dont'] = (
    (df_instructions[3] + df_instructions[4])
    .replace('', None)
    .ffill()
    .fillna('do')
    )

# Filter the df_instructions on 'do' and filter out empty multiplications
df_instructions = df_instructions[(df_instructions['do-dont']=='do')&(df_instructions[1] != '')]

# Get the sum of all the enabled multiplications
sum_multiplications_do = sum(
    df_instructions[1].astype(int) * df_instructions[2].astype(int)
)
print(f'The sum of enabled multiplications is {sum_multiplications_do}')