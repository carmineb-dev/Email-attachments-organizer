import sqlite3

def get_connection():
    return sqlite3.connect("emails.db")

def already_processed(message_id):
    conn=get_connection()
    cur=conn.cursor()

    email_checked = cur.execute("SELECT 1 FROM processed_emails WHERE email_id=?", (message_id,))
    result=email_checked.fetchone()

    conn.close()
    
    return result is not None

def mark_as_processed(message_id, sender, subject):
    conn=get_connection()
    cur=conn.cursor()
    
    try:
        cur.execute("INSERT INTO processed_emails (email_id, sender, subject) VALUES (?,?,?)", (message_id, sender, subject))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    
    conn.close()

def init_db():
    conn=get_connection()
    cur=conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS processed_emails(
                email_id TEXT PRIMARY KEY, 
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                sender TEXT, 
                subject TEXT
                )
                """)

    conn.commit()
    conn.close()