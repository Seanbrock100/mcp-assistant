import os
import requests
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def refresh_access_token():
    url = "https://www.strava.com/oauth/token"
    response = requests.post(url, data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": STRAVA_REFRESH_TOKEN,
    })
    response.raise_for_status()
    return response.json()["access_token"]

def get_activities(access_token, per_page=5):
    url = f"https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params={"per_page": per_page})
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    token = refresh_access_token()
    activities = get_activities(token)
    for act in activities:
        print(f"{act['start_date']} - {act['name']} - {act['distance'] / 1000:.2f} km")
