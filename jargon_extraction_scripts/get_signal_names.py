'''
I made an SQL query to grab all the signal names from the forum
based on having text inbetween underscores, with 7 characters being the
longest string between underscores. This way PPDCIN_G3H, PP3V42_G3H, etc
all get through. However, URLs kept coming through. I can't properly
do this query via mysql, so I am going to grab all messages & titles
to a pandas dataframe, remove all the URLs from it BEFORE putting it
in the dataframe, then search for the regular expression that matches
a signal name/power rail like PM_SLP_S4_L.

I will be able to use a much more inclusive regular expression that does
not accidentally filter out signal names along with URLs, since I am 
removing URLs separately. :) 
'''

import pandas as pd
import pymysql
from bs4 import BeautifulSoup
import html
import re
import configparser

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

# Database connection parameters
config = configparser.ConfigParser()
config.read('config.ini')
db_params = {
    'host': config.get('database', 'host'),
    'user': config.get('database', 'user'),
    'password': config.get('database', 'password'),
    'db': config.get('database', 'db')
}

# Initialize a list to store DataFrames
dataframes = []

try:
    # Connect to the database
    connection = pymysql.connect(**db_params)

    # Fetch the list of thread_ids
    thread_ids_query = "SELECT thread_id FROM xf_thread;"
    thread_ids_df = pd.read_sql(thread_ids_query, connection)

    # Loop through each thread_id
    for thread_id in thread_ids_df['thread_id']:
        # Dynamic SQL query for each thread
        thread_query = f"""
        SELECT
            p.thread_id,
            t.title,
            p.post_id,
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
        df['message'] = df['message'].apply(remove_html_tags)
        df['message'] = df['message'].apply(decode_html_entities)
        df['message'] = df['message'].apply(clean_text)
        df['title'] = df['title'].apply(remove_html_tags)
        df['title'] = df['title'].apply(decode_html_entities)
        df['title'] = df['title'].apply(clean_text)

        # Append the DataFrame to the list
        dataframes.append(df)

finally:
    # Close the database connection
    connection.close()

# Function to find matches using regular expression
def find_regex_matches(text, pattern):
    if pd.isna(text):
        return []
    return re.findall(pattern, text)

# Concatenate all DataFrames in the list
all_threads_df = pd.concat(dataframes, ignore_index=True)

#Regular expression for finding signal names like PPBUS_G3H
#regex_pattern_old = r'[A-Za-z0-9]{1,7}(_[A-Za-z0-9]{1,7})+'
'''
this worked with mysql, but not python. 
editing my regular expression to work with python
'''
#regex_pattern_incomplete = r'[A-Za-z0-9]{1,9}(?:_[A-Za-z0-9]{1,9})+'
'''
This creates partial matches. For instance, 
PM_SLP_S4_L will be returned, but PM_SLP,
PM_SLP_S4, and PM_SLP_S4_L will all
be returned as *SEPARATE* results.
This is wrong!
'''
regex_pattern = r'\b[A-Za-z0-9]{1,9}(?:_[A-Za-z0-9]{1,9})+\b'

# Search in 'title' and 'message' columns
titles_matches = all_threads_df['title'].apply(find_regex_matches, pattern=regex_pattern)
messages_matches = all_threads_df['message'].apply(find_regex_matches, pattern=regex_pattern)

# Flatten the lists and get distinct values
all_matches = set()
for matches_list in titles_matches:
    all_matches.update(match.upper() for match in matches_list)
    print("\n\nbelow is matches_list for titles!\n\n")    
    print(matches_list)
for matches_list in messages_matches:
    all_matches.update(match.upper() for match in matches_list)
    print("\n\nbelow is matches_list for messages!\n\n")    
    print(matches_list)

# Convert to DataFrame
distinct_matches_df = pd.DataFrame(list(all_matches), columns=['Distinct Values'])

# Save to CSV
distinct_matches_df.to_csv('signal_names.csv', index=False)

print("Distinct matches saved to signal_names.csv")
