from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)
from dotenv import load_dotenv
import datetime
import os

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

try:
    # Authenticate
    client = Garmin(EMAIL, PASSWORD)
    client.login()
    print("Login successful.")

    today = datetime.date.today().isoformat()

    # Fetch data
    activities = client.get_activities(0, 1)
    stats = client.get_stats(today)
    steps = client.get_steps_data(today)

    print("\nLatest Activity:")
    print(activities[0])

    print("\nDaily Summary:")
    print(stats)

    print("\nSteps:")
    print(steps)

except GarminConnectAuthenticationError:
    print("Authentication failed: Invalid credentials.")
except GarminConnectConnectionError:
    print("Connection error.")
except GarminConnectTooManyRequestsError:
    print("Rate limit hit.")
except Exception as e:
    print(f"Unexpected error: {e}")
