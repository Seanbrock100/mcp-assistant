import os
from dotenv import load_dotenv
from stravalib.client import Client

# Load environment variables from .env
load_dotenv()

# Retrieve credentials from the environment
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

# Ensure the token exists
if not ACCESS_TOKEN:
    print("Error: STRAVA_ACCESS_TOKEN is missing from environment.")
    exit(1)

# Initialize the Strava client
client = Client()
client.access_token = ACCESS_TOKEN

try:
    print("Fetching latest activities from Strava...")
    activities = client.get_activities(limit=5)

    print("\nRecent Activities:")
    for activity in activities:
        print(f"- {activity.name} | {activity.start_date} | {activity.distance}m")

except Exception as e:
    print(f"Error while fetching activities: {e}")
