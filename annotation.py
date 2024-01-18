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
	file_path = os.path.join(jargon_directory, eachfile)
	file_name = os.path.splitext(eachfile)[0]
	jargon_dataframes[file_name] = pd.read_csv(file_path, header=0).fillna('')

# Load DataFrames (assuming this part is already done)
# For example: resistors_df, capacitors_df, etc.

def annotate_jargon(text, df, jargon_type):
    for index, row in df.iterrows():
        jargon = row[df.columns[0]]
        description = row[df.columns[1]]
        # Don't mess me up if there is jargon inside jargon
        pattern = r'\b' + re.escape(jargon) + r'\b'
        
        # Check if the jargon is in the text
        if re.search(pattern, text):
            if pd.notnull(description) and description.strip() != '':  # Check if there's a description and it's not empty
                annotation = f"<s>[INST] [{jargon_type}]{jargon}[/{jargon_type}]: {description} [/INST]</s>"
            else:
                annotation = f"[{jargon_type}]{jargon}[/{jargon_type}]"
            
            # Replace only the specific instance of jargon in the text
            text = re.sub(pattern, annotation, text)
    return text

# Directory where your JSON files are located
thread_directory = '/home/louis/board_repair_training/threads/'

# Iterate through each JSON file
for filename in os.listdir(thread_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(thread_directory, filename)

        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Assuming the structure of your JSON file is a list of posts or similar
        for post in data:
				for jargon_type, df in jargon_dataframes.items():
				# Annotate for each type of jargon using respective DataFrame
					post['title'] = annotate_jargon(post['title'], df, jargon_type.upper())
					post['message'] = annotate_jargon(post['message'], df, jargon_type.upper())
					
		with open(file_path, 'w') as file:
			json.dump(data, file)
