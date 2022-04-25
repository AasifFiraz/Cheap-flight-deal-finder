import requests
import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
# Get your bearer token from sheety api, An excel sheet has to be created and stored in Google Drive before
# connecting with sheety
HEADER = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

print("Welcome to Aasif's Flight Deal Finder.")
print("We find the best flight deals and email you.")

first_name = input("What's your first name?\n").title()
last_name = input("What's your last name?\n").title()
email = input("What's your email address?\n").strip()
email_check = input("Type your email address again?\n").strip()

while email != email_check:
    print("Email Not Matching")
    email = input("What's your email address?\n").strip()
    email_check = input("Type your email address again?\n").strip()

parameters = {
    "user": {
        "firstName": first_name,
        "lastName": last_name,
        "email": email
    }
}

response = requests.post("https://api.sheety.co/a8a58a4d48375bf8fc0f03c0fcff2abc/flightDealsCustomer/users",
                         headers=HEADER, json=parameters)

if response.status_code == 200:
    print("Success! Your email has been added, look forwards to some amazing flight deals!")
else:
    print("There was an issue, please try again later.")


