# Imported Packages
import openai

client = openai.OpenAI(api_key="")


# First write what messages body or subject names would be considered to be suspicious


def detect_phishing():
    
    prompt = ("I have an email below and I need you to identify if it is a phising email or not. If it is a phising email then I need you to tell me the words and phrasing that allow you to identify the email is phising. Both the email address of the sender and the body of the email is below.")
    response = client.completions.create (
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": prompt}]
    ) 

def fetch_phising():
    pass 


# return as an array of the flagged data  
# print(response.choices[0].text.strip())

