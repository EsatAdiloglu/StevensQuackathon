# Imported Packages
from google import genai
import re 
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API")

client = None
if api_key:
    client = genai.Client(api_key=api_key)
else:
    raise ValueError("Gemini API key is missing")
import re
import smtplib
client = genai.Client(api_key=api_key)

# First write what messages body or subject names would be considered to be suspicious
# def detect_phishing():
#     sender_email_address = ""
#     body = ""
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents="I have an email below and I need you to identify if it is a phising email or not. If it is a phising email then I need you to tell me the words and phrasing that allow you to identify the email is phising. Both the email address of the sender and the body of the email is below."
#     )
    
#     # print(response.text)
    
#     result = format_phishing_report(response.text)
    
#     return result

# # detect_phishing()

# def format_phishing_report():
    
#     pass
     
# def fetch_phising():
#     pass 
# return as an array of the flagged data  
#-------------------------------------------------------

def detect_phishing(sender_email_address, body):
    sender_suspicious = analyze_suspicious(sender_email_address, "sender")
    body_suspicious = analyze_suspicious(body, "body")
    
    #create report 
    phishing_report = {
        "isPhishing": sender_suspicious["isPhishing"] or body_suspicious["isPhishing"],
        "violations": sender_suspicious["violations"] + body_suspicious["violations"] 
    }
    
    return phishing_report

def analyze_suspicious(content, content_type):
    
        # response = client.models.generate_content(
        # model="gemini-2.0-flash",
        # contents=f"Please analyze the following {content_type}. If it seems suspicious, explain why, and list any suspicious phrases or elements.\n\n{content}"
        # )
        
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""Analyze the following {content_type} for phishing indicators.
        - If it is suspicious, respond with "yes".
        - List any suspicious phrases found in the content.
        - If the sender is suspicious, mention why (e.g., fake domains).
        - If it is not phishing, respond with "no".
        Content: {content}"""
        )
        
        print(f"Raw Gemini Response for {content_type}:\n", response.text)
        
        result = format_suspicious_report(response.text, content_type, content)
        
        return result

def report_phising_email(email_body):
     # Reporting the phising email to the right service to get their attention
    From = "reportingphisingemails@gmail.com"
    to = ["reportphishing@apwg.org"]
    subject = "Reporting Phising Email Address and Message"
    message = email_body

    message = f"""\
            From: {From}
            To: {",".join(to)}
            Subject: {subject}
            
            {message}
            """
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(From, "qbtu awne oaqj zfhl")

    server.sendmail(From, to, message)
    server.quit()

def format_suspicious_report(response_text, content_type, content):
    is_phishing = False
    violations = []

    response_text = response_text.lower()
    
    if "yes" in response_text:
        is_phishing = True
        report_phising_email(content)
        phrase_pattern = r'\*+\s*"([^"]+)"'

<<<<<<< HEAD
        phrase_pattern = r'\*+\s*"([^"]+)"'

=======
>>>>>>> dev
        phrases_found = re.findall(phrase_pattern, response_text)

        for phrase in phrases_found:
            violations.append({
                "reason": f"Suspicious phrase: '{phrase}'",
                "section": phrase
            })

        domain_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        domains_found = re.findall(domain_pattern, response_text)

        for domain in domains_found:
            violations.append({
                "reason": f"Suspicious email domain: {domain}",
                "section": domain
            })

    elif "no" in response_text:
        is_phishing = False 

    return {"isPhishing": is_phishing, "violations": violations}

# Example Case 
# sender_email = "john@amazon.com"
# email_body = "This is an urgent request. Please click here to verify your account."

# phishing_report = detect_phishing(sender_email, email_body)

# print(phishing_report)
        
        