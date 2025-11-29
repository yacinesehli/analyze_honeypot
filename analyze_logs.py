import json
from collections import Counter
import os

# Chemin vers les logs de Cowrie
LOG_FILE = 'var/log/cowrie/cowrie.json'

def analyze_logs():
    print("---------------------------------------")
    print("   ANALYSE HONEYPOT COWRIE   ")
    print("---------------------------------------")

    if not os.path.exists(LOG_FILE):
        print(f"Erreur : Le fichier {LOG_FILE} est introuvable.")
        return

    sessions = 0
    ips = []
    credentials = []
    commands = []

    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # Compter les sessions
                if data['eventid'] == 'cowrie.session.connect':
                    sessions += 1
                    ips.append(data['src_ip'])
                
                # Récupérer les identifiants tentés
                if data['eventid'] == 'cowrie.login.success' or data['eventid'] == 'cowrie.login.failed':
                    user = data.get('username', 'unknown')
                    pwd = data.get('password', 'unknown')
                    credentials.append(f"{user}/{pwd}")

                # Récupérer les commandes exécutées
                if data['eventid'] == 'cowrie.command.input':
                    commands.append(data['input'])

            except Exception as e:
                continue

    print(f"\n[+] Nombre total d'attaques (sessions) : {sessions}")
    print(f"[+] Adresses IP des attaquants :\n    {set(ips)}")
    
    print(f"\n[+] Top 5 des identifiants testés (User/Pass) :")
    for cred, count in Counter(credentials).most_common(5):
        print(f"    - {cred} : {count} fois")

    print(f"\n[+] Commandes malveillantes exécutées :")
    for cmd in commands:
        print(f"    $ {cmd}")
    
    print("\n------------------------------------------------")
    print("Analyse terminée.")

if __name__ == "__main__":
    analyze_logs()