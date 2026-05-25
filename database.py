import csv
import hashlib
import sqlite3


class Database:
    # This function connects to the SQLite database and creates needed tables.
    # Parameters: database_name as a string with a default value.
    # Returns: nothing, because it prepares the database connection.
    def __init__(self, database_name="contacts.db"):
        self.database_name = database_name  # Store the database file name.
        self.connection = sqlite3.connect(self.database_name)  # Open the SQLite connection.
        self.cursor = self.connection.cursor()  # Create a cursor to execute SQL queries.
        self.create_tables()  # Create database tables if they do not exist.
        self.ensure_default_admin()  # Add the default admin account if needed.

    # This function creates the contacts and admins tables.
    # Parameters: none.
    # Returns: nothing.
    def create_tables(self):
        # This SQL query creates the contacts table with extended fields.
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                category TEXT,
                address TEXT,
                job_title TEXT,
                company TEXT
            )
            """
        )
        # This SQL query creates the admins table for login accounts.
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )
        self.connection.commit()  # Save the table creation changes.

    # This function hashes a plain password with SHA-256.
    # Parameters: password as a string.
    # Returns: the hashed password as a string.
    def hash_password(self, password):
        encoded_password = password.encode("utf-8")  # Convert text to bytes for hashing.
        hashed_password = hashlib.sha256(encoded_password).hexdigest()  # Create the SHA-256 hash.
        return hashed_password  # Return the hash value.

    # This function checks if an email has a simple valid format.
    # Parameters: email as a string.
    # Returns: True if valid, False otherwise.
    def is_valid_email(self, email):
        return "@" in email and "." in email  # Accept emails containing @ and a dot.

    # This function checks if a phone number contains exactly 10 digits.
    # Parameters: phone as a string.
    # Returns: True if valid, False otherwise.
    def is_valid_phone(self, phone):
        return phone.isdigit() and len(phone) == 10  # Accept only 10 numeric characters.

    # This function adds a contact to the database after validation.
    # Parameters: name, email, phone, category, address, job_title, company as strings.
    # Returns: a tuple containing success as bool and a message as string.
    def add_contact(self, name, email, phone, category="", address="", job_title="", company=""):
        if name.strip() == "" or email.strip() == "" or phone.strip() == "":  # Check required fields.
            return False, "Nom, email et telephone sont obligatoires."
        if not self.is_valid_email(email):  # Validate the email format.
            return False, "Email invalide."
        if not self.is_valid_phone(phone):  # Validate the phone number.
            return False, "Telephone invalide: il faut 10 chiffres."
        if self.find_contact(name) is not None:  # Refuse duplicate names.
            return False, "Un contact avec ce nom existe deja."
        if self.find_contact_by_email(email) is not None:  # Refuse duplicate emails.
            return False, "Un contact avec cet email existe deja."
        try:
            # This SQL query inserts one contact into the contacts table.
            self.cursor.execute(
                """
                INSERT INTO contacts (name, email, phone, category, address, job_title, company)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, email, phone, category, address, job_title, company),
            )
            self.connection.commit()  # Save the inserted contact.
            return True, "Contact ajoute avec succes."
        except sqlite3.Error as error:
            return False, "Erreur SQLite: " + str(error)

    # This function updates an existing contact by its database id.
    # Parameters: contact_id as int, and contact fields as strings.
    # Returns: a tuple containing success as bool and a message as string.
    def update_contact(self, contact_id, name, email, phone, category="", address="", job_title="", company=""):
        if name.strip() == "" or email.strip() == "" or phone.strip() == "":  # Check required fields.
            return False, "Nom, email et telephone sont obligatoires."
        if not self.is_valid_email(email):  # Validate the email format.
            return False, "Email invalide."
        if not self.is_valid_phone(phone):  # Validate the phone number.
            return False, "Telephone invalide: il faut 10 chiffres."
        try:
            # This SQL query updates one contact selected by id.
            self.cursor.execute(
                """
                UPDATE contacts
                SET name = ?, email = ?, phone = ?, category = ?, address = ?, job_title = ?, company = ?
                WHERE id = ?
                """,
                (name, email, phone, category, address, job_title, company, contact_id),
            )
            self.connection.commit()  # Save the updated contact.
            return True, "Contact modifie avec succes."
        except sqlite3.Error as error:
            return False, "Erreur SQLite: " + str(error)

    # This function removes a contact from the database by name.
    # Parameters: name as a string.
    # Returns: a tuple containing success as bool and a message as string.
    def remove_contact(self, name):
        # This SQL query deletes a contact selected by name.
        self.cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
        self.connection.commit()  # Save the deletion.
        if self.cursor.rowcount > 0:  # Check if a row was deleted.
            return True, "Contact supprime avec succes."
        return False, "Contact introuvable."

    # This function gets all contacts sorted alphabetically.
    # Parameters: none.
    # Returns: a list of database rows.
    def get_all_contacts(self):
        # This SQL query selects all contacts ordered by name.
        self.cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            ORDER BY name
            """
        )
        return self.cursor.fetchall()  # Return all selected rows.

    # This function searches contacts by name or email.
    # Parameters: search_text as a string.
    # Returns: a list of matching database rows.
    def search_contacts(self, search_text):
        search_pattern = "%" + search_text + "%"  # Build a LIKE pattern for partial search.
        # This SQL query selects contacts where name or email contains the search text.
        self.cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY name
            """,
            (search_pattern, search_pattern),
        )
        return self.cursor.fetchall()  # Return matching contacts.

    # This function finds one contact by name.
    # Parameters: name as a string.
    # Returns: one database row or None.
    def find_contact(self, name):
        # This SQL query selects one contact by name.
        self.cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            WHERE name = ?
            """,
            (name,),
        )
        return self.cursor.fetchone()  # Return one row or None.

    # This function finds one contact by email.
    # Parameters: email as a string.
    # Returns: one database row or None.
    def find_contact_by_email(self, email):
        # This SQL query selects one contact by email.
        self.cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            WHERE email = ?
            """,
            (email,),
        )
        return self.cursor.fetchone()  # Return one row or None.

    # This function exports all contacts to a CSV file.
    # Parameters: file_name as a string with a default value.
    # Returns: a tuple containing success as bool and a message as string.
    def export_to_csv(self, file_name="contacts.csv"):
        contacts = self.get_all_contacts()  # Load all contacts from the database.
        with open(file_name, "w", newline="", encoding="utf-8") as csv_file:  # Open the CSV file.
            writer = csv.writer(csv_file)  # Create a CSV writer.
            writer.writerow(["id", "name", "email", "phone", "category", "address", "job_title", "company"])  # Write headers.
            writer.writerows(contacts)  # Write all contact rows.
        return True, "Contacts exportes vers " + file_name

    # This function adds an administrator account.
    # Parameters: username and password as strings.
    # Returns: a tuple containing success as bool and a message as string.
    def add_admin(self, username, password):
        password_hash = self.hash_password(password)  # Hash the plain password before storing it.
        try:
            # This SQL query inserts a new admin with a hashed password.
            self.cursor.execute(
                "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            self.connection.commit()  # Save the admin account.
            return True, "Administrateur ajoute avec succes."
        except sqlite3.Error as error:
            return False, "Erreur SQLite: " + str(error)

    # This function checks administrator credentials.
    # Parameters: username and password as strings.
    # Returns: True if credentials are correct, False otherwise.
    def check_admin(self, username, password):
        password_hash = self.hash_password(password)  # Hash the typed password for comparison.
        # This SQL query selects an admin by username and password hash.
        self.cursor.execute(
            "SELECT id FROM admins WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        )
        admin = self.cursor.fetchone()  # Get the matching admin if it exists.
        return admin is not None  # Return True only when an admin was found.

    # This function creates the default admin account if it does not exist.
    # Parameters: none.
    # Returns: nothing.
    def ensure_default_admin(self):
        # This SQL query checks if the default admin already exists.
        self.cursor.execute("SELECT id FROM admins WHERE username = ?", ("admin",))
        admin = self.cursor.fetchone()  # Read the admin row.
        if admin is None:  # Create admin only if missing.
            self.add_admin("admin", "admin")  # Default username and password are both admin.

    # This function closes the database connection.
    # Parameters: none.
    # Returns: nothing.
    def close(self):
        self.connection.close()  # Close the SQLite database connection.
