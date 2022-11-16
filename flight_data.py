import requests
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.tequila_endpoint = os.getenv("TEQUILA_ENDPOINT")
        self.headers = {"apikey": os.environ.get("HEADERS")}
        self.goflightlabs_endpoint = os.environ.get("GOFLIGHTLABS_ENDPOINT")

    def get_codes(self, city):
        """This method performs searches for flight data from the location API and sends the result to main.py"""
        icao_code = ""
        data = {
            "term": city,
        }
        iata_response = requests.get(url=self.tequila_endpoint, params=data, headers=self.headers)
        iata_response.raise_for_status()
        iata_code = iata_response.json()["locations"][0]["code"]
        parameters = {
            "access_key": os.environ.get("GOFLIGHTLABS_KEY"),
            "search": iata_code
        }
        icao_response = requests.get(url=self.goflightlabs_endpoint, params=parameters)
        icao_response.raise_for_status()
        for item in icao_response.json():
            try:
                if item["iata_code"] == iata_code:
                    icao_code = item["icao_code"]
            except TypeError or KeyError:
                continue
            else:
                return iata_code, icao_code
