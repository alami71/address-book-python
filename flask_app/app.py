from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import os
import sys

from database import FlaskDatabase


project_folder = os.path.dirname(os.path.dirname(__file__))
if project_folder not in sys.path:
    sys.path.insert(0, project_folder)

from communication import send_email_result
from communication import send_whatsapp_result


app = Flask(__name__)  # Create the Flask application.
app.secret_key = "change-this-secret-key"  # Secret key used by flash messages.
database = FlaskDatabase()  # Create the database helper.


# This function protects all Flask pages except login and static files.
# Parameters: none.
# Returns: redirect response or nothing.
@app.before_request
def require_login():
    public_endpoints = ["login", "static"]  # Pages that do not need authentication.
    if request.endpoint in public_endpoints:  # Allow public endpoints.
        return None
    if session.get("admin_username") is None:  # Redirect anonymous users to login.
        flash("Connectez-vous pour acceder a l'application.", "warning")
        return redirect(url_for("login"))
    return None


# This function shows and handles the admin login page.
# Parameters: none.
# Returns: rendered HTML page or redirect response.
def login():
    if request.method == "POST":  # Process login form submission.
        username = request.form.get("username", "")  # Read username.
        password = request.form.get("password", "")  # Read password.
        if database.check_admin(username, password):  # Verify admin credentials.
            session["admin_username"] = username  # Store logged admin in the session.
            flash("Connexion reussie.", "success")
            return redirect(url_for("index"))
        flash("Username ou password incorrect.", "danger")
    return render_template("login.html")  # Show login page.


# This function logs out the current admin.
# Parameters: none.
# Returns: redirect response to the login page.
def logout():
    session.pop("admin_username", None)  # Remove logged admin from the session.
    flash("Deconnexion reussie.", "success")
    return redirect(url_for("login"))


# This function shows all contacts on the home page.
# Parameters: none.
# Returns: rendered HTML page.
def index():
    contacts = database.get_all_contacts()  # Load all contacts from SQLite.
    return render_template("index.html", contacts=contacts, search_text="")  # Show the contact list.


# This function shows the add contact form.
# Parameters: none.
# Returns: rendered HTML page.
def add_form():
    return render_template("add.html")  # Show the add form template.


# This function saves a new contact from the form.
# Parameters: none.
# Returns: redirect response to the home page.
def add_contact():
    name = request.form.get("name", "")  # Read the name field.
    email = request.form.get("email", "")  # Read the email field.
    phone = request.form.get("phone", "")  # Read the phone field.
    category = request.form.get("category", "")  # Read the category field.
    address = request.form.get("address", "")  # Read the address field.
    job_title = request.form.get("job_title", "")  # Read the job title field.
    company = request.form.get("company", "")  # Read the company field.
    success, message = database.add_contact(name, email, phone, category, address, job_title, company)  # Save contact.
    flash(message, "success" if success else "danger")  # Show feedback message.
    return redirect(url_for("index"))  # Return to the contact list.


# This function shows the edit form for one contact.
# Parameters: contact_id from the URL as an integer.
# Returns: rendered HTML page or redirect response.
def edit_form(contact_id):
    contact = database.find_contact_by_id(contact_id)  # Load the contact by id.
    if contact is None:  # Handle missing contact.
        flash("Contact introuvable.", "danger")  # Show error message.
        return redirect(url_for("index"))  # Return to home.
    return render_template("edit.html", contact=contact)  # Show edit form.


# This function updates a contact from the edit form.
# Parameters: contact_id from the URL as an integer.
# Returns: redirect response to the home page.
def edit_contact(contact_id):
    name = request.form.get("name", "")  # Read the name field.
    email = request.form.get("email", "")  # Read the email field.
    phone = request.form.get("phone", "")  # Read the phone field.
    category = request.form.get("category", "")  # Read the category field.
    address = request.form.get("address", "")  # Read the address field.
    job_title = request.form.get("job_title", "")  # Read the job title field.
    company = request.form.get("company", "")  # Read the company field.
    success, message = database.update_contact(contact_id, name, email, phone, category, address, job_title, company)  # Update contact.
    flash(message, "success" if success else "danger")  # Show feedback message.
    return redirect(url_for("index"))  # Return to home.


# This function deletes one contact.
# Parameters: contact_id from the URL as an integer.
# Returns: redirect response to the home page.
def delete_contact(contact_id):
    success, message = database.remove_contact_by_id(contact_id)  # Delete the contact.
    flash(message, "success" if success else "danger")  # Show feedback message.
    return redirect(url_for("index"))  # Return to home.


# This function shows the email form for one contact.
# Parameters: contact_id from the URL as an integer.
# Returns: rendered HTML page or redirect response.
def email_form(contact_id):
    contact = database.find_contact_by_id(contact_id)  # Load the contact by id.
    if contact is None:  # Handle missing contact.
        flash("Contact introuvable.", "danger")  # Show error message.
        return redirect(url_for("index"))  # Return to home.
    return render_template("send_email.html", contact=contact)  # Show email form.


# This function sends an email to one contact.
# Parameters: contact_id from the URL as an integer.
# Returns: redirect response to the home page.
def email_contact(contact_id):
    contact = database.find_contact_by_id(contact_id)  # Load the contact by id.
    if contact is None:  # Handle missing contact.
        flash("Contact introuvable.", "danger")  # Show error message.
        return redirect(url_for("index"))  # Return to home.
    subject = request.form.get("subject", "")  # Read the email subject.
    body = request.form.get("body", "")  # Read the email body.
    if subject.strip() == "" or body.strip() == "":  # Check required message fields.
        flash("Sujet et message sont obligatoires.", "danger")
        return render_template("send_email.html", contact=contact)
    success, message = send_email_result(contact["email"], subject, body)  # Send the email.
    flash(message, "success" if success else "danger")  # Show feedback message.
    return redirect(url_for("index"))  # Return to home.


# This function shows the WhatsApp form for one contact.
# Parameters: contact_id from the URL as an integer.
# Returns: rendered HTML page or redirect response.
def whatsapp_form(contact_id):
    contact = database.find_contact_by_id(contact_id)  # Load the contact by id.
    if contact is None:  # Handle missing contact.
        flash("Contact introuvable.", "danger")  # Show error message.
        return redirect(url_for("index"))  # Return to home.
    return render_template("send_whatsapp.html", contact=contact)  # Show WhatsApp form.


# This function sends a WhatsApp message to one contact.
# Parameters: contact_id from the URL as an integer.
# Returns: redirect response to the home page.
def whatsapp_contact(contact_id):
    contact = database.find_contact_by_id(contact_id)  # Load the contact by id.
    if contact is None:  # Handle missing contact.
        flash("Contact introuvable.", "danger")  # Show error message.
        return redirect(url_for("index"))  # Return to home.
    message_text = request.form.get("message", "")  # Read the WhatsApp message.
    if message_text.strip() == "":  # Check required message field.
        flash("Message WhatsApp obligatoire.", "danger")
        return render_template("send_whatsapp.html", contact=contact)
    success, message = send_whatsapp_result(contact["phone"], message_text)  # Send the WhatsApp message.
    flash(message, "success" if success else "danger")  # Show feedback message.
    return redirect(url_for("index"))  # Return to home.


# This function searches contacts by name or email.
# Parameters: none.
# Returns: rendered HTML page with search results.
def search():
    search_text = request.args.get("q", "")  # Read the search text from the URL.
    contacts = database.search_contacts(search_text)  # Search contacts by name or email.
    return render_template("index.html", contacts=contacts, search_text=search_text)  # Show results.


app.add_url_rule("/login", "login", login, methods=["GET", "POST"])  # Register the login route.
app.add_url_rule("/logout", "logout", logout, methods=["GET"])  # Register the logout route.
app.add_url_rule("/", "index", index, methods=["GET"])  # Register the home route without decorators.
app.add_url_rule("/add", "add_form", add_form, methods=["GET"])  # Register the add form route.
app.add_url_rule("/add", "add_contact", add_contact, methods=["POST"])  # Register the add save route.
app.add_url_rule("/edit/<int:contact_id>", "edit_form", edit_form, methods=["GET"])  # Register edit form route.
app.add_url_rule("/edit/<int:contact_id>", "edit_contact", edit_contact, methods=["POST"])  # Register edit save route.
app.add_url_rule("/delete/<int:contact_id>", "delete_contact", delete_contact, methods=["GET"])  # Register delete route.
app.add_url_rule("/email/<int:contact_id>", "email_form", email_form, methods=["GET"])  # Register email form route.
app.add_url_rule("/email/<int:contact_id>", "email_contact", email_contact, methods=["POST"])  # Register email send route.
app.add_url_rule("/whatsapp/<int:contact_id>", "whatsapp_form", whatsapp_form, methods=["GET"])  # Register WhatsApp form route.
app.add_url_rule("/whatsapp/<int:contact_id>", "whatsapp_contact", whatsapp_contact, methods=["POST"])  # Register WhatsApp send route.
app.add_url_rule("/search", "search", search, methods=["GET"])  # Register search route.


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Start the Flask development server without a second process.
