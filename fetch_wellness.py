import json
import datetime
from garminconnect import Garmin

client = Garmin("your_email", "your_password")
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
    except:
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
