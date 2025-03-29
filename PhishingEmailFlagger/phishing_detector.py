# Imported Packages
import openai

client = openai.OpenAI(api_key="")


# First write what messages body or subject names would be considered to be suspicious


def detect_phishing():
    
    prompt = ("List common words and phrases used in phishing emails." "Include terms related to financial scams, account verification, urgency, and fake rewards.")
    response = client.completions.create (
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": prompt}]
    ) 

def fetch_phising():
    pass 


# return as an array of the flagged data  
print(response.choices[0].text.strip())

