# twilio_integration.py

from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC9d05c934c1b5c556e4460e1c1e4eeb5b"
AUTH_TOKEN = "7b9ca4983958d0d620bddf0130fe938a"

def send_sms(to, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    from_number = "+13613221619"  # Replace with your Twilio number
    client.messages.create(to=to, from_=from_number, body=message)
    print("Message sent!")

if __name__ == "__main__":
    recipient = input("Enter recipient's phone number: ")
    message = input("Enter your message: ")
    send_sms(recipient, message)