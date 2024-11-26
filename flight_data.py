"""
This class is responsible for structuring the flight data.
"""

from pprint import pprint


class FlightData:
    def __init__(self, price, origin_iata_code, destination_iata_code, dep_date, ret_date, stops):
        self.price = price
        self.origin_iata_code = origin_iata_code
        self.destination_iata_code = destination_iata_code
        self.dep_date = dep_date
        self.ret_date = ret_date
        self.stops = stops


def find_cheapest_flight(flight_data):
    if flight_data is None or not flight_data['data']:
        print('No Flights Found')
        return FlightData(
            price='N/A',
            origin_iata_code='N/A',
            destination_iata_code='N/A',
            dep_date='N/A',
            ret_date='N/A',
            stops='N/A'
        )

    # Data from the first flight in the json
    first_flight = flight_data['data'][0]
    lowest_price = float(first_flight['price']['grandTotal'])
    origin = first_flight['itineraries'][0]['segments'][0]['departure']['iataCode']
    destination = first_flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
    departure_date = first_flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
    return_date = first_flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0]
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1

    # Initialize FlightData with the first flight for comparison
    cheapest_flight = FlightData(
        price=lowest_price,
        origin_iata_code=origin,
        destination_iata_code=destination,
        dep_date=departure_date,
        ret_date=return_date,
        stops=nr_stops
    )

    for flight in flight_data['data']:
        price = float(flight['price']['grandTotal'])
        if price < lowest_price:
            lowest_price = float(flight['price']['grandTotal'])
            origin = flight['itineraries'][0]['segments'][0]['departure']['iataCode']
            destination = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
            departure_date = flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
            return_date = flight['itineraries'][1]['segments'][0]['departure']['at'].split('T')[0]
            nr_stops = len(flight["itineraries"][0]["segments"]) - 1
            cheapest_flight = FlightData(
                price=lowest_price,
                origin_iata_code=origin,
                destination_iata_code=destination,
                dep_date=departure_date,
                ret_date=return_date,
                stops=nr_stops
            )
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight
