from garminconnect import Garmin
from dotenv import load_dotenv
import os
import json

load_dotenv()

EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()
    print("Login successful.")

    activities = client.get_activities(0, 30)  # fetch 30 most recent

    extracted = []
    for a in activities:
        extracted.append({
            "start": a.get("startTimeLocal"),
            "type": a.get("activityType", {}).get("typeKey"),
            "name": a.get("activityName"),
            "distance_m": a.get("distance"),
            "duration_s": a.get("duration"),
            "averageHR": a.get("averageHR"),
            "maxHR": a.get("maxHR"),
            "vo2max": a.get("vO2MaxValue"),
            "calories": a.get("activeKilocalories")
        })

    with open("recent_activities.json", "w") as f:
        json.dump(extracted, f, indent=2)

    print("Saved to recent_activities.json")

except Exception as e:
    print("Error fetching Garmin activities:", e)
