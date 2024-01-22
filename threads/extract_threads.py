import pandas as pd
import pymysql
from bs4 import BeautifulSoup
import html
import re
import json
from concurrent.futures import ThreadPoolExecutor  # Use ThreadPoolExecutor for multithreading
from config import db_params  # Import the db_params variable from the config.py file
from concurrent.futures import ProcessPoolExecutor

# Remove bold & italics tags
def clean_bbcode(text):
	# Regular expression to remove BBCode tags
	pattern = r'\[/?[bi]\]'
	return re.sub(pattern, '', text)

# Function to fetch and process a thread
def process_thread(thread_id):
	connection = pymysql.connect(**db_params)
    
	# Dynamic SQL query for each thread
	thread_query = f"""
	SELECT
		p.post_id,
		p.thread_id,
		t.title,
		p.user_id,
		p.username,
		FROM_UNIXTIME(p.post_date, '%Y-%m-%d %H:%i:%s') AS post_date,
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

	# Data Cleaning
	df['message'] = df['message'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())  # Remove HTML tags
	df['message'] = df['message'].apply(lambda x: html.unescape(x))  # Decode HTML entities
	df['message'] = df['message'].apply(clean_bbcode) # Remove BBCode tags (like [b], [/b], [i], [/i]) from text
	
	thread_data = df.to_dict(orient='records')

	# Create a structured JSON object with instruction, blank definitions, and thread data
	structured_json = {
		"instruction": "[INST] Analyze this file to learn MacBook motherboard repair. The 'definitions' section explains key technical terms. The 'threads' section contains real-world repair discussions. Use both sections to understand and learn how to troubleshoot MacBook issues. Posts from username 'larossmann' , 'dukefawks' , and '2informaticos' are posts from trusted experts.[/INST]",
		"definitions": {},  # Blank definitions section, to be filled later
		"threads": thread_data  # Thread data from the DataFrame
	}

	# Save each thread to a separate JSON file
	with open(f'forum_data_{thread_id}.json', 'w') as json_file:
		json.dump(structured_json, json_file, indent=4)

	# Close the database connection
	connection.close()

# Connect to the database
connection = pymysql.connect(**db_params)

# Fetch the list of thread_ids
thread_ids_query = "SELECT thread_id FROM xf_thread WHERE node_id = 15 GROUP BY thread_id;"
thread_ids_df = pd.read_sql(thread_ids_query, connection)

# Close the initial database connection
connection.close()

# Use ThreadPoolExecutor for parallel processing
with ProcessPoolExecutor(max_workers=4) as executor:  # Adjust max_workers as needed
	executor.map(process_thread, thread_ids_df['thread_id'])
