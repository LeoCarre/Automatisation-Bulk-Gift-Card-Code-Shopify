import imaplib
import email
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime

# Configuration de la boîte mail
IMAP_SERVER = "imap.gmail.com" # Exemple avec Gmail
EMAIL_ACCOUNT = "[TON EMAIL]"  # Remplacez par votre email Gmail
EMAIL_PASSWORD = "[TON MOT DE PASSE]"  # Remplacez par le mot de passe d'application

# Fonction pour récupérer le code de la carte cadeau à partir de la page
def get_gift_card_code(url):
    # Effectuer une requête HTTP pour obtenir le HTML de la page
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Parser le contenu HTML de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher l'élément contenant le code
        code_div = soup.find('div', class_='[NOM DE LA CLASSE]')
        if code_div:
            code_input = code_div.find('input', class_='[NOM DE LA CLASSE]')
            if code_input:
                return code_input['value']  # Retourner le code de la carte cadeau
        else:
            print("Code non trouvé dans la page.")
            return None
    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return None


try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    print("Connexion réussie !")
except Exception as e:
    print(f"Erreur : {e}")

# Connexion à la boîte mail
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
mail.select("inbox")  # Dossier à scanner

# Créer le dossier "[NOM DU DOSSIER CIBLE]" si il n'existe pas
status, folders = mail.list()
folder_exists = False
for folder in folders:
    if b'[NOM DU DOSSIER CIBLE]' in folder:
        folder_exists = True

if not folder_exists:
    mail.create('[NOM DU DOSSIER CIBLE]')  # Crée le dossier si inexistant
    print("Dossier '[NOM DU DOSSIER CIBLE]' créé.")

# Rechercher les e-mails provenant de Shopify
status, messages = mail.search(None, 'FROM "[EMAIL SENDER]"')
email_ids = messages[0].split()

# Liste pour stocker les données
data = []

# Parcourir chaque e-mail
for idx, email_id in enumerate(email_ids, 1):
    res, msg = mail.fetch(email_id, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # Charger le message email
            msg = email.message_from_bytes(response[1])
            
            # Décoder l'e-mail
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        html_content = part.get_payload(decode=True)

                        try:
                            html_content = html_content.decode('utf-8')  # Tentative de décodage en UTF-8
                        except UnicodeDecodeError:
                            html_content = html_content.decode('latin-1')  # Décodage alternatif en Latin-1 (ISO-8859-1)

                        
                        # Analyser le HTML
                        soup = BeautifulSoup(html_content, "html.parser")
                        
                        # Extraire le lien cadeau
                        link_table = soup.find("a", href=True, string="[PHRASE DU BOUTON]")
                        link = link_table["href"] if link_table else "Lien non trouvé"
                        
                        # Chercher et récupérer le code de la carte cadeau à partir du lien
                        code = get_gift_card_code(link)  # Appel de la fonction pour obtenir le code

                        # Ajouter les données
                        data.append({"ID": idx, "CODE": code if code else "Code non trouvé", "LIEN": link})

                        # Déplacer l'email dans le dossier "[NOM DU DOSSIER CIBLE]"
                        mail.store(email_id, '+X-GM-LABELS', '"[NOM DU DOSSIER CIBLE]"')
                        mail.store(email_id, '+FLAGS', '(\Deleted)')
                        print(f"Email {idx} déplacé dans le dossier '[NOM DU DOSSIER CIBLE]'.")

# Déconnexion de la boîte mail
mail.expunge()  # Supprimer les emails marqués comme supprimés
mail.logout()

# Obtenir la date et l'heure actuelles pour le nom du fichier
now = datetime.now()  # Date et heure actuelles
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")  # Formater la date et l'heure (année-mois-jour_heure-minute-seconde)

# Sauvegarder les données dans un fichier CSV avec la date et l'heure dans le nom du fichier
file_name = f"gift_card_codes_{timestamp}.csv"  # Nom du fichier avec date et heure
df = pd.DataFrame(data)
df.to_csv(file_name, index=False)

print(f"Extraction terminée. Les données sont sauvegardées dans '{file_name}'.")
