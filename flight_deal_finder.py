"""
This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
program requirements.
"""

import time
from datetime import datetime, timedelta
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from data_manager import DataManager
from notification_manager import NotificationManager
import os
os.system('clear')

ORIGIN_IATA_CODE = 'LON'
DEPARTURE_DATE = datetime.now() + timedelta(days=1)
RETURN_DATE = datetime.now() + timedelta(days=180)

flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()
flight_deals_sheet_data = data_manager.get_flight_deals_sheet_data()

for data in flight_deals_sheet_data:
    if data['iataCode'] == '':
        data['iataCode'] = flight_search.find_iata_code(city_code=data['city'])

for data in flight_deals_sheet_data:
    data_manager.update_flight_deals_sheet(row_id=data['id'], iata_code=data['iataCode'])

customer_emails = data_manager.get_customer_emails()

for destination in flight_deals_sheet_data:
    flights = flight_search.check_flights(
        origin_iata_code=ORIGIN_IATA_CODE,
        destination_iata_code=destination['iataCode'],
        dep_date=DEPARTURE_DATE,
        ret_date=RETURN_DATE
    )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price == 'N/A':
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            origin_iata_code=ORIGIN_IATA_CODE,
            destination_iata_code=destination["iataCode"],
            dep_date=DEPARTURE_DATE,
            ret_date=RETURN_DATE,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price with {cheapest_flight.stops} stops is: £{cheapest_flight.price}")

    if cheapest_flight.price != 'N/A' and cheapest_flight.price < destination['lowestPrice']:
        email_body = (f"LOW PRICE ALERT!! Only GBP {cheapest_flight.price} direct from"
                      f" {cheapest_flight.origin_iata_code} to {cheapest_flight.destination_iata_code}, "
                      f"departing on {cheapest_flight.dep_date} and returning on {cheapest_flight.ret_date}.")
        if cheapest_flight.stops != 0:
            email_body = (f"LOW PRICE ALERT!! Only GBP {cheapest_flight.price} direct from"
                          f" {cheapest_flight.origin_iata_code} to {cheapest_flight.destination_iata_code} with "
                          f"{cheapest_flight.stops} stop(s) departing on {cheapest_flight.dep_date} and returning on"
                          f" {cheapest_flight.ret_date}.")

        notification_manager.send_emails(
            customer_emails=customer_emails,
            email_body=email_body
        )
