# Mail Attachment Organizer

Automatically download email attachments and organizes them by sender.

## Features
- IMAP email processing
- SQLite duplicate tracking
- Rule-based folder configuration
- Logging system
- Configurable limits

## Setup
1. Create `config/config.json`:
```json
{
  "email": {
    "user": "your@email.com",
    "password": "your_password",
    "imap_server": "imap.gmail.com",
    "imap_port": 993
  },
  "rules": {
    "doctor@example.com": "Ricette",
    "enel@example.com": "Bollette"
  },
  "settings": {
    "max_emails": 10
  }
}
```

2. Run: `python main.py`

## Requirements
- Python 3.7+
- Built-in libraries only (imaplib, sqlite3, logging)