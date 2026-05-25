import hashlib
import os
import sqlite3


class FlaskDatabase:
    # This function connects to the SQLite database used by the Flask app.
    # Parameters: database_name as a string with a default value.
    # Returns: nothing, because it initializes the database helper.
    def __init__(self, database_name="contacts.db"):
        base_folder = os.path.dirname(__file__)  # Find the flask_app folder.
        self.database_path = os.path.join(base_folder, database_name)  # Build the database path.
        self.create_tables()  # Create needed tables.
        self.ensure_default_admin()  # Create default admin if missing.

    # This function creates a new SQLite connection.
    # Parameters: none.
    # Returns: a sqlite3 connection.
    def connect(self):
        connection = sqlite3.connect(self.database_path)  # Open the SQLite database.
        connection.row_factory = sqlite3.Row  # Allow row values by column name.
        return connection  # Return the open connection.

    # This function creates the contacts and admins tables.
    # Parameters: none.
    # Returns: nothing.
    def create_tables(self):
        connection = self.connect()  # Open a database connection.
        cursor = connection.cursor()  # Create a cursor.
        # This SQL query creates the contacts table with extended fields.
        cursor.execute(
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
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )
        connection.commit()  # Save table creation.
        connection.close()  # Close the connection.

    # This function hashes a password with SHA-256.
    # Parameters: password as a string.
    # Returns: the password hash as a string.
    def hash_password(self, password):
        encoded_password = password.encode("utf-8")  # Convert text to bytes.
        return hashlib.sha256(encoded_password).hexdigest()  # Return SHA-256 hash.

    # This function validates an email address simply.
    # Parameters: email as a string.
    # Returns: True if valid, False otherwise.
    def is_valid_email(self, email):
        return "@" in email and "." in email  # Accept emails containing @ and dot.

    # This function validates a phone number.
    # Parameters: phone as a string.
    # Returns: True if valid, False otherwise.
    def is_valid_phone(self, phone):
        return phone.isdigit() and len(phone) == 10  # Require exactly 10 digits.

    # This function adds a new contact to SQLite.
    # Parameters: name, email, phone, category, address, job_title, company as strings.
    # Returns: a tuple containing success as bool and message as string.
    def add_contact(self, name, email, phone, category="", address="", job_title="", company=""):
        if name.strip() == "" or email.strip() == "" or phone.strip() == "":  # Check required fields.
            return False, "Nom, email et telephone sont obligatoires."
        if not self.is_valid_email(email):  # Check email format.
            return False, "Email invalide."
        if not self.is_valid_phone(phone):  # Check phone format.
            return False, "Telephone invalide: il faut 10 chiffres."
        try:
            connection = self.connect()  # Open a database connection.
            cursor = connection.cursor()  # Create a cursor.
            # This SQL query inserts one contact into the contacts table.
            cursor.execute(
                """
                INSERT INTO contacts (name, email, phone, category, address, job_title, company)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, email, phone, category, address, job_title, company),
            )
            connection.commit()  # Save the new contact.
            connection.close()  # Close the connection.
            return True, "Contact ajoute avec succes."
        except sqlite3.Error as error:
            return False, "Erreur SQLite: " + str(error)

    # This function updates one contact by id.
    # Parameters: contact_id as int and contact fields as strings.
    # Returns: a tuple containing success as bool and message as string.
    def update_contact(self, contact_id, name, email, phone, category="", address="", job_title="", company=""):
        if name.strip() == "" or email.strip() == "" or phone.strip() == "":  # Check required fields.
            return False, "Nom, email et telephone sont obligatoires."
        if not self.is_valid_email(email):  # Check email format.
            return False, "Email invalide."
        if not self.is_valid_phone(phone):  # Check phone format.
            return False, "Telephone invalide: il faut 10 chiffres."
        try:
            connection = self.connect()  # Open a database connection.
            cursor = connection.cursor()  # Create a cursor.
            # This SQL query updates one contact selected by id.
            cursor.execute(
                """
                UPDATE contacts
                SET name = ?, email = ?, phone = ?, category = ?, address = ?, job_title = ?, company = ?
                WHERE id = ?
                """,
                (name, email, phone, category, address, job_title, company, contact_id),
            )
            connection.commit()  # Save the update.
            connection.close()  # Close the connection.
            return True, "Contact modifie avec succes."
        except sqlite3.Error as error:
            return False, "Erreur SQLite: " + str(error)

    # This function deletes one contact by id.
    # Parameters: contact_id as an integer.
    # Returns: a tuple containing success as bool and message as string.
    def remove_contact_by_id(self, contact_id):
        connection = self.connect()  # Open a database connection.
        cursor = connection.cursor()  # Create a cursor.
        # This SQL query deletes one contact selected by id.
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        connection.commit()  # Save the deletion.
        deleted_count = cursor.rowcount  # Store how many rows were deleted.
        connection.close()  # Close the connection.
        if deleted_count > 0:  # Check if something was deleted.
            return True, "Contact supprime avec succes."
        return False, "Contact introuvable."

    # This function gets all contacts sorted by name.
    # Parameters: none.
    # Returns: a list of rows.
    def get_all_contacts(self):
        connection = self.connect()  # Open a database connection.
        cursor = connection.cursor()  # Create a cursor.
        # This SQL query selects all contacts ordered by name.
        cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            ORDER BY name
            """
        )
        contacts = cursor.fetchall()  # Read all rows.
        connection.close()  # Close the connection.
        return contacts  # Return contacts.

    # This function finds one contact by id.
    # Parameters: contact_id as an integer.
    # Returns: a row or None.
    def find_contact_by_id(self, contact_id):
        connection = self.connect()  # Open a database connection.
        cursor = connection.cursor()  # Create a cursor.
        # This SQL query selects one contact by id.
        cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            WHERE id = ?
            """,
            (contact_id,),
        )
        contact = cursor.fetchone()  # Read one row.
        connection.close()  # Close the connection.
        return contact  # Return the contact or None.

    # This function searches contacts by name or email.
    # Parameters: search_text as a string.
    # Returns: a list of matching rows.
    def search_contacts(self, search_text):
        connection = self.connect()  # Open a database connection.
        cursor = connection.cursor()  # Create a cursor.
        search_pattern = "%" + search_text + "%"  # Build search pattern.
        # This SQL query searches contacts by name or email.
        cursor.execute(
            """
            SELECT id, name, email, phone, category, address, job_title, company
            FROM contacts
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY name
            """,
            (search_pattern, search_pattern),
        )
        contacts = cursor.fetchall()  # Read matching rows.
        connection.close()  # Close the connection.
        return contacts  # Return matching contacts.

    # This function creates a default admin if missing.
    # Parameters: none.
    # Returns: nothing.
    def ensure_default_admin(self):
        connection = self.connect()  # Open a database connection.
        cursor = connection.cursor()  # Create a cursor.
        # This SQL query checks if admin already exists.
        cursor.execute("SELECT id FROM admins WHERE username = ?", ("admin",))
        admin = cursor.fetchone()  # Read one admin row.
        if admin is None:  # Create default admin only when missing.
            password_hash = self.hash_password("admin")  # Hash the default password.
            # This SQL query inserts the default admin account.
            cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", ("admin", password_hash))
            connection.commit()  # Save the default admin.
        connection.close()  # Close the connection.
