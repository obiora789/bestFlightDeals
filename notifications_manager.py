import os
from twilio.rest import Client
import dotenv
import smtplib

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

my_outlook = os.environ.get("MY_EMAIL")
my_password = os.getenv("EMAIL_PASSWORD")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = os.getenv("ACCOUNT_SID")
        self.auth_token = os.environ.get("AUTH_TOKEN")
        self.to_phone = os.getenv("TO_PHONE")
        self.from_phone = os.environ.get("FROM_PHONE")

    def send_notification(self, deal_price, dept_city, iata_dep, dest_city, iata_dest, date_7, date_28,
                          stop_over, via_city):
        """This method structures the SMS message to be sent to the user"""
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=f"Low price alert! Only ₦{deal_price} to fly from {dept_city}({iata_dep}) to "
                 f"{dest_city}({iata_dest}), from {date_7} to {date_28}."
                 f"Flight has {stop_over} stop over, via {via_city}",
            from_=self.from_phone,
            to=self.to_phone
        )
        print(message.status)

    def send_emails(self, deal_price, dept_city, iata_dep, dest_city, iata_dest, date_7, date_28,
                    stop_over, via_city, emails):
        with smtplib.SMTP(host="smtp.office365.com:587") as connection:
            connection.starttls()
            connection.login(user=my_outlook, password=my_password)
            connection.sendmail(from_addr=my_outlook, to_addrs=emails,
                                msg="Subject:New Low Price Flight from Obiora's Flight Club!\n\n"
                                    f"Low price alert! Only ₦{deal_price} to fly from {dept_city}({iata_dep}) to "
                                    f"{dest_city}({iata_dest}), from {date_7} to {date_28}.\n"
                                    f"Flight has {stop_over} stop over, via {via_city}.\n"
                                    f"Visit: https://www.google.co.uk/flights?hl=en#flt={iata_dep}.{iata_dest}.{date_7}"
                                    f"*{iata_dest}.{iata_dep}.{date_28}")
