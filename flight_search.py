from pprint import pprint
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class FlightSearch:
    def __init__(self, max_stopovers=0, **kw):
        self.flight_search_endpoint = os.environ.get("FLIGHTSEARCH_ENDPOINT")
        self.return_ticket = {"apikey": os.environ.get("RETURN_TICKET")}
        self.today = datetime.today().date()
        self.tomorrow = (self.today + timedelta(days=+1)).strftime("%d/%m/%Y")  # tomorrow
        self.six_months = (self.today + relativedelta(months=+6)).strftime("%d/%m/%Y")  # in six months
        self.round_7 = (self.today + timedelta(days=+7)).strftime("%d/%m/%Y")  # in 7 days time
        self.round_28 = (self.today + relativedelta(days=+28)).strftime("%d/%m/%Y")  # in 28 days time
        self.currency = "NGN"
        self.stop_overs = max_stopovers
        self.one_stop = False

    def search_flight(self, departure, destination):
        """This method performs flight searches from the flight API and sends the result to main.py"""
        stop_over_count = 0
        stop_over_city = ""
        parameters = {
            "fly_from": departure,
            "fly_to": destination,
            "date_from": self.tomorrow,
            "date_to": self.six_months,
            "return_from": self.round_7,
            "return_to": self.round_28,
            "curr": self.currency,
            "stop_over": self.stop_overs
        }
        response = requests.get(url=self.flight_search_endpoint, params=parameters, headers=self.return_ticket)
        response.raise_for_status()

        for item in response.json()["data"][0]["route"]:
            if item["flyTo"] != destination:
                stop_over_count += 1
                self.one_stop = True
                stop_over_city = item["cityTo"]
            elif stop_over_count == 0:
                self.one_stop = False
            break

        try:
            no_flight = response.json()["data"][0]["price"]
        except IndexError:
            no_flight = "0"
        return no_flight, stop_over_count, stop_over_city
