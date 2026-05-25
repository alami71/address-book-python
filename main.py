from address_book import AddressBook
from contact import Contact


# This function reads contact information from the user.
# Parameters: none.
# Returns: a Contact object created from user input.
def read_contact_from_input():
    name = input("Nom: ")  # Ask for the contact name.
    email = input("Email: ")  # Ask for the contact email.
    phone = input("Telephone (10 chiffres): ")  # Ask for the phone number.
    category = input("Categorie (Client/Fournisseur/Entreprise): ")  # Ask for the category.
    address = input("Adresse: ")  # Ask for the physical address.
    job_title = input("Fonction: ")  # Ask for the job title.
    company = input("Entreprise: ")  # Ask for the company name.
    return Contact(name, email, phone, category, address, job_title, company)  # Return the new contact.


# This function runs the command-line menu.
# Parameters: none.
# Returns: nothing.
def main():
    address_book = AddressBook()  # Create the address book object.
    running = True  # Control the menu loop.

    while running:  # Repeat the menu until the user quits.
        print("\n===== Carnet d'Adresses =====")  # Show the menu title.
        print("1. Ajouter Contact")  # Show add option.
        print("2. Supprimer Contact")  # Show remove option.
        print("3. Afficher Contacts")  # Show display option.
        print("4. Rechercher Contact")  # Show search option.
        print("5. Exporter CSV")  # Show export option.
        print("6. Quitter")  # Show quit option.
        choice = input("Votre choix: ")  # Read the user's choice.

        if choice == "1":  # Add a contact.
            contact = read_contact_from_input()  # Read contact fields.
            success, message = address_book.add_contact(contact)  # Save the contact.
            print(message)  # Show the result message.
        elif choice == "2":  # Remove a contact.
            name = input("Nom a supprimer: ")  # Ask for the name.
            success, message = address_book.remove_contact(name)  # Delete the contact.
            print(message)  # Show the result message.
        elif choice == "3":  # Display contacts.
            address_book.display_contacts()  # Print all contacts.
        elif choice == "4":  # Search for a contact.
            name = input("Nom a rechercher: ")  # Ask for the name.
            contact = address_book.find_contact(name)  # Search in the address book.
            if contact is None:  # Check if not found.
                print("Contact introuvable.")  # Show not found message.
            else:
                print(contact)  # Show the found contact.
        elif choice == "5":  # Export contacts.
            success, message = address_book.database.export_to_csv()  # Export to CSV.
            print(message)  # Show export result.
        elif choice == "6":  # Quit the program.
            running = False  # Stop the loop.
            print("Au revoir!")  # Show goodbye message.
        else:
            print("Choix invalide.")  # Show invalid choice message.


if __name__ == "__main__":
    main()  # Start the CLI program.
