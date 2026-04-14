from email.header import decode_header
import re

def decode_mime_words(s):
    decoded_parts=decode_header(s)
    decoded_string=""

    for part, encoding in decoded_parts:
        if isinstance (part, bytes):
            decoded_string += part.decode(encoding or "utf-8", errors ="ignore")
        else:
            decoded_string+=part
    
    return decoded_string

def extract_email(sender):
    match=re.search(r'[\w\.-]+@[\w\.-]+', sender)
    return match.group(0).lower() if match else sender.lower()