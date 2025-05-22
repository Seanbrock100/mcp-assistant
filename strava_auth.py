import os
from dotenv import load_dotenv
from stravalib.client import Client

ENV_FILE = ".env"

def update_env(tokens):
    """Update .env with new tokens."""
    try:
        with open(ENV_FILE, "r") as file:
            lines = file.readlines()

        with open(ENV_FILE, "w") as file:
            for line in lines:
                if line.startswith("STRAVA_ACCESS_TOKEN="):
                    file.write(f'STRAVA_ACCESS_TOKEN={tokens["access_token"]}\n')
                elif line.startswith("STRAVA_REFRESH_TOKEN="):
                    file.write(f'STRAVA_REFRESH_TOKEN={tokens["refresh_token"]}\n')
                else:
                    file.write(line)
    except Exception as e:
        print("Failed to update .env file:", e)

def print_tokens(label, token_data):
    print(f"\n{label} Tokens:")
    for k, v in token_data.items():
        if 'token' in k:
            print(f"{k}: {v}")

def main():
    load_dotenv()

    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    access_token = os.getenv("STRAVA_ACCESS_TOKEN")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    # Validate environment variables
    if not all([client_id, client_secret, access_token, refresh_token]):
        print("ERROR: Missing required credentials in .env file.")
        print("Ensure STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, STRAVA_ACCESS_TOKEN, and STRAVA_REFRESH_TOKEN are set.")
        return

    token_data = {
        "STRAVA_ACCESS_TOKEN": access_token,
        "STRAVA_REFRESH_TOKEN": refresh_token
    }
    print_tokens("Loaded", token_data)

    client = Client()
    client.access_token = access_token

    try:
        athlete = client.get_athlete()
        print(f"\nAuthenticated as: {athlete.firstname} {athlete.lastname}")
    except Exception as e:
        print("\nAccess token invalid or expired. Attempting refresh...")
        try:
            token_response = client.refresh_access_token(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token
            )
            client.access_token = token_response['access_token']
            update_env(token_response)
            print_tokens("Refreshed", token_response)
        except Exception as refresh_error:
            print("ERROR: Failed to refresh token.")
            print(refresh_error)
            return

    try:
        print("\nFetching latest activities...")
        activities = client.get_activities(limit=5)
        for activity in activities:
            print(f"- {activity.name} on {activity.start_date_local} ({activity.distance} m)")
    except Exception as fetch_error:
        print("ERROR: Failed to fetch activities.")
        print(fetch_error)

if __name__ == "__main__":
    main()
