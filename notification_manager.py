from twilio.rest import Client
import smtplib

MY_EMAIL = YOUR_EMAIL
PASSWORD = YOUR_PASSWORD
TWILIO_SID = YOUR_TWILIO_SID
TWILIO_AUTH_TOKEN = YOUR_AUTH_TOKEN
TWILIO_VIRTUAL_NUMBER = YOUR_VIRTUAL_NUMBER
TWILIO_VERIFIED_NUMBER = YOUR_VERIFIED_NUMBER


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )

        print(message.sid)

    def send_emails(self, message, email, google_link):

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=email,
                                msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_link}".encode('utf-8'))
