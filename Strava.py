import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

def refresh_access_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }
    response = requests.post("https://www.strava.com/api/v3/oauth/token", headers=headers, data=data)
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
    try:
        print("Attempting to fetch activities with current access token...")
        activities = get_activities(ACCESS_TOKEN)
    except requests.exceptions.HTTPError as e:
        print("Access token may be expired. Attempting to refresh...")
        ACCESS_TOKEN = refresh_access_token()
        try:
            activities = get_activities(ACCESS_TOKEN)
        except requests.exceptions.HTTPError as e2:
            print("Failed even after refreshing token:", e2)
            activities = None

    if activities:
        print("Recent activities:", activities)
    else:
        print("No activities retrieved.")
