from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager
from notifications_manager import NotificationManager
from get_user_record import UserRecords

CITY_OF_DEPARTURE = "Lagos"
flight_prices = FlightSearch()
get_iata = FlightData()
DEPARTURE_AERODROME = get_iata.get_codes(CITY_OF_DEPARTURE)[0]
data_mgr = DataManager()
notify_user = NotificationManager()
users = UserRecords()
flight_date_7 = flight_prices.round_7
flight_date_28 = flight_prices.round_28


def write_code():
    """This method sends necessary data to notifications, Google Sheets and the data.json file to be updated."""
    global flight_prices
    iata_code = both_codes[0]
    icao_code = both_codes[1]
    if flight_prices.one_stop:
        flight_prices = FlightSearch(max_stopovers=1)
    best_deals = flight_prices.search_flight(departure=DEPARTURE_AERODROME, destination=iata_code)
    best_price = best_deals[0]
    number_of_stopovers = best_deals[1]
    stop_city = best_deals[2]
    best_price = round(float(best_price), 2)
    write_data = {
        location["city"].title(): {"iataCode": iata_code, "icaoCode": icao_code,
                                   "lowestPrice": f"{best_price}", "id": location["id"], },
    }
    if best_price > 0:
        try:
            old_price = location["lowestPrice"]
            try:
                old_price = float(old_price.split("₦")[1])
            except ValueError:
                old_price = float(old_price.split("₦")[2])
        except KeyError:
            location["lowestPrice"] = best_price
        else:
            if best_price < float(old_price):
                email_list = [record["email"] for record in users.user_dict]
                notify_user.send_emails(deal_price=f"{'{:.2f}'.format(best_price)}", dept_city=CITY_OF_DEPARTURE,
                                        iata_dep=DEPARTURE_AERODROME, iata_dest=iata_code,
                                        date_7=flight_date_7, date_28=flight_date_28,
                                        dest_city=location["city"].title(), stop_over=number_of_stopovers,
                                        via_city=stop_city, emails=email_list)
                # notify_user.send_notification(deal_price=f"{'{:.2f}'.format(best_price)}",dept_city=CITY_OF_DEPARTURE,
                #                               iata_dep=DEPARTURE_AERODROME, iata_dest=iata_code,
                #                               date_7=flight_date_7, date_28=flight_date_28,
                #                               dest_city=location["city"].title(), stop_over=number_of_stopovers,
                #                               via_city=stop_city)
        if "iataCode" in keys_list or "icaoCode" in keys_list:
            data_mgr.write_google_sheet([{"lowestPrice": f"{'{:.2f}'.format(best_price)}", "id": location["id"]}])
        else:
            data_mgr.write_google_sheet([{"iataCode": iata_code, "icaoCode": icao_code,
                                          "lowestPrice": f"{'{:.2f}'.format(best_price)}", "id": location["id"]}])
        data_mgr.write_to_file(write_data)


print("Welcome to Obiora's Flight Club. \nWe find the best flight deals for you.")
user_request = input("Type 'New' or 'Search' to either register a new user or send out emails for best flight deals.\n")
user_request = user_request.title()
if user_request == "New":
    users.new_user()
elif user_request == "Search":
    for location in data_mgr.sheety_data:
        keys_list = list(location.keys())
        get_local_data = data_mgr.search_local(location["city"])
        if data_mgr.data_found:
            both_codes = get_local_data
            write_code()
        else:
            both_codes = get_iata.get_codes(location["city"])
            write_code()
