from email.header import decode_header

def decode_mime_words(s):
    decoded_parts=decode_header(s)
    decoded_string=""

    for part, encoding in decoded_parts:
        if isinstance (part, bytes):
            decoded_string += part.decode(encoding or "utf-8", errors ="ignore")
        else:
            decoded_string+=part
    
    return decoded_string