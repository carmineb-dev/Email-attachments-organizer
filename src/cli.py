from config_manager import load_config, save_config

def email_menu(config):
    print("\n --- ACCOUNT EMAIL ---")
    config["email"]["user"] =input ("Email: ") or config ["email"]["user"]
    config["email"]["password"]= input ("Password: ") or config ["email"]["password"]

def rules_menu(config):
    print ("\n--- RULES ---")

    print ("Regole attuali: ")
    for k,v in config["rules"].items():
        print(f"{k} -> {v}\n")
    
    print("\n Aggiungi una nuova regola:")
    sender=input("Mittente: ")
    folder = input("Cartella: ")

    if sender and folder:
        config["rules"][sender]=folder


def menu():
    config=load_config()

    while True:
        print("\n---- MENU ----")
        print("1. Account email")
        print("2. Regole (mittente -> cartella)")
        print("3. Esci")

        choice=input("Scelta: ")
        
        if choice == "1":
            email_menu(config)
        elif choice =="2":
            rules_menu(config)
        elif choice =="3":
            save_config(config)
            break

    save_config(config)

if __name__=="__main__":
    menu()