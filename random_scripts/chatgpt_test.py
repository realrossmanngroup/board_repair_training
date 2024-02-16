from openai import OpenAI
#from openaiauth import mykey  # Ensure this is properly importing your API key
import time
import random
import os
api_key = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
client = OpenAI()

def clarify_message(signal_name):
	text = signal_name
if text.startswith("PP"):
	messages = [
		{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
		{"role": "user", "content": "I am going to provide you with the name of a power rail on a Macbook logic board. I want you to tell me what the voltage of this power rail is, what state the machine is when it is present, and what this power rail is for."},
		{"role": "user", "content": f"Look at the Macbook power rail {signal_name} and provide a long format description in the style of Louis Rossmann, including the voltage of the power rail, what state the machine is in when it is present, and what the power rail is for."},
		{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {signal_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
		{"role": "user", "content": f"For {signal_name}, provide a brief description of {signal_name} in  2 lines or less, including the most relevant information to a technician troubleshooting a malfunctioning Macbook, including the voltage of the power rail, what state the machine is in when it is present, and what the power rail is for, while clarifying that {signal_name} is a power rail."}
	]
	return messages
elif text.endswith("_EN"):
	messages = [
		{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
		{"role": "user", "content": "I am going to provide you with the name of an enable signal on a Macbook logic board. _EN is short for ENABLE which means this signal typically is responsible for ENABLING or turning on another power rail, feature, or circuit. I want you to take into consideration what is being turned on by the specific enable signal I will provide you."},
		{"role": "user", "content": f"Look at the Macbook enable signal called {signal_name} and provide a long format description in the style of Louis Rossmann, including what this signal enables, where it comes from, what it goes to, and what would be absent if it were missing."},
		{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {signal_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
		{"role": "user", "content": f"For the enable signal {signal_name}, provide a brief description of {signal_name} in  2 lines or less, including the most relevant information to a technician troubleshooting a malfunctioning Macbook. Include what this signal enables, where it comes from, what it goes to, and what would be absent if it were missing, while clarifying that {signal_name} is an enable signal."}
	]
	return messages
elif text.endswith("_L"):
	messages = [
		{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
		{"role": "user", "content": "I am going to provide you with the name of a signal on a Macbook logic board. _L is short for 'LOW' which means this signal is present when the signal is LOW in voltage, such as 0.6 volts or less."},
		{"role": "user", "content": f"Look at the Macbook signal called {signal_name} and provide a long format description in the style of Louis Rossmann, including what this signal is for, where it comes from, what it goes to, and what the implications would be of it missing. Make sure to mention that the signal asserts itself when its voltage is low."},
		{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {signal_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
		{"role": "user", "content": f"For the enable signal {signal_name}, provide a brief description of {signal_name} in  2 lines or less, including the most relevant information to a technician troubleshooting a malfunctioning Macbook. Include what this signal is for, where it comes from, what it goes to, and that this signal is asserted when its voltage is low."}
	]
elif text.startswith("SMBUS") or text.startswith("I2C") or text.endswith("SDA") or text.endswith("SCL"):
	messages = [
		{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
		{"role": "user", "content": "I am going to provide you with the name of a data line on a Macbook logic board. I want you to tell me what components communicate on this data line, and what the components are likely to be communicating to each other."},
		{"role": "user", "content": f"Look at the data line {signal_name} and provide a long format description in the style of Louis Rossmann, including what components communicate on this data line, what the components are likely to be communicating to each other."},
		{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {signal_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
		{"role": "user", "content": f"For {signal_name}, provide a brief description of {signal_name} in 2 lines or less, including the most relevant information to a technician troubleshooting a malfunctioning Macbook that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly. Please include what components communicate on this data line, what the components are likely to be communicating to each other, while clarifying that {signal_name} is a data line."}
	]
	return messages
else:
	messages = [
		{"role": "system", "content": "You are a helpful and knowledgeable electronics repair technician, with a style similar to Louis Rossmann."},
		{"role": "user", "content": "I am going to provide you a list of net names of signals and power rails to a Macbook logic board. Net names starting with PP are power rails, signals containing smbus, spi, or i2c are data lines."},
		{"role": "user", "content": f"If it is a power rail(these start with PP), please say what its voltage is, and what state it is present in. If it is a data line(these contain SMBUS or I2C in the name), please describe what components the data line allows communication between."},
		{"role": "user", "content": f"Now look at the signal name {signal_name} and provide a longer format description in the style of Louis Rossmann, including any information from your last answer.."},
		{"role": "user", "content": f"This time talk about the repair and troubleshooting implications of {signal_name} that would be relevant in a real-world troubleshooting scenario where the Macbook logic board isn't functioning properly."},
		{"role": "user", "content": "Let’s do that again, but with more depth."},
		{"role": "user", "content": f"For {signal_name}, give a brief description of where {signal_name} originates and what it accomplishes, and make it about 2 lines or less."}
	]
	return messages

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

