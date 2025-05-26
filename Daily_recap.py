import json
from datetime import datetime, timedelta

# Load data
with open("trend_profile.json") as f:
    trends = json.load(f)

with open("recent_activities.json") as f:
    activities = json.load(f)

with open("wellness_history.json") as f:
    wellness = json.load(f)

# Extract yesterday’s date
yesterday = (datetime.now() - timedelta(days=1)).date()

# Find the wellness record for yesterday
yesterday_data = next((entry["stats"] for entry in wellness if entry["date"] == str(yesterday)), None)

# Find the most recent running activity
latest_run = next((act for act in activities if act["type"] == "running"), None)

# Build recap
messages = []

if yesterday_data:
    rhr = yesterday_data.get("restingHeartRate")
    sleep_sec = yesterday_data.get("sleepingSeconds", 0)
    stress = yesterday_data.get("averageStressLevel")
    steps = yesterday_data.get("totalSteps", 0)
    sleep_hours = round(sleep_sec / 3600, 1)

    messages.append(f"Yesterday you slept for {sleep_hours} hours and took {steps:,} steps.")
    
    if rhr and rhr < trends["wellness"]["average_daily_calories"] * 0.025:
        messages.append("Your resting heart rate was lower than usual — a sign of good recovery.")
    if stress is not None:
        if stress < 20:
            messages.append("Your stress was low, which is great.")
        elif stress > 40:
            messages.append("Stress was elevated — keep that in mind today.")
else:
    messages.append("No wellness data available for yesterday.")

if latest_run:
    hr = latest_run.get("averageHR")
    pace = latest_run.get("distance_m", 0) / (latest_run.get("duration_s", 1) / 60) / 1000  # km/min
    pace_min_per_km = round(1 / pace, 2) if pace else None
    messages.append(f"Your last run averaged {hr} bpm at {pace_min_per_km} min/km.")
    
    if hr and hr > trends["running"]["average_heart_rate"] + 5:
        messages.append("That’s a bit higher than your average — maybe ease up today.")
    else:
        messages.append("That’s in line with your usual effort.")

# Final recommendation
if "Stress was elevated" in messages[-1] or (yesterday_data and yesterday_data.get("sleepingSeconds", 0) < 6 * 3600):
    messages.append("Consider an easier session or even rest today.")
else:
    messages.append("Looks like a good day for a quality workout!")

# Output result
print("\n".join(messages))
