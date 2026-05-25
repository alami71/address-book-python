from contact import Contact
from database import Database


class AddressBook:
    # This function creates an address book connected to the database.
    # Parameters: none.
    # Returns: nothing, because it initializes the object.
    def __init__(self):
        self.database = Database()  # Create the database helper object.
        self.contacts = []  # Keep a list copy for Part 1 compatibility.
        self.load_contacts()  # Load contacts at startup.

    # This function loads all contacts from the database into the list.
    # Parameters: none.
    # Returns: the list of Contact objects.
    def load_contacts(self):
        self.contacts = []  # Clear the old list before loading.
        rows = self.database.get_all_contacts()  # Read all contacts from SQLite.
        for row in rows:  # Convert each database row into a Contact object.
            contact = Contact(row[1], row[2], row[3], row[4], row[5], row[6], row[7])  # Build one contact.
            self.contacts.append(contact)  # Add the contact to the list.
        return self.contacts  # Return the loaded contacts.

    # This function adds a Contact object to the address book.
    # Parameters: contact as a Contact object.
    # Returns: a tuple containing success as bool and a message as string.
    def add_contact(self, contact):
        result = self.database.add_contact(
            contact.name,
            contact.email,
            contact.phone,
            contact.category,
            contact.address,
            contact.job_title,
            contact.company,
        )  # Save the contact in SQLite.
        self.load_contacts()  # Refresh the list after saving.
        return result  # Return the database result.

    # This function removes a contact by name.
    # Parameters: name as a string.
    # Returns: a tuple containing success as bool and a message as string.
    def remove_contact(self, name):
        result = self.database.remove_contact(name)  # Delete the contact from SQLite.
        self.load_contacts()  # Refresh the list after deletion.
        return result  # Return the database result.

    # This function displays all contacts in the console.
    # Parameters: none.
    # Returns: nothing.
    def display_contacts(self):
        self.load_contacts()  # Refresh the list from the database.
        if len(self.contacts) == 0:  # Check if there are no contacts.
            print("Aucun contact trouve.")  # Show an empty message.
        for contact in self.contacts:  # Display every contact.
            print(contact)  # Print the readable contact text.

    # This function finds one contact by name.
    # Parameters: name as a string.
    # Returns: a Contact object or None.
    def find_contact(self, name):
        row = self.database.find_contact(name)  # Search the database by name.
        if row is None:  # Return None when not found.
            return None
        return Contact(row[1], row[2], row[3], row[4], row[5], row[6], row[7])  # Convert row to Contact.


# Difference between storing in a list vs a file:
# A list stores contacts only while the program is running, so data disappears when the program stops.
# A file stores contacts on the disk, so data stays available after closing and reopening the program.
# In the final version, SQLite is used because it is safer and easier to search than a simple text file.
