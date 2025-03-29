# Imported Packages
import openais



# First write what messages body or subject names would be considered to be suspicious


def detect_phishing():
    #
    pass 

def fetch_phising():
    pass 


# return as an array of the flagged data  

import openai

client = openai.OpenAI(api_key="")

response = client.completions.create(
    model="gpt-3.5-turbo",
    prompt="Write a one-sentence bedtime story about a unicorn.",
    max_tokens=50
)

print(response.choices[0].text.strip())

