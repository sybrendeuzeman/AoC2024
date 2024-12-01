import pandas as pd

# Get input
df_input = pd.read_csv('input.txt', sep = '   ', header = None)

# Part 1:
# Make a dataframe with two sorted columns
df_sorted = pd.DataFrame()
df_sorted['sorted_0'] = list(df_input[0].sort_values())
df_sorted['sorted_1'] = list(df_input[1].sort_values())

# Calculate total distance
df_sorted['distance'] = df_sorted['sorted_0'] - df_sorted['sorted_1']
total_distance = sum(df_sorted['distance'].abs())


# Part 2: 
# Count numnbers in 1
df_count_1 = pd.DataFrame()
df_count_1['count_1'] = df_input.groupby(1).count()
df_count_1 = df_count_1.reset_index()

# Check if count adds up to 0
sum(df_count_1['count_1'].fillna(0))

# Merge with 0 column:
df_0_counted_1 = df_input.merge(
    df_count_1, 
    left_on = 0, 
    right_on = 1, 
    how = 'left'
    )

total_similarity = sum(df_0_counted_1[0] * df_0_counted_1['count_1'].fillna(0))