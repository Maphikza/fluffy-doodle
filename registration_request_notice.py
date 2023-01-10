import os
import smtplib

MY_EMAIL = os.environ.get("GOOGLE_APP_EMAIL")
APP_PASSWORD = os.environ.get("GOOGLE_APP_PASSWORD")
WORK_EMAIL = os.environ.get("WORK_EMAIL")


class NotificationManager:

    def __init__(self):
        self.email = MY_EMAIL
        self.password = APP_PASSWORD
        self.notice_email = WORK_EMAIL
        self.message = None

    def send_email_notification(self, name, email, message):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(from_addr=self.email, to_addrs=self.notice_email,
                                msg=f"Subject:Registration Request from{name}\n\nEmail address: {email}\nRequest "
                                    f"Message: {message}")
