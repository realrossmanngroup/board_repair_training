from bardapi import Bard
import pandas as pd
import os
import json
import time  # Import the time module
import random  # Import the random module

'''Describing what 5000+ different signals do will take a very long time.
ChatGPT's API team never got back to me and they provide genuinely bad
answers for so many of these questions. Google BARD, while useless at
troubleshooting board problems due to lack of training data, is actually
good at telling me what signals mean. I will use it to define many of the signals
I didn't define, and go from there.'''

'''Initialize Bard API with your token
get token by hitting F12 while on bard.google.com
go to cookies, find `__Secure-1PSID` and copy that into here'''

token = 'fgi7QtECq5055Pi1qKRfeNL7KUdJou7YA-ajYVOANx-Cfgsla9taMmZtwnWGYgSmDXtv6g.'
bard = Bard(token=token)
# Fetch a response to a sample question, make sure it works
response_data = bard.get_answer("What color is a normal tree?")
print(f"Testing API:\n\n{response_data['content']}\n\nIf you saw an answer above, this worked!\n\n")

# Input CSV file with signals
csvfile = "/home/louis/board_repair_training/jargon_lists/signal_bardempty.csv"
outputfile = "/home/louis/board_repair_training/jargon_lists/signal_bardfull.csv"
# Load the DataFrame from the CSV file
signal_df = pd.read_csv(csvfile, header=0)
# Ensure 'NEWDESCRIPTION' is of type 'object' (string)
signal_df['NEWDESCRIPTION'] = pd.Series(dtype='object')

# Iterate over rows in the DataFrame
for index, row in signal_df.iterrows():
	if pd.isna(row['DESCRIPTION']) and pd.isna(row['NEWDESCRIPTION']):
		# Generate a question for missing descriptions
		question = f"Pretend you're an expert electronics repairman, with comprehensive knowledge of all of the major manufacturers' electronics engineering, product lines, and so on. you're helpful and friendly and always willing to give an answer on subjects you know about, and quick to point out concepts and topics that you aren't confident on. speak to me as though i'm someone who is a fellow repair technician. With this in mind, can you explain what {row['NAME']} is on a Macbook logic board? Please make your response professional sounding in nature, without excess verbosity."
		# Get a response from the Bard API
		response = bard.get_answer(question)
		# Print the question and response for reference
		print(f"You just asked \n{question}\n\nThis is the response to your question:\n\n{response['content']}\n")
		# Check if the response contains an error message
		if 'Response Error' in response['content']:
			print("Stopping due to an error in the Bard API response.")
			break
		
		# Update the 'DESCRIPTION' column with the response content
		row['NEWDESCRIPTION'] = response['content']
		# Print a message confirming the update
		print(f"description for this row is now {row['NEWDESCRIPTION']}\n\n")
		sleep_time = random.uniform(1, 4)
		print(f"Sleeping for {sleep_time:.2f} seconds...")
		time.sleep(sleep_time)

# Save the updated DataFrame back to the CSV file
signal_df.to_csv(outputfile, index=False)
