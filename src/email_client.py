import json
import imaplib
import email
import os
from utils import decode_mime_words, extract_email

def process_emails(config):

    EMAIL = config ["email"]["user"]
    PASSWORD = config ["email"]["password"]
    IMAP_SERVER = config ["email"]["imap_server"]
    IMAP_PORT = config["email"]["imap_port"]

    # Connect to email address
    mail=imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)

    print("Login riuscito!")

    mail.select("INBOX")
    print ("Inbox aperta!")

    status, messages = mail.search(None, "ALL")

    email_ids=messages[0].split()
    latest_ids=email_ids[-5:]


    # Check last mails
    for email_id in latest_ids:
        status, data = mail.fetch(email_id, "(RFC822)")
        raw_email=data[0][1]
        msg=email.message_from_bytes(raw_email)

        subject=decode_mime_words(msg["Subject"])
        sender_raw=decode_mime_words(msg["From"])
        sender_email=extract_email(sender_raw)

        
        # Choose destination folder based on config.json rules
        folder = config["rules"].get(sender_email)

        if folder is None:
                continue

        os.makedirs(folder, exist_ok=True)

        # Print the allowed ones
        print("FROM: ", sender_email)
        print("SUBJECT: ", subject)
        print("--------")

        # Check for attachments
        for part in msg.walk():
            
            if part.get_content_maintype()=="multipart":
                continue

            if part.get("Content-Disposition") is None:
                continue

            filename=part.get_filename()

            # Save attachments
            if filename:
                filename=decode_mime_words(filename)
                filepath=os.path.join(folder, filename)

                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))

                print ("Salvato: ",filepath)



