# Extraction et Gestion Automatisée des Codes de Cartes Cadeaux Shopify
Ce projet permet de récupérer automatiquement les codes de cartes cadeaux envoyés par email depuis Shopify, les extraire, les organiser dans un fichier CSV et déplacer les emails associés dans un dossier spécifique dans Gmail.

## Problématique
Lors de l'achat de nombreuses cartes cadeaux (par exemple 1100 cartes), Shopify génère un email par carte cadeau, contenant le code cadeau et un lien vers le solde. Cependant :

Shopify ne permet pas d'exporter directement les codes des cartes cadeaux.
Le processus manuel est fastidieux : il faut ouvrir chaque email, extraire le code, et l'enregistrer dans un fichier.
Les emails associés encombrent la boîte mail.

## Solutions envisagées
1. Utiliser l'API Shopify :
Problème : L'API ne donne pas accès aux codes des cartes cadeaux pour des raisons de sécurité.

2. Extraction directe des emails :
Utilisation d'une combinaison de scripts Python pour :
- Analyser les emails entrants.
- Extraire le code et le lien depuis le contenu HTML.
- Organiser les données dans un fichier CSV.
- Déplacer les emails traités dans un dossier spécifique dans Gmail.

### Choix retenu :
Extraction directe des emails, car elle répond aux besoins tout en automatisant le processus avec des outils accessibles.

## Grande Étape 1 Création des 1100 Cartes Cadeaux dans Shopify
## Outil utilisé : Matrixify
Pour créer en masse les 1100 cartes cadeaux dans Shopify, nous avons utilisé Matrixify, un outil puissant permettant d'importer et de gérer des données en masse dans Shopify.

### Étape 1 : Préparation du fichier d'import
Un fichier Excel a été préparé avec les informations nécessaires pour la création des cartes cadeaux, notamment :
- Montant des cartes cadeaux : 20 euros par carte.
- Quantité : 1100 cartes.
- Statut de la commande : Commande marquée comme "payée".

Un exemple du fichier utilisé :
📁 1100 giftcards 20 euros each IMPORT FINAL.xlsx
(le fichier contient les colonnes spécifiques pour Matrixify et Shopify).

### Étape 2 : Importation dans Shopify
1. Ouvrir Matrixify dans le BackOffice Shopify.
2. Cliquer sur Import et charger le fichier Excel préparé.
3. Vérifier les données dans Matrixify pour confirmer leur exactitude.
4. Lancer l'import.

### Étape 3 : Résultat
Une fois l'import terminé :
- Une commande contenant les 1100 cartes cadeaux a été créée dans Shopify.
- Shopify envoie automatiquement les emails de cartes cadeaux aux destinataires configurés.

## L'objectif : Recevoir les emails et avoir dans son BackOffice les 1100 Cartes Cadeau
Le script Python traite ensuite ces emails pour :
- Extraire les codes et liens des cartes cadeaux.
- Organiser ces données dans un fichier CSV utilisable.

## Grande Étape 2 Script Python : Solution Implémentée
Fonctionnalités principales :

1. Connexion sécurisée à Gmail :
- Authentification via IMAP avec un mot de passe d'application.
- Gestion des emails reçus depuis une adresse Shopify spécifique.

2. Extraction des données :
- Récupération du code cadeau et du lien de solde.
- Gestion des erreurs en cas de données manquantes.

3. Organisation des emails :
- Déplacement des emails traités dans un dossier dédié ([NOM DU DOSSIER CIBLE]).

4. Exportation des données :
- Création d'un fichier CSV contenant les données extraites.
- Nom du fichier formaté avec la date et l'heure de l'extraction pour un suivi clair.

## Prérequis
Avant de lancer le script Python pour extraire les données des cartes cadeaux, assurez-vous de respecter les prérequis suivants :

### Étape 1 : Installer Python + Créer un environnement virtuel
1. Installer Python
- Téléchargez et installez la dernière version de Python depuis le site officiel : python.org.
- Assurez-vous que pip est installé (il est inclus avec les versions récentes de Python).

2. Créer et activer un environnement virtuel
L'utilisation d'un environnement virtuel permet d'isoler les dépendances du projet.
- Ouvrez votre terminal ou invite de commande.
- Accédez au dossier du projet :
```bash
cd /chemin/vers/votre/dossier/projet
```
- Créez l'environnement virtuel :
```bash
python -m venv env
```

### Étape 2 : Activer l'environnement virtuel
- Sous Windows :
```bash
.\env\Scripts\activate
```
- Sous macOS/Linux :
```bash
source env/bin/activate
```

### Étape 3 : Vérifier l'activation
Lorsque l'environnement virtuel est activé, vous verrez son nom (par exemple env) dans la ligne de commande : (env) $

- Modules Python nécessaires :
```bash
pip install beautifulsoup4 pandas requests 
```

## Étape 2 : Activer IMAP et créer un mot de passe d'application :
1. Connectez-vous à votre compte Gmail.
2. Allez dans Paramètres > Rechercher "IMAP" et activez le protocole IMAP.
3. Créez un mot de passe d'application via https://myaccount.google.com/security :
- Sélectionnez "Mail" et "Appareil utilisé".
- Copiez le mot de passe généré pour le script.

## Guide d'installation et d'exécution
### Étape 1 : Configuration du script
1. Clonez ce projet ou copiez le script extract_gift_cards.py.
2. Mettez à jour les variables dans le script :
- Votre email Gmail :
```python
EMAIL_ACCOUNT = "[TON EMAIL]"
```
- Mot de passe d'application :
```python
EMAIL_PASSWORD = "[TON MOT DE PASSE]"
```
- Email Shopify :
```python
status, messages = mail.search(None, 'FROM "[EMAIL SENDER]"')
```
- Nom du dossier Gmail :
```python
mail.create('[NOM DU DOSSIER CIBLE]')
```
### Étape 2 : Exécution du script
1. Ouvrez un terminal.
2. Naviguez vers le dossier contenant le script.
3. Lancez le script :
```bash
python3 extract_gift_cards.py
```

### Étape 3 : Résultats
- Les codes extraits seront enregistrés dans un fichier CSV, nommé par exemple :
```
gift_card_codes_2024-11-19_14-30-00.csv
```
- Les emails traités seront déplacés dans le dossier [NOM DU DOSSIER CIBLE] dans Gmail.

## Architecture du code
- Connexion Gmail :
    - Authentification via IMAP avec imaplib.
    - Création d'un dossier Gmail si nécessaire.
- Extraction HTML :
    - Décodage et parsing des emails avec BeautifulSoup.
    - Récupération du code cadeau et du lien depuis la page Shopify avec requests.
- Organisation et export :
    - Sauvegarde des données dans un fichier CSV avec pandas.
    - Déplacement des emails traités dans Gmail.

## Exemple de sortie
Fichier CSV généré :
| ID | CODE | LIEN | 
|--|:-------------------:|-----------------------------------------------------------:| 
| 1| EDF6 F994 GFEF 7266 | https://checkout.shopify.com/gift_cards/62740070559/abc12345 | 
| 2| GH78 JKL9 MNO1 P234 | https://checkout.shopify.com/gift_cards/62740070559/xyz98765 |

## Limitations
1. Les emails non conformes au format attendu seront ignorés.
2. Le script suppose que les liens et codes de cartes cadeaux sont extraits correctement depuis Shopify.

## Améliorations futures
1. Ajouter une interface utilisateur pour une configuration plus simple.
2. Supporter d'autres fournisseurs d'email ou formats d'email.
3. Ajouter une gestion avancée des erreurs et des logs détaillés.

## Contact
Pour toute question ou suggestion, n'hésitez pas à me contacter via GitHub ou par email.


