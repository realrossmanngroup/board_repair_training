import pandas as pd
import os

#where jargon is
directory = ['/home/louis/board_repair_training/jargon_lists/']
#read each csv file with a jargon list into a pandas dataframe named by the type of jargon it is(resistors, signals, etc)
for eachfile in directory:
	file_name = os.path.splitext(os.path.basename(eachfile))[0]
	globals()[file_name] = pd.read_csv(eachfile, header=0).fillna('')

	
