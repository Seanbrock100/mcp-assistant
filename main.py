import os
import requests

# Load environment variables
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# Step 1: Exchange refresh token for access token
def get_access_token():
    response = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": STRAVA_REFRESH_TOKEN
    })
    response.raise_for_status()
    return response.json()["access_token"]

# Step 2: Fetch recent activities
def get_recent_activities(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("MCP Assistant is online.")
    token = get_access_token()
    activities = get_recent_activities(token)

    for act in activities[:5]:  # Show latest 5
        print(f"{act['name']} - {act['distance']/1000:.2f} km - Avg HR: {act.get('average_heartrate', 'N/A')}")
