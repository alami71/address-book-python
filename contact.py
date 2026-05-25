class Contact:
    # This function creates a contact object with all contact information.
    # Parameters: name, email, phone, category, address, job_title, company as strings.
    # Returns: nothing, because it initializes the current object.
    def __init__(self, name, email, phone, category="", address="", job_title="", company=""):
        self.name = name  # Store the contact name.
        self.email = email  # Store the contact email.
        self.phone = phone  # Store the contact phone number.
        self.category = category  # Store the contact category.
        self.address = address  # Store the physical address.
        self.job_title = job_title  # Store the job or function.
        self.company = company  # Store the company name.

    # This function converts a contact into a readable text format.
    # Parameters: none.
    # Returns: a string that represents the contact.
    def __str__(self):
        return (
            "Nom: " + self.name
            + " | Email: " + self.email
            + " | Telephone: " + self.phone
            + " | Categorie: " + self.category
            + " | Adresse: " + self.address
            + " | Fonction: " + self.job_title
            + " | Entreprise: " + self.company
        )
