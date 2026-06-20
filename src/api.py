from fastapi import FastAPI
from db_manager import get_all_processed
from config_manager import load_config, save_config
from logger_config import setup_logger
from email_client import process_emails
from pydantic import BaseModel

app = FastAPI(
    title="Email Organizer API",
    description="API to manage the emails' automatic organization"
)

logger = setup_logger()

@app.get("/")
def root():
    return {"message": "Email Organizer API attiva"}


@app.get("/history")
def get_history():
    emails=get_all_processed()
    return {"emails": emails, "total":len(emails)}


@app.post("/process")
def process():
    config=load_config()
    process_emails(config,logger)
    return {"message": "Processing completato"}

class Rule(BaseModel):
    sender : str
    folder : str

@app.get("/rules")
def get_rules():
    config = load_config()
    return {"rules": config["rules"]}

@app.post("/rules")
def add_rule(rule:Rule):
    config = load_config()

    config ["rules"][rule.sender]=rule.folder

    save_config(config)

    return {"message": "Regola aggiunta", "sender": rule.sender, "folder":rule.folder}

@app.delete ("/rules/{sender}")
def delete_rule (sender : str):
    config =load_config()

    if sender not in config["rules"]:
        return {"message": "Regola non trovata", "sender": sender}
    
    del config ["rules"][sender]
    save_config(config)

    return {"message": "Regola eliminata", "sender": sender}


@app.put ("/rules/{sender}")
def update_rule(sender:str, rule:Rule):
    config=load_config()

    if sender not in config ["rules"]:
        return {"message": "Regola non trovata", "sender":sender}
    
    config ["rules"][sender]=rule.folder
    save_config(config)

    return {"message":"Regola aggiornata", "sender":sender, "folder":rule.folder}

class Settings (BaseModel):
    max_emails: int

@app.put("/settings")
def update_settings (settings:Settings):
    config=load_config()
    config["settings"]["max_emails"] = settings.max_emails
    save_config(config)

    return {"message": "Impostazioni aggiornate", "max_emails":settings.max_emails}