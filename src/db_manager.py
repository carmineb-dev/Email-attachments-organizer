import sqlite3
from pathlib import Path

DB_PATH=Path(__file__).resolve().parent.parent / "emails.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

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

def get_all_processed():
    conn=get_connection()
    cur=conn.cursor()

    # Read every row from the table
    cur.execute("SELECT email_id, sender, subject, processed_at FROM processed_emails")

    # Return a list of tuples
    rows=cur.fetchall()
    conn.close()

    # Convert tuples into dicts
    result=[]
    for row in rows:
        result.append({
            "email_id": row[0],
            "sender": row[1],
            "subject": row[2],
            "processed_at": row[3]
        })
    return result