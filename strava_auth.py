import os
from dotenv import load_dotenv
from stravalib.client import Client

load_dotenv()

def get_strava_client():
    client = Client()
    client.access_token = os.getenv("STRAVA_ACCESS_TOKEN")

    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")

    if client.access_token and refresh_token:
        try:
            client.get_activities(limit=1)
        except:
            print("Refreshing token...")
            token_response = client.refresh_access_token(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token
            )
            client.access_token = token_response['access_token']
            print("New access token:", client.access_token)

    return client
