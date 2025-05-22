import os
from stravalib.client import Client
from dotenv import load_dotenv

ENV_FILE = ".env"

def update_env(tokens):
    lines = []
    with open(ENV_FILE, "r") as file:
        for line in file:
            if line.startswith("STRAVA_ACCESS_TOKEN="):
                lines.append(f'STRAVA_ACCESS_TOKEN={tokens["access_token"]}\n')
            elif line.startswith("STRAVA_REFRESH_TOKEN="):
                lines.append(f'STRAVA_REFRESH_TOKEN={tokens["refresh_token"]}\n')
            elif line.strip() != "":
                lines.append(line)
    with open(ENV_FILE, "w") as file:
        file.writelines(lines)

def main():
    load_dotenv()

    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("Missing one or more required .env variables.")
        return

    client = Client()
    
    try:
        print("Refreshing tokens...")
        token_response = client.refresh_access_token(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token
        )

        # Save updated tokens back to .env
        update_env(token_response)

        client.access_token = token_response["access_token"]

        print("Fetching latest activities from Strava...")
        activities = client.get_activities(limit=5)
        for activity in activities:
            print(f"{activity.name} on {activity.start_date_local} - {activity.distance} m")

    except Exception as e:
        print("Failed to fetch activities:", str(e))

if __name__ == "__main__":
    main()
