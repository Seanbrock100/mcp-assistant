# garmin_daily_sync.py

from garminconnect import Garmin
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)
from dotenv import load_dotenv
import os
import json
import datetime

# Load credentials
load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()

    today = datetime.date.today().isoformat()

    # Fetch sleep, stress, resting HR, body battery
    sleep = client.get_sleep_data(today)
    stress = client.get_stress_data(today)
    resting_hr = client.get_heart_rates(today)
    body_battery = client.get_body_battery(today)
    stats = client.get_stats(today)

    daily = {
        "date": today,
        "sleep": sleep,
        "stress": stress,
        "resting_hr": resting_hr,
        "body_battery": body_battery,
        "summary": stats
    }

    # Append to file
    file_path = "wellness_history.json"
    if os.path.exists(file_path):
        with open(file_path) as f:
            data = json.load(f)
    else:
        data = []

    # Remove existing entry for today if it exists
    data = [d for d in data if d["date"] != today]
    data.append(daily)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Synced sleep, stress, and HR data.")

except GarminConnectAuthenticationError:
    print("❌ Authentication failed.")
except GarminConnectConnectionError:
    print("❌ Connection error.")
except GarminConnectTooManyRequestsError:
    print("❌ Rate limit hit.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
