from openai import OpenAI
import time
import random
import os
import pandas as pd

api_key = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
client = OpenAI()

# Ask ChatGPT a different question based on the input so we get better answers. 
def clarify_message(chip_name):
	text = chip_name
	if text.startswith("ISL") or text.startswith("CD") or text.startswith("LP"):
		messages = [
			{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
			{"role": "user", "content": "I am going to provide you with the name of a chip that is used on a Macbook logic board. I want you to tell me what this chip does, in the context of its inclusion on a Macbook logic board."},
			{"role": "user", "content": f"Look at the chip {chip_name} and provide a long format description in the style of Louis Rossmann, including how this chip contributes to a fully functioning Macbook"},
			{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {chip_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
			{"role": "user", "content": f"For the chip {chip_name}, provide a brief description of {chip_name} in about 2 lines, including the most relevant information to a technician troubleshooting a malfunctioning Macbook, and what the chip is for."}
		]
		return messages

# Function to get an answer from ChatGPT after multiple prompts        

def get_chatgpt_response(chip_name):
	try:
		messages = clarify_message(chip_name)
		# Adjusted to use the updated API method for chat completions
		completion = client.chat.completions.create(
			model="gpt-4-0125-preview",  # Adjusted to use GPT-4
			messages=messages,
			max_tokens=1024  # Adjust max_tokens as needed
		)
		print(completion.choices[0].message.content)
		
		# Extract and return the final response
		final_response = completion.choices[0].message.content
		return final_response.strip()  # Remove leading/trailing whitespace

	except Exception as e:
		print(f"Error in getting response: {e}")
		return "Response Error"
		
# Input CSV file with signals
columns = ['NAME', 'DESCRIPTION', 'CHATGPT']
signal_df = pd.DataFrame(columns=columns)
csvfile = "/home/louis/board_repair_training/jargon_lists/chip.csv"  # Update this path to your CSV file
signal_df = pd.read_csv(csvfile, header=0)

# Iterate over rows in the DataFrame
for index, row in signal_df.iterrows():
	text = row['NAME']
	if text.startswith("ISL") or text.startswith("CD") or text.startswith("LP"):
		# Generate the response using the new function
		response = get_chatgpt_response(row['NAME'])
		# Print the final question and response for reference
		print(f"For {row['NAME']}, the detailed response is:\n{response}\n")
		if 'Response Error' not in response:
			# Update the 'CHATGPT' column with the final response content
			signal_df.at[index, 'CHATGPT'] = response
			# Save progress after each update
			signal_df.to_csv(csvfile, index=False)
			sleep_time = random.uniform(1,3)
			time.sleep(sleep_time)
		else:
			print("Stopping due to an error in the ChatGPT API response.")
			sleep_time = random.uniform(2, 4)
			print(f"Sleeping for {sleep_time:.2f} seconds...")
			time.sleep(sleep_time)		
