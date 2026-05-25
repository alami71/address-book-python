import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class AgendaApp:
    # This function creates the appointment manager window.
    # Parameters: none.
    # Returns: nothing, because it initializes the object.
    def __init__(self):
        self.window = tk.Tk()  # Create the main agenda window.
        self.window.title("Gestion des RDV")  # Set the window title.
        self.window.configure(bg="#F5F5F5")  # Set the background color.
        self.appointments = {}  # Store appointments as slot: contact name.
        self.buttons = {}  # Store buttons by slot text.
        self.days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]  # Define week days.
        self.times = self.create_time_slots()  # Build all time slots.
        self.build_interface()  # Create the visual interface.

    # This function creates time slots from 08:00 to 18:00 every 30 minutes.
    # Parameters: none.
    # Returns: a list of time strings.
    def create_time_slots(self):
        times = []  # Prepare the list of time slots.
        hour = 8  # Start at 08:00.
        minute = 0  # Start at zero minutes.
        while hour < 18:  # Stop before 18:00.
            times.append(str(hour).zfill(2) + ":" + str(minute).zfill(2))  # Add the current slot.
            minute = minute + 30  # Move forward by 30 minutes.
            if minute == 60:  # When minutes reach 60, move to next hour.
                minute = 0  # Reset minutes.
                hour = hour + 1  # Increase hour.
        return times  # Return all generated slots.

    # This function builds the weekly calendar buttons.
    # Parameters: none.
    # Returns: nothing.
    def build_interface(self):
        title = tk.Label(self.window, text="Agenda Hebdomadaire", font=("Helvetica", 18, "bold"), bg="#F5F5F5")  # Title label.
        title.pack(pady=15)  # Place the title.

        calendar_frame = tk.Frame(self.window, bg="#F5F5F5")  # Create the calendar frame.
        calendar_frame.pack(padx=15, pady=10)  # Place the calendar frame.

        for column, day in enumerate(self.days):  # Create day headers.
            label = tk.Label(calendar_frame, text=day, font=("Helvetica", 11, "bold"), bg="#F5F5F5")  # Day label.
            label.grid(row=0, column=column, padx=4, pady=4)  # Place the day label.

        for row, time_text in enumerate(self.times, start=1):  # Create a row for each time.
            for column, day in enumerate(self.days):  # Create a button for each day.
                slot = day + " " + time_text  # Build the appointment slot key.
                button = tk.Button(calendar_frame, text=time_text, width=10, bg="#4A90D9", fg="white", font=("Helvetica", 9), command=lambda selected_slot=slot: self.book_slot(selected_slot))  # Slot button.
                button.grid(row=row, column=column, padx=3, pady=3)  # Place the slot button.
                self.buttons[slot] = button  # Save the button reference.

        view_button = tk.Button(self.window, text="Voir mes RDV", bg="#4A90D9", fg="white", font=("Helvetica", 11), command=self.show_appointments)  # View appointments button.
        view_button.pack(pady=15)  # Place the view button.

    # This function books one appointment slot.
    # Parameters: slot as a string.
    # Returns: nothing.
    def book_slot(self, slot):
        contact_name = simpledialog.askstring("RDV", "Nom du contact:")  # Ask for the contact name.
        if contact_name is None or contact_name.strip() == "":  # Check if the name is empty.
            return
        self.appointments[slot] = contact_name  # Save the appointment in the dict.
        self.buttons[slot].config(bg="#E57373", state="disabled", text=slot.split(" ")[1])  # Mark the slot as booked.
        messagebox.showinfo("Succes", "RDV ajoute pour " + contact_name)  # Show success feedback.

    # This function shows all booked appointments.
    # Parameters: none.
    # Returns: nothing.
    def show_appointments(self):
        if len(self.appointments) == 0:  # Check if no appointments exist.
            messagebox.showinfo("RDV", "Aucun RDV reserve.")  # Show empty message.
            return
        text = ""  # Prepare display text.
        for slot in self.appointments:  # Build one line per appointment.
            text = text + slot + " : " + self.appointments[slot] + "\n"  # Add appointment line.
        messagebox.showinfo("Mes RDV", text)  # Show appointments.

    # This function starts the Tkinter event loop.
    # Parameters: none.
    # Returns: nothing.
    def run(self):
        self.window.mainloop()  # Run the agenda window.


if __name__ == "__main__":
    AgendaApp().run()  # Start the agenda application.
