import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

from address_book import AddressBook
from communication import send_email
from communication import send_whatsapp
from contact import Contact


class AddressBookGUI:
    # This function creates the main Tkinter address book interface.
    # Parameters: none.
    # Returns: nothing, because it initializes the object.
    def __init__(self):
        self.address_book = AddressBook()  # Create the address book controller.
        self.selected_name = ""  # Store the selected contact name.
        self.window = tk.Tk()  # Create the Tkinter window.
        self.window.title("Carnet d'Adresses")  # Set the window title.
        self.window.geometry("900x620")  # Set a comfortable window size.
        self.window.configure(bg="#F5F5F5")  # Apply the required background color.
        self.build_interface()  # Build all interface frames and widgets.
        self.refresh_contacts()  # Load contacts into the listbox.

    # This function creates the visual widgets in three stacked frames.
    # Parameters: none.
    # Returns: nothing.
    def build_interface(self):
        self.frameH = tk.Frame(self.window, bg="#F5F5F5")  # Create the top frame.
        self.frameH.pack(fill="x", padx=20, pady=12)  # Place the top frame.

        self.frameM = tk.Frame(self.window, bg="#F5F5F5")  # Create the middle frame.
        self.frameM.pack(fill="both", expand=True, padx=20, pady=8)  # Place the middle frame.

        self.frameB = tk.Frame(self.window, bg="#F5F5F5")  # Create the bottom frame.
        self.frameB.pack(fill="x", padx=20, pady=12)  # Place the bottom frame.

        title_label = tk.Label(self.frameH, text="Carnet d'Adresses", font=("Helvetica", 22, "bold"), bg="#F5F5F5")  # App title.
        title_label.grid(row=0, column=0, columnspan=4, pady=10)  # Place the title.

        self.name_entry = self.create_labeled_entry("Nom", 1, 0)  # Create name field.
        self.email_entry = self.create_labeled_entry("Email", 1, 2)  # Create email field.
        self.phone_entry = self.create_labeled_entry("Telephone", 2, 0)  # Create phone field.
        self.address_entry = self.create_labeled_entry("Adresse", 2, 2)  # Create address field.
        self.job_title_entry = self.create_labeled_entry("Fonction", 3, 0)  # Create job title field.
        self.company_entry = self.create_labeled_entry("Entreprise", 3, 2)  # Create company field.

        category_label = tk.Label(self.frameH, text="Categorie", font=("Helvetica", 11), bg="#F5F5F5")  # Category label.
        category_label.grid(row=4, column=0, padx=8, pady=8, sticky="e")  # Place category label.
        self.category_box = ttk.Combobox(self.frameH, values=["Client", "Fournisseur", "Entreprise"], font=("Helvetica", 11), width=27)  # Category combobox.
        self.category_box.grid(row=4, column=1, padx=8, pady=8, sticky="w")  # Place category combobox.

        self.listbox = tk.Listbox(self.frameM, font=("Helvetica", 11), height=12)  # Create contact listbox.
        self.listbox.pack(side="left", fill="both", expand=True)  # Place listbox.
        self.listbox.bind("<<ListboxSelect>>", self.on_contact_select)  # Fill entries when a contact is clicked.

        scrollbar = tk.Scrollbar(self.frameM)  # Create scrollbar.
        scrollbar.pack(side="right", fill="y")  # Place scrollbar.
        self.listbox.config(yscrollcommand=scrollbar.set)  # Connect listbox to scrollbar.
        scrollbar.config(command=self.listbox.yview)  # Connect scrollbar to listbox.

        self.create_button("Ajouter", self.add_contact).pack(side="left", padx=6)  # Add button.
        self.create_button("Supprimer", self.remove_contact).pack(side="left", padx=6)  # Remove button.
        self.create_button("Afficher", self.refresh_contacts).pack(side="left", padx=6)  # Refresh button.
        self.create_button("Envoyer Email", self.email_selected_contact).pack(side="left", padx=6)  # Email button.
        self.create_button("Envoyer WhatsApp", self.whatsapp_selected_contact).pack(side="left", padx=6)  # WhatsApp button.

    # This function creates a label and entry pair.
    # Parameters: label_text as string, row and column as integers.
    # Returns: the created Entry widget.
    def create_labeled_entry(self, label_text, row, column):
        label = tk.Label(self.frameH, text=label_text, font=("Helvetica", 11), bg="#F5F5F5")  # Create field label.
        label.grid(row=row, column=column, padx=8, pady=8, sticky="e")  # Place label.
        entry = tk.Entry(self.frameH, font=("Helvetica", 11), width=30)  # Create text entry.
        entry.grid(row=row, column=column + 1, padx=8, pady=8, sticky="w")  # Place entry.
        return entry  # Return entry for later use.

    # This function creates a styled button.
    # Parameters: text as string and command as a function.
    # Returns: the created Button widget.
    def create_button(self, text, command):
        return tk.Button(self.frameB, text=text, command=command, bg="#4A90D9", fg="white", font=("Helvetica", 11), padx=12, pady=8)  # Return styled button.

    # This function reads the current form values and creates a Contact.
    # Parameters: none.
    # Returns: a Contact object.
    def get_contact_from_form(self):
        return Contact(
            self.name_entry.get(),
            self.email_entry.get(),
            self.phone_entry.get(),
            self.category_box.get(),
            self.address_entry.get(),
            self.job_title_entry.get(),
            self.company_entry.get(),
        )  # Return the contact from form fields.

    # This function clears all input fields.
    # Parameters: none.
    # Returns: nothing.
    def clear_form(self):
        self.name_entry.delete(0, tk.END)  # Clear name field.
        self.email_entry.delete(0, tk.END)  # Clear email field.
        self.phone_entry.delete(0, tk.END)  # Clear phone field.
        self.category_box.set("")  # Clear category field.
        self.address_entry.delete(0, tk.END)  # Clear address field.
        self.job_title_entry.delete(0, tk.END)  # Clear job field.
        self.company_entry.delete(0, tk.END)  # Clear company field.
        self.selected_name = ""  # Clear the selected name.

    # This function adds the current form contact.
    # Parameters: none.
    # Returns: nothing.
    def add_contact(self):
        contact = self.get_contact_from_form()  # Build contact from form.
        success, message = self.address_book.add_contact(contact)  # Save contact.
        if success:  # Show success and refresh.
            messagebox.showinfo("Succes", message)  # Success feedback.
            self.clear_form()  # Clear form after adding.
            self.refresh_contacts()  # Refresh the listbox.
        else:
            messagebox.showerror("Erreur", message)  # Error feedback.

    # This function removes the selected contact.
    # Parameters: none.
    # Returns: nothing.
    def remove_contact(self):
        if self.selected_name == "":  # Require a selected contact.
            messagebox.showerror("Erreur", "Selectionnez un contact.")
            return
        success, message = self.address_book.remove_contact(self.selected_name)  # Remove selected contact.
        if success:  # Refresh on success.
            messagebox.showinfo("Succes", message)  # Success feedback.
            self.clear_form()  # Clear form after deletion.
            self.refresh_contacts()  # Refresh the listbox.
        else:
            messagebox.showerror("Erreur", message)  # Error feedback.

    # This function refreshes the listbox with sorted contacts.
    # Parameters: none.
    # Returns: nothing.
    def refresh_contacts(self):
        self.listbox.delete(0, tk.END)  # Clear old listbox items.
        contacts = self.address_book.database.get_all_contacts()  # Read sorted contacts from SQLite.
        for contact in contacts:  # Insert each contact.
            display_text = contact[1] + " | " + contact[2] + " | " + contact[3]  # Build visible line.
            self.listbox.insert(tk.END, display_text)  # Add line to listbox.

    # This function fills the form when the user clicks a contact.
    # Parameters: event from Tkinter.
    # Returns: nothing.
    def on_contact_select(self, event):
        selection = self.listbox.curselection()  # Get selected list index.
        if len(selection) == 0:  # Stop if there is no selection.
            return
        selected_text = self.listbox.get(selection[0])  # Read the selected line.
        selected_name = selected_text.split(" | ")[0]  # Extract the contact name.
        row = self.address_book.database.find_contact(selected_name)  # Load full contact row.
        if row is None:  # Stop if the contact no longer exists.
            return
        self.clear_form()  # Clear fields before filling them.
        self.selected_name = row[1]  # Store selected name for removal.
        self.name_entry.insert(0, row[1])  # Fill name.
        self.email_entry.insert(0, row[2])  # Fill email.
        self.phone_entry.insert(0, row[3])  # Fill phone.
        self.category_box.set(row[4])  # Fill category.
        self.address_entry.insert(0, row[5])  # Fill address.
        self.job_title_entry.insert(0, row[6])  # Fill job title.
        self.company_entry.insert(0, row[7])  # Fill company.

    # This function sends an email to the selected contact.
    # Parameters: none.
    # Returns: nothing.
    def email_selected_contact(self):
        contact = self.get_contact_from_form()  # Read selected contact info from form.
        if contact.email.strip() == "":  # Require an email address.
            messagebox.showerror("Erreur", "Selectionnez un contact avec email.")
            return
        subject = simpledialog.askstring("Email", "Sujet:")  # Ask for the email subject.
        body = simpledialog.askstring("Email", "Message:")  # Ask for the email body.
        if subject is not None and body is not None:  # Send only if both values exist.
            send_email(contact.email, subject, body)  # Call the email function.

    # This function sends a WhatsApp message to the selected contact.
    # Parameters: none.
    # Returns: nothing.
    def whatsapp_selected_contact(self):
        contact = self.get_contact_from_form()  # Read selected contact info from form.
        if contact.phone.strip() == "":  # Require a phone number.
            messagebox.showerror("Erreur", "Selectionnez un contact avec telephone.")
            return
        message = simpledialog.askstring("WhatsApp", "Message:")  # Ask for the WhatsApp message.
        if message is not None:  # Send only if a message was typed.
            send_whatsapp(contact.phone, message)  # Call the WhatsApp function.

    # This function starts the GUI event loop.
    # Parameters: none.
    # Returns: nothing.
    def run(self):
        self.window.mainloop()  # Run the Tkinter event loop.


if __name__ == "__main__":
    AddressBookGUI().run()  # Start the GUI application.
