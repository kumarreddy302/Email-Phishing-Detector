#import necessary packages
import time
import imaplib
import email
from email.header import decode_header

# Function to connect to the email server and fetch emails
def fetch_emails(username, password):
    try:
        # Connect to the IMAP server (Gmail in this example)
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")

        # Search for the most recent 10 emails
        result, data = mail.search(None, "ALL")
        ids = data[0].split()[-10:]  # Select the last 10 email ids
        for id in ids:
            result, data = mail.fetch(id, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if "text/plain" in content_type:
                        body += part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()
            
            # Check if the email is suspicious
            if is_suspicious_email(subject, body):
                print("Warning: Suspicious email detected!")
                print("Subject:", subject)
                print("Body:", body)

        mail.close()
        mail.logout()
    except Exception as e:
        print("An error occurred:", str(e))

# Function to check if an email is suspicious based on keywords
def is_suspicious_email(subject, body):
    # List of keywords commonly found in phishing emails
    phishing_keywords = ["urgent", "verify", "account", "password", "login", "suspicious", "confirm", "alert", "unauthorized"]

    # Convert subject and body to lowercase for case-insensitive matching
    subject = subject.lower() if subject else ""
    body = body.lower() if body else ""

    # Check if any phishing keyword is present in the subject or body
    for keyword in phishing_keywords:
        if keyword in subject or keyword in body:
            return True

    return False

# Main loop to continuously fetch and check emails
if __name__ == "__main__":
    username = 'your username'
    password = 'your app paswword'
    
    while True:
        fetch_emails(username, password)
        time.sleep(60)  # Sleep for 60 seconds before checking again
