from config_manager import load_config
from email_client import process_emails
from db_manager import init_db
from logger_config import setup_logger

def main():
    logger = setup_logger()
    config=load_config()

    init_db()

    logger.info ("Avvio sistema mail...")
    process_emails(config, logger)
    
    logger.info("Fine esecuzione")

if __name__=="__main__":
    main()