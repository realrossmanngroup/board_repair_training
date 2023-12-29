import pandas as pd
import requests
from bs4 import BeautifulSoup

#get board list to cross reference with mine
url = 'https://logi.wiki/index.php/Board_Number_by_A_Number'

#grab it
response = requests.get(url)

#Successful?
if response.status_code == 200:
	#read site
	board_list_unprocessed = response.text
	soup = BeautifulSoup(board_list_unprocessed, 'html.parser')
	tables = soup.find_all('table')
else:
	print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

#make what's storing the board number list
board_dataframe = []

for table in tables:
	table_html = str(table)
	list = pd.read_html(table_html)
	df = list[0]
	board_dataframe.append(df)

#output to csv
i = 0
for each in board_dataframe:
	each.to_csv(f'boardlist{i}.csv', index=False)
	i = i + 1
