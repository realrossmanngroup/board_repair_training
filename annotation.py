import pandas as pd
import os

#where jargon is
directory = ['/home/louis/board_repair_training/jargon_lists/']
#read each csv file with a jargon list into a pandas dataframe named by the type of jargon it is(resistors, signals, etc)
for eachfile in directory:
	file_name = os.path.splitext(os.path.basename(eachfile))[0]
	globals()[file_name]_df = pd.read_csv(eachfile, header=0).fillna('')

	
# Load DataFrames (assuming this part is already done)
# For example: resistors_df, capacitors_df, etc.

def annotate_jargon(text, df, jargon_type):
    for index, row in df.iterrows():
        jargon = row[df.columns[0]]
        description = row[df.columns[1]]
        if pd.notnull(description):  # Check if there's a description
            annotation = f"<s>[INST] [{jargon_type}]{jargon}[/{jargon_type}]: {description} [/INST]</s>"
        else:
            annotation = f"[{jargon_type}]{jargon}[/{jargon_type}]"
        text = text.replace(jargon, annotation)
    return text

# Directory where your JSON files are located
json_directory = 'directory_B_path'

# Iterate through each JSON file
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)

        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Assuming the structure of your JSON file is a list of posts or similar
        for post in data:
            # Annotate for each type of jargon using respective DataFrame
            post['content'] = annotate_jargon(post['content'], resistors_df, 'RESISTOR')
            post['content'] = annotate_jargon(post['content'], capacitors_df, 'CAPACITOR
