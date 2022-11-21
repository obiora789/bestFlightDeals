import requests
import dotenv
import os

hidden_file = dotenv.find_dotenv()
dotenv.load_dotenv(hidden_file)


class UserRecords:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email_one = None
        self.email_two = None
        self.sheety_user_api = os.environ.get("SHEETY_USER_ENDPOINT")
        self.sheety_flight = os.environ.get("SHEETY_ENDPOINT")
        self.headers = {"Authorization": "Bearer " + os.getenv("SHEETY_AUTH")}
        self.user_dict = self.get_users()["users"]
        self.number_of_cities = None
        self.new_input = False

    def new_user(self):
        """This method registers a new user."""
        self.first_name = input("What is your first name?\n").title()
        self.last_name = input("What is your last name?\n").title()
        self.email_one = input("What is your email?\n").lower()
        self.email_two = input("Type your email again.\n").lower()
        if self.email_one == self.email_two:
            parameters = {
                "user": {
                    "firstName": self.first_name,
                    "lastName": self.last_name,
                    "email": self.email_one,
                }
            }
            self.post_cities()
            user_response = requests.post(url=self.sheety_user_api, json=parameters, headers=self.headers)
            user_response.raise_for_status()
            print("You're in the club.")
            return user_response.json()

    def post_cities(self):
        sheety_list = requests.get(url=self.sheety_flight, headers=self.headers)
        self.number_of_cities = int(input("How many destinations would you like to visit?\n"))
        if self.number_of_cities > 0:
            destination_list = [input(f"Input Destination {number+1}:\n").title()
                                for number in range(self.number_of_cities)]
            existing_list = []
            for sheety_dict in sheety_list.json()["costs"]:
                for key, value in sheety_dict.items():
                    if key == "city":
                        existing_list.append(value)
            for destination in destination_list:
                if destination not in existing_list:
                    city_params = {
                        "cost": {
                            "city": destination,
                        }
                    }
                    city_response = requests.post(url=self.sheety_flight, json=city_params, headers=self.headers)
                    city_response.raise_for_status()

    def get_users(self):
        """This method retrieves the user records from the Google sheet."""
        user_list = requests.get(url=self.sheety_user_api, headers=self.headers)
        user_list.raise_for_status()
        return user_list.json()
