import json
import datetime
import os
from dotenv import load_dotenv
from garminconnect import Garmin

# Load credentials from .env file
load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

client = Garmin(EMAIL, PASSWORD)
client.login()

today = datetime.date.today()
days = 30
summaries = []

for i in range(days):
    day = today - datetime.timedelta(days=i)
    iso = day.isoformat()
    try:
        stats = client.get_stats(iso)
        summaries.append({
            "date": iso,
            "stats": stats
        })
    except Exception as e:
        print(f"Failed to fetch for {iso}: {e}")
        continue

# Merge with existing wellness data
try:
    with open("wellness_history.json", "r") as f:
        previous = json.load(f)
except FileNotFoundError:
    previous = []

existing_dates = {d["date"] for d in previous}
combined = previous + [s for s in summaries if s["date"] not in existing_dates]
combined.sort(key=lambda x: x["date"])

with open("wellness_history.json", "w") as f:
    json.dump(combined, f, indent=2)

print(f"Fetched and saved {len(summaries)} new day(s) of wellness data.")
