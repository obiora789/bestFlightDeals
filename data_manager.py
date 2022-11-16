import requests
import json
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class DataManager:
    def __init__(self):
        self.sheety_endpoint = os.environ.get("SHEETY_ENDPOINT")
        self.sheety_auth = {"Authorization": "Bearer " + os.getenv("SHEETY_AUTH")}
        self.sheety_data = self.read_google_sheet()["costs"]
        self.data_found = None

    def read_google_sheet(self):
        """This method reads from the Google sheet to get data"""
        sheety_response = requests.get(url=self.sheety_endpoint, headers=self.sheety_auth)
        sheety_response.raise_for_status()
        return sheety_response.json()

    def write_google_sheet(self, sheety_list):
        """This method updates the Google sheet with flight details """
        price_upload = {}
        try:
            items = [{"iataCode": sheet_dict["iataCode"], "icaoCode": sheet_dict["icaoCode"],
                      "lowestPrice": f"₦{sheet_dict['lowestPrice']}", "id": sheet_dict["id"]}
                     for sheet_dict in sheety_list]
        except KeyError:
            items = [{"lowestPrice": f"₦{sheet_dict['lowestPrice']}", "id": sheet_dict["id"]}
                     for sheet_dict in sheety_list]
        for item in items:
            price_upload["cost"] = item
            sheety_write = requests.put(
                url=f"{self.sheety_endpoint}/{item['id']}", json=price_upload, headers=self.sheety_auth)
            sheety_write.raise_for_status()

    def search_local(self, city: str):
        """This method performs a local search through the data.json. It only searches the flight API for
        details when the destination does not exist in the json file"""
        try:
            with open("data.json", mode="r") as local_file:
                local_data = json.load(local_file)
        except FileNotFoundError:
            self.data_found = False
        else:
            for key, value in local_data.items():
                key = key.title()
                city = city.title()
                if key == city:
                    self.data_found = True
                    return value["iataCode"], value["icaoCode"]
                else:
                    self.data_found = False

    def write_to_file(self, data):
        """This method manages the data.json file"""
        try:
            with open("data.json", mode="r") as read_file:
                read_data = json.load(read_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as write_file:
                json.dump(data, write_file, indent=4)
        else:
            for key in list(read_data.keys()):
                if key not in data:
                    read_data.update(data)
                    with open("data.json", mode="w") as write_file:
                        json.dump(read_data, write_file, indent=4)
