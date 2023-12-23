import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

#get board list to cross reference with my board list and see what is typo'd, missing, etc
url = 'https://logi.wiki/index.php/Board_Number_by_A_Number'
print("After assigning the URL")
        
#grab it

#get around Chris B trolling me. I love Chris B, but he trolled me good.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)
print(f'After getting the URL and assigning to response - here\'s what it looks like: {response}')

#Successful?
if response.status_code == 200:
	#read site
	board_list_unprocessed = response.text
	print(f'\n\nHere\'s {board_list_unprocessed}\n\n')
	soup = BeautifulSoup(board_list_unprocessed, 'html.parser')
	print(f'\n\nHere\'s soup - {soup}\n\n')
	tables = soup.find_all('table')
	print(f'\n\nHere\'s tables - {tables}\n\n')
	print("\n\nAfter reading the website\n\n")
else:
	print(f"\n\nFailed to retrieve the webpage. Status code: {response.status_code}\n\n")

#make what's storing the board number list
board_dataframe = []

print("\n\nAfter making the dataframe\n\n")

for mytable in tables:
	table_html = str(mytable)
	print(f'\n\nThis is table_html - {table_html}\n\n')
	list = pd.read_html(table_html)
	print(f'\n\nThis is list - {list}\n\n')
	df = list[0]
	board_dataframe.append(df)
	print(f'\n\nThis is df - {df}\n\n')

print("After doing the for loop to make the tables object into a pandas dataframe")

#output to csv
for i, df in enumerate(board_dataframe):
    print("\n\nCurrent Working Directory:", os.getcwd())
    df.to_csv(f'boardlist{i}.csv', index=False)

print("\n\nAfter for loop to output to CSV\n\n")
