from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)
from dotenv import load_dotenv
import datetime
import os

# Load credentials from .env file
load_dotenv()
email = os.getenv("GARMIN_USERNAME")
password = os.getenv("GARMIN_PASSWORD")

try:
    client = Garmin(email, password)
    client.login()

    today = datetime.date.today()

    # Get today’s summary data
    daily_summary = client.get_stats(today)
    print("Daily Summary:", daily_summary)

    # Get latest activity
    activities = client.get_activities(0, 1)
    print("Most Recent Activity:", activities[0])

except GarminConnectAuthenticationError:
    print("Authentication error: Check your Garmin username/password.")
except GarminConnectConnectionError:
    print("Connection error: Could not connect to Garmin.")
except GarminConnectTooManyRequestsError:
    print("Rate limit exceeded: Too many requests to Garmin API.")
