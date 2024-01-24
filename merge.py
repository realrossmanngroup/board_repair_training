import pandas as pd

# Step 1: Read CSV files into DataFrames
csv_file_a = '1.csv'
csv_file_b = '2.csv'

df_a = pd.read_csv(csv_file_a)
df_b = pd.read_csv(csv_file_b)

# Step 2: Filter rows in CSV A with both NAME and DESCRIPTION columns populated
filtered_df_a = df_a.dropna(subset=['NAME', 'DESCRIPTION']).copy()

# Step 3: Add an index column to CSV B before merging
df_b['index_col'] = range(len(df_b))

# Step 4: Convert the "NAME" column to uppercase in both DataFrames
filtered_df_a['NAME'] = filtered_df_a['NAME'].str.upper()
df_b['NAME'] = df_b['NAME'].str.upper()

# Step 5: Merge CSV A with CSV B based on the lowercase "NAME" column
merged_df = filtered_df_a.merge(df_b, on='NAME', how='right')

# Step 6: Sort the resulting DataFrame by the index column to retain row order from CSV B
merged_df.sort_values(by='index_col', inplace=True)

# Step 7: Drop the index column
merged_df.drop(columns=['index_col'], inplace=True)

# Step 8: Save the resulting DataFrame to a new CSV file
output_csv_file = 'matched_data.csv'
merged_df.to_csv(output_csv_file, index=False)

print(f"Matching data saved to {output_csv_file}")
