import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_activities():
    token = os.getenv("STRAVA_ACCESS_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities?per_page=5",
        headers=headers
    )
    response.raise_for_status()
    return response.json()

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
