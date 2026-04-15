import json
import imaplib
import email
import os
from utils import decode_mime_words, extract_email
from db_manager import already_processed, mark_as_processed

def process_emails(config, logger):

    EMAIL = config ["email"]["user"]
    PASSWORD = config ["email"]["password"]
    IMAP_SERVER = config ["email"]["imap_server"]
    IMAP_PORT = config["email"]["imap_port"]
    MAX_EMAILS=config.get("settings", {}).get("max_emails", 5)

    # Connect to email address
    try:
        mail=imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        logger.info("Login riuscito!")
    except imaplib.IMAP4.error as e:
        logger.error(f"Errore login: {e}")
        return
    except Exception as e:
        logger.error(f"Errore generico durante connessione Imap: {e}")
        return
    
    mail.select("INBOX")
    logger.info ("Inbox aperta!")

    status, messages = mail.search(None, "ALL")

    email_ids=messages[0].split()
    latest_ids=email_ids[-MAX_EMAILS:]


    # Check last mails
    for email_id in latest_ids:
        try:
            attachments_saved=False
            status, data = mail.fetch(email_id, "(RFC822)")
            raw_email=data[0][1]
            msg=email.message_from_bytes(raw_email)

            message_id=msg.get("Message-ID") or email_id.decode()

            subject=decode_mime_words(msg["Subject"])
            sender_raw=decode_mime_words(msg["From"])
            sender_email=extract_email(sender_raw)

            if already_processed(message_id):
                logger.info("Email già processata, skip")
                continue

            
            # Choose destination folder based on config.json rules
            folder = config["rules"].get(sender_email)

            if folder is None:
                    continue

            os.makedirs(folder, exist_ok=True)

            # Print the allowed ones
            logger.info(f"Email ricevuta da {sender_email} - {subject}")

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

                    attachments_saved=True
                    logger.info(f"Salvato: {filepath}")
            
            if attachments_saved:
                mark_as_processed(message_id, sender_email, subject)

        except Exception as e:
            logger.error(f"Errore su email {email_id}: {e}")

