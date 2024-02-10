import pandas as pd
import os
import re
import json
import traceback
from concurrent.futures import ProcessPoolExecutor

# Make dataframe to store jargon
jargon_dataframes = {}
# Where jargon is
jargon_directory = '/home/louis/board_repair_training/jargon_lists/'
# Read each CSV file with a jargon list into a pandas dataframe named by the type of jargon it is (resistors, signals, etc)
for eachfile in os.listdir(jargon_directory):
	if eachfile.endswith('.csv'):
		file_path = os.path.join(jargon_directory, eachfile)
		file_name = os.path.splitext(eachfile)[0]
		jargon_dataframes[file_name] = pd.read_csv(file_path, header=0).fillna('')

'''
Combine all jargon dataframes with an additional 'jargon_type' column
When I run my command to annotate separately based on the different jargon types
being in different dataframes, I wind up with annotations within annotations of
annotations and that's a mess. I have to look for them all at once, but
I also need to know the name of the jargon if they are all in one combined
dataframe, which requires an extra column.
'''

combined_jargon_df = pd.DataFrame()
for jargon_type, df in jargon_dataframes.items():
	df['jargon_type'] = jargon_type.upper()  # Add a column for jargon type
	combined_jargon_df = pd.concat([combined_jargon_df, df], ignore_index=True)

# Compile regex patterns for each jargon term outside the loop
jargon_patterns = {
        row['NAME']: {
                'pattern': re.compile(r'\b' + re.escape(row['NAME']) + r'\b', re.IGNORECASE),
                'description': row['DESCRIPTION'] if not pd.isna(row['DESCRIPTION']) and row['DESCRIPTION'].strip() != '' else f"a {row['jargon_type']}",
                'jargon_type': row['jargon_type']
        }
        for _, row in combined_jargon_df.iterrows()
}

# Compile regex patterns for each jargon term outside the loop
# so this isn't slow. we do this once, so we never have to do it again!
jargon_patterns = {
	row['NAME']: {
		'pattern': re.compile(r'\b' + re.escape(row['NAME']) + r'\b', re.IGNORECASE),
		'description': row['DESCRIPTION'] if not pd.isna(row['DESCRIPTION']) and row['DESCRIPTION'].strip() != '' else f"a {row['jargon_type']}",
		'jargon_type': row['jargon_type']
	}
	for _, row in combined_jargon_df.iterrows()
}

#annotate jargon in the JSON file
def annotate_jargon(text, jargon_patterns):
	found_jargon = {}  # Dictionary to hold jargon terms found in the text
	for jargon, info in jargon_patterns.items():
		# Check if the jargon is in the text (case-insensitive search)
		if info['pattern'].search(text):
			annotation = f"<{info['jargon_type']}>{jargon}</{info['jargon_type']}>"
			text = info['pattern'].sub(annotation, text)  # Replace jargon with annotation
			found_jargon[jargon] = info['description']  # Store found jargon description

	return text, found_jargon

# Define a function to process each file
def process_file(filename):
	file_path = os.path.join(thread_directory, filename)
	try:
		# Open and load the JSON file
		with open(file_path, 'r') as file:
			data = json.load(file)

		# Initialize a dictionary to hold all definitions for this file
		all_definitions = {}

		# Go through JSON file and find content in 'threads'
		for post in data['threads']:
			# Annotate for each type of jargon using dataframe of jargon. 
			# THIS FUNCTION RETURNS TWO THINGS, remember for later if this confuses you
			# the second thing it returns is a dictionary, not one single value
			post['title'], found_jargon_title = annotate_jargon(post['title'], jargon_patterns)
			post['message'], found_jargon_message = annotate_jargon(post['message'], jargon_patterns)

			# Update all_definitions only with jargon found in the text
			for jargon, definition in found_jargon_title.items():
				all_definitions[jargon] = definition
			for jargon, definition in found_jargon_message.items():
				all_definitions[jargon] = definition

		# Format the definitions section
		formatted_definitions = {}
		for jargon, definition in all_definitions.items():
			formatted_definitions[jargon] = f"What is {jargon}? {definition}."

		# Add the formatted definitions to the 'definitions' section in data
		data['definitions'] = formatted_definitions

		# Write the updated data back to the file
		with open(file_path, 'w') as file:
			json.dump(data, file, indent=4, ensure_ascii=False)
			print(f"\nDEBUG OUTPUT - WE JUST WROTE {file_path}\n")

	except Exception as e:
		print(f"Error processing file '{filename}': {e}")
		traceback.print_exc()

# Directory where your JSON files are located
thread_directory = '/home/louis/board_repair_training/threads/'

# Get list of filenames to process
filenames = [f for f in os.listdir(thread_directory) if f.endswith('.json')]
print(filenames)

# Use ThreadPoolExecutor to process files in parallel
with ProcessPoolExecutor(max_workers=20) as executor:
	executor.map(process_file, filenames)
