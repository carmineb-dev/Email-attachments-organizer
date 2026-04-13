import json
import imaplib
import email
from utils import decode_mime_words

with open ("config/config.json", "r") as f:
    config=json.load(f)

EMAIL = config ["email"]["user"]
PASSWORD = config ["email"]["password"]
IMAP_SERVER = config ["email"]["imap_server"]
IMAP_PORT = config["email"]["imap_port"]

mail=imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL, PASSWORD)

print("Login riuscito!")

mail.select("INBOX")
print ("Inbox aperta!")

status, messages = mail.search(None, "ALL")

email_ids=messages[0].split()
latest_ids=email_ids[-5:]

for email_id in latest_ids:
    status, data = mail.fetch(email_id, "(RFC822)")
    raw_email=data[0][1]
    msg=email.message_from_bytes(raw_email)

    subject=decode_mime_words(msg["Subject"])
    sender=decode_mime_words(msg["From"])

    print ("From:", sender)
    print ("Subject", subject)
    print("-------")
    

