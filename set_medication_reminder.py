#set_medication_reminder.py

import schedule
import time
from twilio.rest import Client
import threading

# Function to send SMS reminders
def send_reminder(message, phone_number):
    # Replace with your Twilio credentials
    account_sid = "AC9d05c934c1b5c556e4460e1c1e4eeb5b"
    auth_token = "7b9ca4983958d0d620bddf0130fe938a"
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_="+13613221619",  # Replace with your Twilio phone number
        to=phone_number
    )

# Function to set medication reminder
def set_medication_reminder(message, phone_number, reminder_time):
    """
    Schedules the SMS reminder at a specified time.
    reminder_time should be in 'HH:MM' 24-hour format.
    """
    # Schedule the task
    schedule.every().day.at(reminder_time).do(send_reminder, message=message, phone_number=phone_number)
    print(f"Reminder set for {reminder_time}. A message will be sent to {phone_number}.")

    # Start the scheduler in a separate thread to prevent blocking
    threading.Thread(target=run_scheduler, daemon=True).start()

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
    time.sleep(1)
