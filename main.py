from strava_auth import get_strava_client

if __name__ == "__main__":
    client = get_strava_client()
    activities = client.get_activities(limit=5)

    for activity in activities:
        print(f"{activity.name} - {activity.distance}m in {activity.moving_time}")
