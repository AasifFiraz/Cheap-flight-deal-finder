import requests
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

header = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}


class DataManager:

    def __init__(self):
        self.customer_data = None
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get("https://api.sheety.co/a8a58a4d48375bf8fc0f03c0fcff2abc/flightDeals/prices",
                                headers=header)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(f"https://api.sheety.co/a8a58a4d48375bf8fc0f03c0fcff2abc/flightDeals/prices/"
                                    f"{city['id']}", json=new_data, headers=header)

    def get_customer_emails(self):
        customers_endpoint = "https://api.sheety.co/a8a58a4d48375bf8fc0f03c0fcff2abc/flightDealsCustomer/users"
        response = requests.get(customers_endpoint, headers=header)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
