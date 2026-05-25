# Gestion d'un Carnet d'Adresses

## Description
Application Python complete pour gerer un carnet d'adresses. Le projet contient une interface en ligne de commande, une interface Tkinter, une authentification, une base SQLite, une application Flask, des fonctions de communication et un agenda de rendez-vous.

## Project Structure
- `contact.py` : classe Contact.
- `address_book.py` : logique du carnet d'adresses.
- `main.py` : menu CLI.
- `auth.py` : connexion administrateur Tkinter.
- `database.py` : operations SQLite.
- `communication.py` : email et WhatsApp.
- `agenda.py` : gestionnaire de rendez-vous Tkinter.
- `app_gui.py` : interface graphique Tkinter.
- `flask_app/app.py` : application web Flask.
- `flask_app/database.py` : base SQLite adaptee a Flask.
- `flask_app/templates/base.html` : layout commun.
- `flask_app/templates/index.html` : liste et recherche.
- `flask_app/templates/add.html` : formulaire d'ajout.
- `flask_app/templates/edit.html` : formulaire de modification.
- `seed_data.py` : donnees realistes pour tester rapidement.
- `requirements.txt` : dependances.
- `.gitignore` : fichiers ignores par Git.

## How to Install
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python main.py
python auth.py
python app_gui.py
python agenda.py
python flask_app/app.py
```

Identifiants admin par defaut pour Tkinter et Flask:
```text
username: admin
password: admin
```

## How to Add Sample Data
```bash
python seed_data.py
```

## Email and WhatsApp Setup
Pour envoyer un email avec Gmail, configurez les variables d'environnement avant de lancer `app_gui.py`.

PowerShell:
```powershell
$env:GMAIL_EMAIL="votre@gmail.com"
$env:GMAIL_PASSWORD="mot_de_passe_application_gmail"
python app_gui.py
```

Important: Gmail demande souvent un mot de passe d'application, pas le mot de passe normal du compte.

Pour WhatsApp, les numeros doivent normalement contenir l'indicatif pays, par exemple `+212612345678`. Le projet convertit automatiquement les numeros marocains au format `0612345678` vers `+212612345678`.

## Features
1. Classe Contact, classe AddressBook et menu CLI.
2. Stockage persistant avec validations et explication liste/fichier.
3. Interface Tkinter avec liste, boutons et messages.
4. Authentification admin avec SHA-256 pour Tkinter et Flask.
5. Base SQLite avec contacts, admins et export CSV.
6. Application Flask avec Bootstrap 5, ajout, modification, suppression, email et WhatsApp.
7. Envoi email et WhatsApp.
8. Champs etendus: categorie, adresse, fonction, entreprise.
9. Agenda hebdomadaire Tkinter.
10. Preparation GitHub avec README, `.gitignore` et requirements.

## Technologies Used
- Python
- Tkinter
- SQLite
- Flask
- Bootstrap 5
- smtplib
- pywhatkit
- hashlib, module integre a Python

## Authors
- Projet realise pour le cours Python.

## How to collaborate with GitHub
1. Clone the repo:
```bash
git clone <repo-url>
```
2. Create a branch:
```bash
git checkout -b feature/your-feature
```
3. Commit your work:
```bash
git commit -m "feat: description"
```
4. Push the branch:
```bash
git push origin feature/your-feature
```
5. Open a Pull Request on GitHub.
