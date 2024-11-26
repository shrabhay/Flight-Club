"""
This class is responsible for talking to the Google Sheet.
"""

import requests
from dotenv import load_dotenv
import os
os.system('clear')

load_dotenv()


class DataManager:
    def __init__(self):
        self.sheety_prices_endpoint = os.getenv('SHEETY_PRICES_ENDPOINT')
        self.sheety_users_endpoint = os.getenv('SHEETY_USERS_ENDPOINT')
        self.sheety_auth_token = os.getenv('SHEETY_AUTH_TOKEN')
        self.sheety_headers = {
            'Authorization': f'Bearer {self.sheety_auth_token}',
            'Content-Type': 'application/json'
        }
        self.flight_deals_sheet_data = None
        self.sheety_put_endpoint = None
        self.sheety_put_request_body = None

    def get_flight_deals_sheet_data(self):
        response = requests.get(url=self.sheety_prices_endpoint, headers=self.sheety_headers)
        self.flight_deals_sheet_data = response.json()['prices']
        return self.flight_deals_sheet_data

    def update_flight_deals_sheet(self, row_id, iata_code):
        self.sheety_put_endpoint = f'{self.sheety_prices_endpoint}/{row_id}'
        self.sheety_put_request_body = {
            'price': {
                'iataCode': iata_code
            }
        }
        response = requests.put(
            url=self.sheety_put_endpoint,
            headers=self.sheety_headers,
            json=self.sheety_put_request_body
        )
        # print(response.text)

    def get_customer_emails(self):
        customer_emails = []
        response = requests.get(url=self.sheety_users_endpoint, headers=self.sheety_headers)
        users = response.json()['users']
        for user in users:
            customer_emails.append(user['emailAddress'])
        return customer_emails
