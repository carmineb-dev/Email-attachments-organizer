from config_manager import load_config
from email_client import process_emails

def main():
    config=load_config()
    print ("Avvio sistema mail...\n")
    process_emails(config)
    print("\nFine esecuzione")

if __name__=="__main__":
    main()