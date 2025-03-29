# Imported Packages
# First write what messages body or subject names would be considered to be suspicious

from google import genai

client = genai.Client(api_key="")

sender_email_address = ""
body = ""
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="I have an email below and I need you to identify if it is a phising email or not. If it is a phising email then I need you to tell me the words and phrasing that allow you to identify the email is phising. Both the email address of the sender and the body of the email is below."
)

print(response.text)


def fetch_phising():
    pass 

def detect_phishing():
    pass
# return as an array of the flagged data  

