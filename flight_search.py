import requests
from flight_data import FlightData
import os
from dotenv import load_dotenv

load_dotenv()

TEQUILA_ENDPOINT = 'https://tequila-api.kiwi.com'
API_KEY = os.getenv("TEQUILA_API_KEY")


class FlightSearch:

    def get_destination_code(self, city_name):
        header = {"apikey": API_KEY}
        parameters = {"term": city_name, "location_types": "city"}
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        response = requests.get(location_endpoint, headers=header, params=parameters)
        data = response.json()["locations"][0]["code"]
        return data

    def check_flights(self, destination_city_code, from_time, to_time, flight_location):
        header = {"apikey": API_KEY}
        parameters = {
            "fly_from": "CMB",  # Change this to CMB
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "LKR"
        }
        response = requests.get(f"{TEQUILA_ENDPOINT}/v2/search", headers=header, params=parameters)

        try:

            data = response.json()["data"][0]
            print(f"{data['route'][0]['cityTo']}: Rs.{data['price']}")

        except IndexError:

            parameters["max_stopovers"] = 1
            response = requests.get(f"{TEQUILA_ENDPOINT}/v2/search", headers=header, params=parameters)
            try:
                data = response.json()["data"][0]
            except IndexError:
                print("No flights available")
                return None

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            return flight_data

