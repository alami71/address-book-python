import os
import smtplib
from email.mime.text import MIMEText
from tkinter import messagebox

from dotenv import load_dotenv


load_dotenv()


# This function converts a local Moroccan phone number to WhatsApp international format.
# Parameters: phone as a string.
# Returns: a formatted phone number string.
def format_phone_for_whatsapp(phone):
    clean_phone = phone.strip()  # Remove spaces before and after the phone number.
    clean_phone = clean_phone.replace(" ", "")  # Remove spaces inside the phone number.
    clean_phone = clean_phone.replace("-", "")  # Remove dashes inside the phone number.

    if clean_phone.startswith("+"):  # Keep already international numbers unchanged.
        return clean_phone
    if clean_phone.startswith("00"):  # Convert 00212... format to +212...
        return "+" + clean_phone[2:]
    if clean_phone.startswith("0") and len(clean_phone) == 10:  # Convert Moroccan local numbers.
        return "+212" + clean_phone[1:]

    return clean_phone  # Return the original cleaned number if no rule matched.


# This function sends an email with Gmail SMTP.
# Parameters: to_email, subject, and body as strings.
# Returns: True if sent, False otherwise.
def send_email(to_email, subject, body):
    sender_email = os.environ.get("GMAIL_EMAIL")  # Read Gmail address from environment variables.
    sender_password = os.environ.get("GMAIL_PASSWORD")  # Read Gmail app password from environment variables.
    if sender_email is None or sender_password is None:  # Check if credentials are missing.
        messagebox.showerror("Erreur", "Variables GMAIL_EMAIL et GMAIL_PASSWORD manquantes.\nExemple PowerShell:\n$env:GMAIL_EMAIL='votre@gmail.com'\n$env:GMAIL_PASSWORD='mot_de_passe_application'")
        return False

    message = MIMEText(body)  # Create the text email body.
    message["From"] = sender_email  # Set sender email header.
    message["To"] = to_email  # Set receiver email header.
    message["Subject"] = subject  # Set email subject header.

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)  # Connect to Gmail SMTP server.
        smtp_server.starttls()  # Start TLS encryption for security.
        smtp_server.login(sender_email, sender_password)  # Login with Gmail credentials.
        smtp_server.sendmail(sender_email, to_email, message.as_string())  # Send the email message.
        smtp_server.quit()  # Close the SMTP connection.
        messagebox.showinfo("Succes", "Email envoye avec succes.")
        return True
    except Exception as error:
        messagebox.showerror("Erreur", "Email non envoye: " + str(error))
        return False


# This function sends a WhatsApp message instantly.
# Parameters: phone and message as strings.
# Returns: True if the call succeeds, False otherwise.
def send_whatsapp(phone, message):
    # The phone number must include country code, for example +212612345678.
    formatted_phone = format_phone_for_whatsapp(phone)  # Convert local phone number to international format.
    try:
        import pywhatkit  # Import pywhatkit only when WhatsApp sending is requested.
        pywhatkit.sendwhatmsg_instantly(formatted_phone, message)  # Open WhatsApp Web and send the message.
        messagebox.showinfo("Succes", "Message WhatsApp envoye.")
        return True
    except Exception as error:
        messagebox.showerror("Erreur", "WhatsApp non envoye: " + str(error))
        return False
