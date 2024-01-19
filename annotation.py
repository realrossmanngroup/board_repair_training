import pandas as pd
import os
import re
import json 

#make dataframe to store jargon
jargon_dataframes = {}
#where jargon is
jargon_directory = '/home/louis/board_repair_training/jargon_lists/'
#read each csv file with a jargon list into a pandas dataframe named by the type of jargon it is(resistors, signals, etc)
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

# Load DataFrames (assuming this part is already done)
# For example: resistors_df, capacitors_df, etc.

print("DATAFRAME JARGON_DATAFRAMES BELOW\n\n")
print(jargon_dataframes)
print("\n\nDATAFRAME COMBINED_JARGON_DF BELOW!\n\n")
print(combined_jargon_df)
print("\n\n")

'''
def annotate_jargon(text, df):
	for index, row in df.iterrows():
		jargon = row[df.columns[0]]
		description = row['Description'] if 'Description' in df.columns else ''
		jargon_type = row['jargon_type']

		# Don't mess me up if there is jargon inside jargon
		pattern = r'\b' + re.escape(jargon) + r'\b'
		
		# Check if the jargon is in the text
		if re.search(pattern, text):
			if pd.notnull(description) and description.strip() != '':  # Check if there's a description and it's not empty
				annotation = f"<s>[INST] [{jargon_type}]{jargon}[/{jargon_type}]: {description} [/INST]</s>"
			else:
				annotation = f"[{jargon_type}]{jargon}[/{jargon_type}]"
            
			#Replace only the specific instance of jargon in the text
			text = re.sub(pattern, annotation, text)
	return text

# Directory where your JSON files are located
thread_directory = '/home/louis/board_repair_training/threads/'

# Iterate through each JSON file
for filename in os.listdir(thread_directory):
	if filename.endswith('.json'):
		file_path = os.path.join(thread_directory, filename)
		try:
			#Open and load the JSON file
			with open(file_path, 'r') as file:
				data = json.load(file)
				print(f"\n\n{data}\n\n")

			#Assuming the structure of your JSON file is a list of posts or similar
			for post in data:
				#Annotate for each type of jargon using respective DataFrame
				post['title'] = annotate_jargon(post['title'], combined_jargon_df)
				post['message'] = annotate_jargon(post['message'], combined_jargon_df)
					
			with open(file_path, 'w') as file:
				json.dump(data, file)
		except Exception as e:
			print(f"Error processing file '{filename}': {e}")

'''
