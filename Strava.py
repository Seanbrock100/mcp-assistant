import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def refresh_access_token():
    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    })
    response.raise_for_status()
    new_token = response.json()['access_token']
    print("Refreshed token:", new_token)
    return new_token

def get_activities(token):
    url = "https://www.strava.com/api/v3/athlete/activities?per_page=5"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    access_token = refresh_access_token()  # always refresh for now
    try:
        activities = get_activities(access_token)
        print("Recent activities:")
        for act in activities:
            print(f"- {act['name']} ({act['distance']}m)")
    except requests.exceptions.HTTPError as e:
        print("Failed to get activities:", e)
