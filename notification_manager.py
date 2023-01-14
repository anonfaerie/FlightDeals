from twilio.rest import Client
import smtplib

MY_EMAIL = "laurenoneill307@gmail.com"
PASSWORD = "apwjmcoubfholibe"
TWILIO_SID = "ACd65f7001accadcdee86581d88ec4fa42"
TWILIO_AUTH_TOKEN = "e418593cfcf047077dc61d33f5584c5f"
TWILIO_VIRTUAL_NUMBER = "+15105607931"
TWILIO_VERIFIED_NUMBER = "+353833697670"


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
