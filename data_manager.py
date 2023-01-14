import requests
SHEETY_ENDPOINT = "https://api.sheety.co/8422d21732d6fec56c965791f556b4d5/flightDealsSheet/prices"
SHEETY_USER_ENDPOINT = "https://api.sheety.co/8422d21732d6fec56c965791f556b4d5/flightDealsSheet/users"

class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.user_data = {}

    def get_data(self):
        sheet_response = requests.get(SHEETY_ENDPOINT).json()
        sheety_data = sheet_response["prices"]
        self.destination_data = sheety_data

        return self.destination_data


    def get_emails(self):
        data = requests.get(SHEETY_USER_ENDPOINT).json()
        self.user_data = data["users"]

        return self.user_data


    def update_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )

