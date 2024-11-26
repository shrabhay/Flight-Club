"""
This class is responsible for talking to the Flight Search API.
"""

import requests
from dotenv import load_dotenv
from pprint import pprint
import os
os.system('clear')

load_dotenv()


class FlightSearch:
    def __init__(self):
        self.api_key = os.getenv('AMADEUS_API_KEY')
        self.api_secret = os.getenv('AMADEUS_API_SECRET')
        self.token = self.get_new_token()
        self.iata_code = None

    def get_new_token(self):
        """
        Generates the authentication token used for accessing the Amadeus API and returns it.
        This function makes a POST request to the Amadeus token endpoint with the required credentials (API key and
        API secret) to obtain a new client credentials token. Upon receiving a response, the function updates the
        FlightSearch instance's token.

        Returns:
            str: The new access token obtained from the API response.
        """
        amadeus_get_token_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        amadeus_get_token_request_body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }

        response = requests.post(
            url=os.getenv('AMADEUS_GET_TOKEN_ENDPOINT'),
            headers=amadeus_get_token_headers,
            data=amadeus_get_token_request_body
        )

        return response.json()['access_token']

    def find_iata_code(self, city_code):
        amadeus_city_search_headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        amadeus_city_search_parameters = {
            'keyword': city_code,
            'max': 1
        }

        response = requests.get(
            url=os.getenv('AMADEUS_CITY_SEARCH_ENDPOINT'),
            headers=amadeus_city_search_headers,
            params=amadeus_city_search_parameters
        )

        self.iata_code = response.json()['data'][0]['iataCode']
        return self.iata_code

    def check_flights(self, origin_iata_code, destination_iata_code, dep_date, ret_date, is_direct=True):
        amadeus_flight_offers_headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        amadeus_flight_offers_request_body = {
            'originLocationCode': origin_iata_code,
            'destinationLocationCode': destination_iata_code,
            'departureDate': dep_date.strftime('%Y-%m-%d'),
            'returnDate': ret_date.strftime('%Y-%m-%d'),
            'adults': 1,
            'nonStop': 'true' if is_direct else 'false',
            'currencyCode': 'GBP',
            'max': 10
        }

        response = requests.get(
            url=os.getenv('AMADEUS_FLIGHT_OFFERS_ENDPOINT'),
            headers=amadeus_flight_offers_headers,
            params=amadeus_flight_offers_request_body
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()
