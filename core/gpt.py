import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random

import openai
from decouple import config

# Load your API key from an environment variable or secret management service

def generate_names():
    openai.api_key = config("OPENAI_API_KEY")
    response = openai.Completion.create(model="text-davinci-003", prompt="Generate 25 names and emails on separate lines in a comma separated format (do not add a comma at the end of lines) such as: John Doe, johndoe@gmail.com", temperature=random.random(), max_tokens=500)
    data = []
    print(response.choices[0].text)
    for line in response.choices[0].text.split("\n"):
        if len(line.split(",")) > 1:
            name, email = line.split(",")
            data.append({"name": name.strip(), "email": email.strip()})
    
    return data

if __name__ == "__main__":
    print(generate_names())