import requests
import pprint
from flight_data import FlightData

FLIGHT_API = "QfxQ6PFDb2x5oI3DD8iiVTuahDZINEZh"
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"


class FlightSearch:

    def find_codes(self, city_name):

        tequila_headers = {
        "apikey": FLIGHT_API,
        }

        query = {
            "term": city_name,
            "location_types": "city",
        }

        tequila_response = requests.get(url=TEQUILA_ENDPOINT, params=query, headers=tequila_headers)
        result = tequila_response.json()["locations"]
        code = result[0]["code"]
        return code


    def find_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        tequila_headers = {
            "apikey": FLIGHT_API,
        }

        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            url="https://api.tequila.kiwi.com/v2/search",
            headers=tequila_headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(
                url="https://api.tequila.kiwi.com/v2/search",
                headers=tequila_headers,
                params=query,
            )

            data = response.json()["data"][0]

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )

            return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data


