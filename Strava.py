import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

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
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        activities = get_activities(ACCESS_TOKEN)
    except requests.exceptions.HTTPError as e:
        print("Access token likely expired, refreshing...")
        ACCESS_TOKEN = refresh_access_token()
        activities = get_activities(ACCESS_TOKEN)

    print("Latest activities:")
    for activity in activities:
        print(f"- {activity['name']} ({activity['distance']/1000:.2f} km, {activity['moving_time']//60} min)")
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
