import hashlib
import tkinter as tk
from tkinter import messagebox

from database import Database


# This function hashes a plain text password with SHA-256.
# Parameters: password as a string.
# Returns: a SHA-256 hash as a string.
def hash_password(password):
    # Hashing means transforming a password into a fixed unreadable value.
    # We use hashing so the real password is not stored directly.
    encoded_password = password.encode("utf-8")  # Convert the password to bytes.
    hashed_password = hashlib.sha256(encoded_password).hexdigest()  # Create the SHA-256 hash.
    return hashed_password  # Return the hashed password.


# This function compares a plain password with a stored hash.
# Parameters: plain as the typed password and hashed as the stored hash.
# Returns: True if both match, False otherwise.
def check_password(plain, hashed):
    return hash_password(plain) == hashed  # Compare the new hash with the stored hash.


class LoginWindow:
    # This function creates the login window.
    # Parameters: none.
    # Returns: nothing, because it initializes the window.
    def __init__(self):
        self.database = Database()  # Create the database helper.
        self.window = tk.Tk()  # Create the main login window.
        self.window.title("Connexion")  # Set the window title.
        self.window.geometry("380x260")  # Set a comfortable window size.
        self.window.configure(bg="#F5F5F5")  # Set the background color.
        self.build_interface()  # Build all widgets.

    # This function builds the login form widgets.
    # Parameters: none.
    # Returns: nothing.
    def build_interface(self):
        title_label = tk.Label(self.window, text="Connexion Admin", font=("Helvetica", 18, "bold"), bg="#F5F5F5")  # Title.
        title_label.pack(pady=20)  # Place the title with vertical padding.

        form_frame = tk.Frame(self.window, bg="#F5F5F5")  # Create a frame for fields.
        form_frame.pack(pady=5)  # Place the form frame.

        tk.Label(form_frame, text="Username", font=("Helvetica", 11), bg="#F5F5F5").grid(row=0, column=0, padx=8, pady=8, sticky="e")  # Username label.
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=24)  # Username entry.
        self.username_entry.grid(row=0, column=1, padx=8, pady=8)  # Place username entry.

        tk.Label(form_frame, text="Password", font=("Helvetica", 11), bg="#F5F5F5").grid(row=1, column=0, padx=8, pady=8, sticky="e")  # Password label.
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=24, show="*")  # Password entry.
        self.password_entry.grid(row=1, column=1, padx=8, pady=8)  # Place password entry.

        login_button = tk.Button(self.window, text="Se connecter", command=self.login, bg="#4A90D9", fg="white", font=("Helvetica", 11), padx=16, pady=8)  # Login button.
        login_button.pack(pady=20)  # Place the login button.

    # This function checks the typed login credentials.
    # Parameters: none.
    # Returns: nothing.
    def login(self):
        username = self.username_entry.get()  # Read the username.
        password = self.password_entry.get()  # Read the password.
        if self.database.check_admin(username, password):  # Verify credentials in SQLite.
            messagebox.showinfo("Succes", "Connexion reussie.")  # Show success feedback.
            self.window.destroy()  # Close the login window.
            from app_gui import AddressBookGUI  # Import here to avoid circular import problems.
            AddressBookGUI().run()  # Open the main address book GUI.
        else:
            messagebox.showerror("Erreur", "Username ou password incorrect.")  # Show error feedback.

    # This function starts the login event loop.
    # Parameters: none.
    # Returns: nothing.
    def run(self):
        self.window.mainloop()  # Run the Tkinter window loop.


if __name__ == "__main__":
    LoginWindow().run()  # Start the login window.
