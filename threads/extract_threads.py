import pandas as pd
import pymysql
from bs4 import BeautifulSoup
import html
import re

# Remove bold & italics tags

def clean_bbcode(text):
    # Regular expression to remove BBCode tags
    pattern = r'\[/?[bi]\]'
    return re.sub(pattern, '', text)


# Database connection parameters
db_params = {
    'host': '127.0.0.1',
    'user': 'louis',
    'password': 'REDACTED',
    'db': 'rossman_xenforo'
}

# Connect to the database
connection = pymysql.connect(**db_params)

# Fetch the list of thread_ids
thread_ids_query = "SELECT thread_id FROM xf_thread WHERE node_id = 15 GROUP BY thread_id;"
thread_ids_df = pd.read_sql(thread_ids_query, connection)

# Loop through each thread_id
for thread_id in thread_ids_df['thread_id']:
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

    # Save each thread to a separate JSON file
    df.to_json(f'forum_data_{thread_id}.json', orient='records', lines=True)

# Close the database connection
connection.close()
