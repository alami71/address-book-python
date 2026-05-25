from database import Database
from flask_app.database import FlaskDatabase


# This function returns realistic sample contacts for the project.
# Parameters: none.
# Returns: a list of dictionaries containing contact information.
def get_sample_contacts():
    contacts = []  # Prepare the list that will contain sample contacts.

    contacts.append({"name": "Amina El Mansouri", "email": "amina.mansouri@example.com", "phone": "0612457890", "category": "Client", "address": "23 Rue Ibn Sina, Rabat", "job_title": "Architecte", "company": "Atelier Nord"})  # Add a client contact.
    contacts.append({"name": "Youssef Bennani", "email": "youssef.bennani@example.com", "phone": "0661987432", "category": "Entreprise", "address": "14 Avenue Hassan II, Casablanca", "job_title": "Directeur Commercial", "company": "Casa Tech"})  # Add a company contact.
    contacts.append({"name": "Sara Lahlou", "email": "sara.lahlou@example.com", "phone": "0623344556", "category": "Fournisseur", "address": "8 Rue Al Massira, Tanger", "job_title": "Responsable Achats", "company": "Nord Fournitures"})  # Add a supplier contact.
    contacts.append({"name": "Karim Alaoui", "email": "karim.alaoui@example.com", "phone": "0655123409", "category": "Client", "address": "5 Boulevard Zerktouni, Marrakech", "job_title": "Gerant", "company": "Riad Atlas"})  # Add a tourism client.
    contacts.append({"name": "Nadia Berrada", "email": "nadia.berrada@example.com", "phone": "0677001122", "category": "Entreprise", "address": "31 Rue Oued Sebou, Fes", "job_title": "Cheffe de Projet", "company": "Fes Digital"})  # Add a project manager.
    contacts.append({"name": "Omar Chraibi", "email": "omar.chraibi@example.com", "phone": "0609876543", "category": "Fournisseur", "address": "19 Zone Industrielle, Kenitra", "job_title": "Responsable Logistique", "company": "LogiMaroc"})  # Add a logistics supplier.
    contacts.append({"name": "Imane Zahraoui", "email": "imane.zahraoui@example.com", "phone": "0632109876", "category": "Client", "address": "44 Avenue Mohammed V, Agadir", "job_title": "Consultante RH", "company": "Talents Sud"})  # Add a human resources client.
    contacts.append({"name": "Mehdi Tazi", "email": "mehdi.tazi@example.com", "phone": "0645678901", "category": "Entreprise", "address": "12 Parc Technologique, Rabat", "job_title": "Developpeur Senior", "company": "Atlas Software"})  # Add a technology contact.
    contacts.append({"name": "Leila Fassi", "email": "leila.fassi@example.com", "phone": "0698765432", "category": "Fournisseur", "address": "7 Rue des Orangers, Meknes", "job_title": "Commerciale", "company": "Bureau Plus"})  # Add an office supplier.
    contacts.append({"name": "Hicham Radi", "email": "hicham.radi@example.com", "phone": "0611223344", "category": "Client", "address": "2 Avenue des FAR, Oujda", "job_title": "Pharmacien", "company": "Pharmacie Al Amal"})  # Add a healthcare client.
    contacts.append({"name": "Salma Idrissi", "email": "salma.idrissi@example.com", "phone": "0666554433", "category": "Entreprise", "address": "29 Boulevard Anfa, Casablanca", "job_title": "Responsable Marketing", "company": "Blue Media"})  # Add a marketing contact.
    contacts.append({"name": "Anas Kabbaj", "email": "anas.kabbaj@example.com", "phone": "0671230987", "category": "Fournisseur", "address": "10 Route de Safi, El Jadida", "job_title": "Technicien Support", "company": "Print Services"})  # Add a technical supplier.

    return contacts  # Return the complete sample list.


# This function inserts sample contacts into the main SQLite database.
# Parameters: contacts as a list of dictionaries.
# Returns: the number of contacts added as an integer.
def seed_main_database(contacts):
    database = Database()  # Open the main project database.
    added_count = 0  # Count successfully inserted contacts.
    for contact in contacts:  # Insert each sample contact.
        success, message = database.add_contact(contact["name"], contact["email"], contact["phone"], contact["category"], contact["address"], contact["job_title"], contact["company"])  # Add the contact.
        if success:  # Count only new contacts.
            added_count = added_count + 1  # Increase the inserted count.
    database.close()  # Close the database connection.
    return added_count  # Return how many contacts were added.


# This function inserts sample contacts into the Flask SQLite database.
# Parameters: contacts as a list of dictionaries.
# Returns: the number of contacts added as an integer.
def seed_flask_database(contacts):
    database = FlaskDatabase()  # Open the Flask project database.
    added_count = 0  # Count successfully inserted contacts.
    for contact in contacts:  # Insert each sample contact.
        success, message = database.add_contact(contact["name"], contact["email"], contact["phone"], contact["category"], contact["address"], contact["job_title"], contact["company"])  # Add the contact.
        if success:  # Count only new contacts.
            added_count = added_count + 1  # Increase the inserted count.
    return added_count  # Return how many contacts were added.


# This function runs the seed process for both databases.
# Parameters: none.
# Returns: nothing.
def main():
    contacts = get_sample_contacts()  # Load realistic sample contacts.
    main_added = seed_main_database(contacts)  # Seed the main database.
    flask_added = seed_flask_database(contacts)  # Seed the Flask database.
    print(str(main_added) + " contacts ajoutes dans contacts.db.")  # Show main database result.
    print(str(flask_added) + " contacts ajoutes dans flask_app/contacts.db.")  # Show Flask database result.
    print("Les doublons existants sont ignores automatiquement.")  # Explain duplicate behavior.


if __name__ == "__main__":
    main()  # Start the seed script.
