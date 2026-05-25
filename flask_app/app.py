from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from database import FlaskDatabase


app = Flask(__name__)  # Create the Flask application.
app.secret_key = "change-this-secret-key"  # Secret key used by flash messages.
database = FlaskDatabase()  # Create the database helper.


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


# This function searches contacts by name or email.
# Parameters: none.
# Returns: rendered HTML page with search results.
def search():
    search_text = request.args.get("q", "")  # Read the search text from the URL.
    contacts = database.search_contacts(search_text)  # Search contacts by name or email.
    return render_template("index.html", contacts=contacts, search_text=search_text)  # Show results.


app.add_url_rule("/", "index", index, methods=["GET"])  # Register the home route without decorators.
app.add_url_rule("/add", "add_form", add_form, methods=["GET"])  # Register the add form route.
app.add_url_rule("/add", "add_contact", add_contact, methods=["POST"])  # Register the add save route.
app.add_url_rule("/edit/<int:contact_id>", "edit_form", edit_form, methods=["GET"])  # Register edit form route.
app.add_url_rule("/edit/<int:contact_id>", "edit_contact", edit_contact, methods=["POST"])  # Register edit save route.
app.add_url_rule("/delete/<int:contact_id>", "delete_contact", delete_contact, methods=["GET"])  # Register delete route.
app.add_url_rule("/search", "search", search, methods=["GET"])  # Register search route.


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Start the Flask development server without a second process.
