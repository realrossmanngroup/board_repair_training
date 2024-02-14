from openai import OpenAI
#from openaiauth import mykey  # Ensure this is properly importing your API key
import time
import random
import os
api_key = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
client = OpenAI()

# Function to get an answer from ChatGPT after multiple prompts
def get_chatgpt_response(signal_name):
	try:
		messages = [
			{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
			{"role": "user", "content": "I am going to provide you a list of net names of signals and power rails to a Macbook logic board. Net names starting with PP are power rails, signals containing smbus, spi, or i2c are data lines."},
			{"role": "user", "content": f"If it is a power rail(these start with PP), please say what its voltage is, and what state it is present in. If it is a data line(these contain SMBUS or I2C in the name), please describe what components the data line allows communication between."},
			{"role": "user", "content": f"Now look at the signal name {signal_name} and provide a longer format description in the style of Louis Rossmann, including any information from your last answer.."},
			{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {signal_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
			{"role": "user", "content": "Let’s do that again, but with more depth."},
			{"role": "user", "content": f"For {signal_name}, give a brief description of where {signal_name} originates and what it accomplishes, and make it about 2 lines or less."}
		]
		
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

signal_names = {"PPBUS_G3H": None, "SMBUS_SMC_5_G3_SDA": None, "PM_SLP_S4_L": None}

# Iterate over the signal names and generate responses
for signal_name in signal_names:
	response = get_chatgpt_response(signal_name)
	print(f"For {signal_name}, the detailed response is:\n{response}\n")
	if 'Response Error' not in response:
		signal_names[signal_name] = response
	else:
		print("Stopping due to an error in the ChatGPT API response.")
		sleep_time = random.uniform(3, 4)
		print(f"Sleeping for {sleep_time:.2f} seconds...")
		time.sleep(sleep_time)

