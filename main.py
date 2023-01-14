
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager

notification_manager = NotificationManager()
flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_data()

if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch

    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.find_codes(row["city"])
    print(sheet_data)

    data_manager.destination_data = sheet_data
    data_manager.update_codes()

ORIGIN_CITY = "LON"

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    flight = flight_search.find_flights(
        ORIGIN_CITY,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:

        users = data_manager.get_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        notification_manager.send_emails(email=emails, message=message, google_link=link)
