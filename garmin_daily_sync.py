from garminconnect import Garmin
from dotenv import load_dotenv
import datetime
import os
import json
from pathlib import Path

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

# Create date-stamped filename
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"{today_str}.json"

try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()

    print(f"Fetching Garmin data for {today_str}...")

    # Get core data
    activities = client.get_activities(0, 5)
    stats = client.get_stats(today)
    sleep = client.get_sleep_data(today)
    steps = client.get_steps_data(today)
    heart_rate = client.get_heart_rates(today)

    data = {
        "date": today_str,
        "summary": stats,
        "sleep": sleep,
        "steps": steps,
        "heart_rate": heart_rate,
        "activities": activities
    }

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Data saved to {output_file}")

except Exception as e:
    print(f"Failed to fetch Garmin data: {e}")
