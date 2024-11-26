# Flight Deal Finder Project
## Description
This project finds the cheapest flight deals from London (LON) to various destinations worldwide. It checks for flight availability using the Amadeus API, processes the data to identify the best deals, and sends email notifications to customers when a low-price flight is found.

---

## Files Overview

1. **`flight_data.py`**: This file contains the `FlightData` class, which structures flight data and the `find_cheapest_flight` function to find the cheapest flight from the provided data.
2. **`flight_search.py`**: This file interacts with the Amadeus Flight Search API to fetch flight data, including fetching IATA codes for cities and checking for flights based on specified criteria.
3. **`data_manager.py`**: Manages data from the flight deals sheet, including retrieving and updating flight deal data.
4. **`notification_manager.py`**: Handles sending email notifications using SMTP when a low-price flight is found.
5. **`flight_deal_finder.py`**: The main script that coordinates all tasks, from retrieving flight data to sending notifications.
6. **`requirements.txt`**: Contains the dependencies required for the project.

---

## Getting Started

Follow the steps below to get the project up and running on your local machine.

### Prerequisites

- Python 3.x
- An Amadeus API account (for flight search data)
- A valid SMTP email account (e.g., Gmail, SendGrid) for sending email notifications

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```commandline
git clone https://github.com/shrabhay/Flight-Club.git
cd Flight-Club
```

### Step 2: Install Dependencies
Install the required Python libraries by running:
```commandline
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the root directory of the project and add the following variables:
```text
AMADEUS_API_KEY=<your_amadeus_api_key>
AMADEUS_API_SECRET=<your_amadeus_api_secret>
AMADEUS_GET_TOKEN_ENDPOINT=https://test.api.amadeus.com/v1/security/oauth2/token
AMADEUS_CITY_SEARCH_ENDPOINT=https://test.api.amadeus.com/v2/reference-data/cities
AMADEUS_FLIGHT_OFFERS_ENDPOINT=https://test.api.amadeus.com/v2/shopping/flight-offers
SMTP_HOST=<your_smtp_host>
SMTP_USER=<your_smtp_user>
SMTP_PASSWORD=<your_smtp_password>
```

#### How to Get API Keys:
##### 1. Amadeus API Key:
* Go to the [Amadeus for Developers](https://developers.amadeus.com/) website and sign up for an account.
* Once logged in, create a new application to get your API key and API secret.
* Use the credentials you receive to authenticate and access the flight data API.

##### 2. SMTP Credentials:
* If you're using Gmail:
  * Enable "Less Secure Apps" access in your Gmail account settings or set up App Passwords if you have 2FA enabled.
  * Use your Gmail email address and password for the `SMTP_USER` and `SMTP_PASSWORD` fields.
* For other SMTP services, you will need to refer to their documentation to get the SMTP host and credentials.

### Step 4: Run the Application
Once you've set up the environment variables, you can run the main script to search for flight deals and send email notifications.
```commandline
python3 flight_deal_finder.py
```

This script will:
* Fetch flight deals from Amadeus API for different destinations.
* Find the cheapest flight and check if it’s below the specified threshold price.
* Send email notifications to customers if a deal is found.

### Step 5: Customize the Application
You can modify the following variables in `flight_deal_finder.py` to adjust the program:
* `ORIGIN_IATA_CODE`: The origin city code (default is 'LON' for London).
* `DEPARTURE_DATE`: The departure date (default is set to 1 day from today).
* `RETURN_DATE`: The return date (default is set to 180 days from today).

### Step 6: Modify the Flight Deals Sheet (Optional)
The `data_manager.py` file retrieves and updates flight deals from the flight deals sheet. Ensure that the sheet is structured with columns like `city`, `iataCode`, and `lowestPrice`.

### Step 7: Email Notification Body Customization (Optional)
In the notification_manager.py file, you can customize the email body for the notifications sent to customers when a flight deal is found.

---

## Troubleshooting
* **API Token Expired**: If you get an error related to the API token being expired, the program will automatically fetch a new token by calling `get_new_token()` in the `FlightSearch` class.
* **No Flights Found**: If no flights are returned from the Amadeus API, ensure that the dates and destinations are valid, and try again.
* **SMTP Authentication Issues**: Ensure that the `SMTP_USER` and `SMTP_PASSWORD` are correct, and if you're using Gmail, check if "Less Secure Apps" or App Passwords are enabled.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgements
* [Amadeus API](https://developers.amadeus.com/) for flight data.
* [Python](https://www.python.org/) for being a versatile programming language.
* [dotenv](https://pypi.org/project/python-dotenv/) for managing environment variables.

