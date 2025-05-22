import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
TOKEN_FILE = "tokens.json"

def save_tokens(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {}

def refresh_access_token(refresh_token):
    print("Refreshing access token...")
    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })
    response.raise_for_status()
    new_tokens = response.json()
    save_tokens(new_tokens)
    return new_tokens

def get_athlete_profile(access_token):
    print("Fetching athlete profile...")
    response = requests.get("https://www.strava.com/api/v3/athlete", headers={
        "Authorization": f"Bearer {access_token}"
    })
    if response.status_code == 401:
        print("Access token invalid or expired. Attempting to refresh...")
        raise Exception("TokenExpired")
    response.raise_for_status()
    return response.json()

def main():
    tokens = load_tokens()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if not access_token or not refresh_token:
        print("Error: Missing tokens in tokens.json.")
        return

    try:
        athlete = get_athlete_profile(access_token)
        print("Athlete:", json.dumps(athlete, indent=2))
    except Exception as e:
        if str(e) == "TokenExpired":
            tokens = refresh_access_token(refresh_token)
            access_token = tokens["access_token"]
            athlete = get_athlete_profile(access_token)
            print("Athlete (after refresh):", json.dumps(athlete, indent=2))
        else:
            print("Unhandled error:", e)

if __name__ == "__main__":
    main()
