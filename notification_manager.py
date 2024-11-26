"""
This class is responsible for sending notifications with the deal flight details.
"""

import smtplib
from dotenv import load_dotenv
import os
os.system('clear')

load_dotenv()


class NotificationManager:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST')
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')

    def connect_to_email_account(self):
        connection = smtplib.SMTP(host=self.smtp_host)
        connection.starttls()
        connection.login(
            user=self.smtp_user,
            password=self.smtp_password
        )
        return connection

    def send_emails(self, customer_emails, email_body):
        subject = 'LOW PRICE ALERT'
        message = email_body

        connection = self.connect_to_email_account()
        connection.sendmail(
            from_addr=self.smtp_user,
            to_addrs=customer_emails,
            msg=f'Subject:{subject}\n\n{message}'
        )
        connection.close()
