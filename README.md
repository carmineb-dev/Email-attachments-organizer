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
- REST API for remote/programmatic access (history, rules management, processing trigger)

---

## Tech Stack
- Python 3
- FastAPI + Uvicorn
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
│   ├── api.py
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

git clone https://github.com/carmineb-dev/Email-attachments-organizer.git email-attachments-organizer
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
> Includes FastAPI and Uvicorn for the API, alongside standard library modules used by the CLI.

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

### CLI

Run the application:

```bash
python src/main.py
```

## REST API

Start the API server from the `src` folder:

```bash
uvicorn api:app --reload
```

The API is available at `http://localhost:8000`

Interactive documentation is auto-generated at:
```
http://localhost:8000/docs
```

## Available endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API status |
| GET | `/history` | List of already processed emails (from SQLite) |
| POST | `/process` | Triggers email processing (IMAP fetch + sorting) |
| GET | `/rules` | List of sender → folder rules |
| POST | `/rules` | Add a new rule |
| PUT | `/rules/{sender}` | Update the destination folder for an existing sender |
| DELETE | `/rules/{sender}` | Remove an existing rule |
| PUT | `/settings` | Update runtime settings (e.g. max_emails) |

#### Example requests

Add a rule:

```bash
curl -X POST http://localhost:8000/rules \
  -H "Content-Type: application/json" \
  -d '{"sender": "boss@example.com", "folder": "Lavoro"}'
```

Trigger email processing:

```bash
curl -X POST http://localhost:8000/process
```

Check processed history:

```bash
curl http://localhost:8000/history
```

---

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

> The REST API reuses the same business logic (`email_client.py`, `db_manager.py`, `config_manager.py`) as the CLI, with no code duplication. File paths for the database and config are resolved dynamically using `pathlib`, independent of the directory the command is run from.

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

- Support for multiple email providers (Gmail, Outlook, etc.)
- Improved attachment filtering (size/type rules)
- Retry mechanism for network errors
- Better sender normalization
- Authentication layer for the API (currently intended for local/personal use)

