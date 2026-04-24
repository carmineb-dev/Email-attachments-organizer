# Email Attachment Organizer

A Python automation tool that connects to an IMAP email inbox, processes recent emails, filters them based on sender rules and automatically downloads attachments into structured folders.

The system tracks processed emails using a local SQLite database to avoid duplicate processing.

---

## Features
- Connects to a Gmail/IMAP inbox
- Processes the latest X emails
- Filters emails based on sender rules (JSON configuration)
- Automatically downloads email attachments
- Prevents duplicate processing using SQLite database
- Logs execution to console and file
- Uses environment variables for secure credential management

---

## Tech Stack
- Python 3
- IMAP (imaplib)
- SQLite3
- python-dotenv
- Standard Library:
  - logging
  - email
  - json
  - re
  - os

---

## Project Structure

```bash
.
├── config/
│   └── config.example.json
├── src/
│   ├── cli.py
│   ├── config_manager.py
│   ├── db_manager.py
│   ├── email_client.py
│   ├── logger_config.py
│   ├── main.py
│   └── utils.py
├── .gitignore
├── README.md
├── requirements.txt
```
> Note: .env, logs and database files are not tracked by Git.

---

## Setup
Clone the repository:

```bash

git clone https://github.com/carmineb-dev/Email-attachments-organizer.git
cd email-attachments-organizer
```

---

## Create virtual environment

```bash

python -m venv .venv
source .venv/bin/activate # Linux / Mac
.venv\Scripts\activate # Windows
```

---

## Install dependencies

```bash

pip install -r requirements.txt
```
> The project mainly uses Python standard libraries.

---

## Configuration

1. **Environment variables (.env)**

Create a .env file in the project root:

```.env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```
> For Gmail, you must use and **App Password**, not your normal password

2. **Rules configuration (`config/config.json`)**

Create a config.json file in the config folder

```JSON
{
    "rules":{
        "example@email.com": "/path/to/folder"
    },
    "settings":{
        "max_emails": 5
    }
}
```
- rules → maps sender emails to destination folders
- settings → runtime configuration

---

## Usage

Run the application:

```bash
python src/main.py
```

## How It Works

1. Loads environment variables from .env
2. Loads configuration from JSON file
3. Initializes SQLite database
4. Connects to IMAP inbox
5. Fetches latest emails
6. Checks sender against rules
7. Downloads attachments
8. Saves files into corresponding folders
9. Marks emails as processed

---

## Database

Uses SQLite (emails.db) to track processed emails and avoid duplicates

Stored data:
- email ID
- sender
- subject
- timestamp

---

## Logging

Logs are:
- printed to console
- saved to `logs/app.log`

---

## Security Notes

- Never hardcode credentials in source code
- Use .env for sensitive data
- Do not commit .env to GitHub
- Use Gmail App Password for IMAP access

---

## Future Improvements

- Better CLI Interface (arguments for filters, limits, dry-run)
- Support for multiple email providers (Gmail, Outlook, etc.)
- Improved attachment filtering (size/type rules)
- Retry mechanism for network errors
- Better sender normalization

