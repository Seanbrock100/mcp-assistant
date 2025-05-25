import json
import datetime
from garminconnect import Garmin

# Assume authentication done
client = Garmin("your_email", "your_password")
client.login()

# Fetch recent activities
activities = client.get_activities(0, 100)  # Fetch more if needed

extracted = []
for a in activities:
    extracted.append({
        "start": a.get("startTimeLocal"),
        "type": a.get("activityType", {}).get("typeKey"),
        "name": a.get("activityName"),
        "distance_m": a.get("distance"),
        "duration_s": a.get("duration"),
        "average_pace_min_per_km": round((a.get("duration") / (a.get("distance") / 1000)) / 60, 2) if a.get("distance") else None,
        "averageHR": a.get("averageHR"),
        "maxHR": a.get("maxHR"),
        "vo2max": a.get("vO2MaxValue"),
        "calories": a.get("activeKilocalories")
    })

# Merge with history
try:
    with open("run_history.json", "r") as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

existing_starts = {a["start"] for a in history}
combined = history + [a for a in extracted if a["start"] not in existing_starts]
combined.sort(key=lambda x: x["start"])

with open("run_history.json", "w") as f:
    json.dump(combined, f, indent=2)
