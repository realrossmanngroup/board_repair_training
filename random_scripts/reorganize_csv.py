import pandas as pd

# Input CSV file path
csvfile = "/home/louis/board_repair_training/jargon_lists/signals.csv"	# Update this path to your CSV file

# Load the CSV file into a DataFrame
signal_df = pd.read_csv(csvfile, header=0)

# Iterate over rows in the DataFrame and update as necessary
for index, row in signal_df.iterrows():
	if pd.isnull(row['DESCRIPTION']) and pd.notnull(row['BARD']):
		signal_df.at[index, 'DESCRIPTION'] = row['BARD']
		signal_df.at[index, 'BARD'] = None	# or use '' for an empty string

# Save the modified DataFrame back to the CSV file, outside the loop
signal_df.to_csv(csvfile, index=False)
