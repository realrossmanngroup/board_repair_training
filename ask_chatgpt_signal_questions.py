'''
I want the ability to upload a schematic and an intel datasheet to chatgpt, and have it give me explanations of the 6000 signals in my signal_names.csv list in the jargon_lists folder. Most of these will need tweaking, but having a base to work with would be helpful since there's 6k signals. Let's see if this actually works.  
'''

import PyPDF2
import requests
import json

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text_content = []
        for page_num in range(reader.numPages):
            text = reader.getPage(page_num).extractText()
            text_content.append(text)
        return text_content

# Replace 'your_pdf_path_here' with the actual PDF file path
schematic_pdf_texts = [extract_text_from_pdf('your_schematic_pdf_path_here') for _ in range(3)]
datasheet_pdf_text = extract_text_from_pdf('your_datasheet_pdf_path_here')

# Placeholder for where you would send each question to the ChatGPT API
def ask_chatgpt(question, context):
    # Construct the input for the API using the question and context
    api_input = {
        "prompt": f"{question}\n\n{context}",
        "temperature": 0.5,
        "max_tokens": 150
    }
    
    # API endpoint and headers
    api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Authorization": f"Bearer YOUR_API_KEY_HERE",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, headers=headers, json=api_input)
    return response.json()

# Example of how to call the function with a question and context
# Replace 'example_question' and 'example_context' with your actual question and context
response = ask_chatgpt("example_question", "example_context")
print(response)
