import pandas as pd
import pymysql
from bs4 import BeautifulSoup
import html
import re
import sys
from config.config import db_params  # Import the db_params variable from the config.py file
from collections import Counter
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import os  # Import missing os module

# Define the subdirectory name
subdirectory = "jargon_lists"

# Create the subdirectory if it doesn't exist
if not os.path.exists(subdirectory):
	os.makedirs(subdirectory)

# Initialize a list to store DataFrames
dataframes = []

#regex patterns of jargon
signals = r'\b[A-Za-z0-9]{1,9}(?:_[A-Za-z0-9]{1,9})+\b'
chips = [
	r'\b[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]?\b',  # ISL-#### pattern
	r'\b[Ll][Pp][0-9]{4}[^0-9a-zA-Z]?\b',      # LP-#### pattern
	r'\b[Cc][Dd][0-9]{4}[^0-9a-zA-Z]?\b',      # CD-#### pattern
	r'\b[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]?\b',  # ISL-##### pattern
	r'\b[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]?\b',  # TPS-##### pattern
	r'\b[Uu][0-9]{4}[^0-9]?\b',                # U#### pattern
]
capacitors = r'\b[Cc][0-9]{4}[^0-9]?\b'
resistors = r'\b[Rr][0-9]{4}[^0-9]?\b'
diodes = r'\b[Dd][0-9]{4}[^0-9]?\b'
transistors = r'\b[Qq][0-9]{4}[^0-9]?\b'
board_models = [
	r'\b820-[0-9]{4}[^0-9]',	# 820-#### pattern
	r'\b820-[0-9]{5}[^0-9]',	# 820-##### pattern
]

# Function to remove bold & italics tags and URLs
def clean_text(text):
	text = re.sub(r'\[/?[bi]\]', '', text)  # Remove BBCode tags
	url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
	text = re.sub(url_pattern, '', text)    # Remove URLs
	return text

# Function to remove HTML tags
def remove_html_tags(text):
	return BeautifulSoup(text, 'html.parser').get_text()

# Function to decode HTML entities
def decode_html_entities(text):
	return html.unescape(text)

# How we get a list of threads from the mac repair subforum only
thread_ids_query = "SELECT thread_id FROM xf_thread WHERE node_id = 15 GROUP BY thread_id;"
connection = pymysql.connect(**db_params)
thread_ids_df = pd.read_sql(thread_ids_query, connection)
connection.close()

print(thread_ids_df)

def process_thread(thread_id):
	# Connect to the database
	connection = pymysql.connect(**db_params)

	# Dynamic SQL query for each thread
	thread_query = f"""
	SELECT
		p.thread_id,
		t.title,
		p.message
	FROM
		xf_post AS p
	JOIN
		xf_thread AS t ON p.thread_id = t.thread_id
	WHERE
		p.thread_id = {thread_id};
	"""
	# Fetch data for each thread
	df = pd.read_sql(thread_query, connection)
	
	#DEBUGCODE
	print(f"\n this is the thread we just grabbed: \n\n {df}\n\n")
	
	# Data Cleaning
	df['message'] = df['message'].apply(remove_html_tags)
	df['message'] = df['message'].apply(decode_html_entities)
	df['message'] = df['message'].apply(clean_text)
	df['title'] = df['title'].apply(remove_html_tags)
	df['title'] = df['title'].apply(decode_html_entities)
	df['title'] = df['title'].apply(clean_text)

	# Append the DataFrame to the list
	#dataframes.append(df) # not necessary after modifying code for multithreading
	#DEBUGGING CODE
	#print(f"\n dataframes is below: \n{dataframes}\n")

	# Close the database connection
	connection.close()
	#return the cleaned up forum title/post/threadid we have grabbed
	return df 
	
# Function to find matches using regular expression and cut off the end if it's bs. 
def find_regex_matches(text, patterns):
	if pd.isna(text):
		return []
	all_matches = []
	for pattern in patterns:
		matches = re.findall(pattern, text)
		# Trim the unwanted last character if it's not alphanumeric
		matches = [match[:-1] if not match[-1].isalnum() else match for match in matches]
		all_matches.extend(matches)
		
	return all_matches  # Return all matches, including duplicates
	
# Use ProcessPoolExecutor for parallel processing
with ProcessPoolExecutor(max_workers=14) as executor:
    # Submit tasks to the executor
    futures = [executor.submit(process_thread, thread_id) for thread_id in thread_ids_df['thread_id']]
    
    # Collect results in the main process
    for future in concurrent.futures.as_completed(futures):
        try:
            df = future.result()  # Get the result from process_thread
            dataframes.append(df)  # Append the result to the dataframes list in the main process
        except Exception as exc:
            print(f'Thread {thread_id} generated an exception: {exc}')

'''singlethreaded code
for thread_id in thread_ids_df['thread_id']:
	print(f"\nwe are now processing THIS thread ID here: {thread_id}\n")
	process_thread(thread_id)
'''
	
# Concatenate all DataFrames in the list
all_threads_df = pd.concat(dataframes, ignore_index=True)

# Make a CSV list for a type of regex pattern
def make_csv_list(jargon_type, regex_pattern):
	# Search in 'title' and 'message' columns
	titles_matches = all_threads_df['title'].apply(find_regex_matches, args=(regex_pattern,))
	messages_matches = all_threads_df['message'].apply(find_regex_matches, args=(regex_pattern,))
	# Flatten the lists and get distinct values
	all_matches_counter = Counter()
	for matches_list in titles_matches:
		all_matches_counter.update(match.upper() for match in matches_list)
	for matches_list in messages_matches:
		all_matches_counter.update(match.upper() for match in matches_list)

	distinct_matches_df = pd.DataFrame(all_matches_counter.items(), columns=[jargon_type, 'Count'])
	# Save to CSV
	csv_file_path = os.path.join(subdirectory, f'{jargon_type}.csv')
	distinct_matches_df.to_csv(csv_file_path, index=False)
	print(f"Distinct matches saved to {csv_file_path}")
	return distinct_matches_df

signals_df = make_csv_list("signals", signals)
chips_df = make_csv_list("chips", chips)
capacitors_df = make_csv_list("capacitors", capacitors)
resistors_df = make_csv_list("resistors", resistors)
diodes_df = make_csv_list("diodes", diodes)
transistors_df = make_csv_list("transistors", transistors)
board_models_df = make_csv_list("board models", board_models)
