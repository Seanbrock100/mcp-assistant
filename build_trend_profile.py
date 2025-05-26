# build_trend_profile.py

import json
from datetime import datetime

def avg(values):
    nums = [v for v in values if isinstance(v, (int, float))]
    return round(sum(nums) / len(nums), 2) if nums else None

# Load running data
with open("recent_activities.json") as f:
    runs = json.load(f)

# Load wellness data
with open("daily_summary.json") as f:
    wellness = json.load(f)

# --- Process run data ---
run_metrics = {
    "average_pace_min_per_km": [],
    "averageHR": [],
    "vo2max": [],
    "distance_km": []
}

for run in runs:
    duration = run.get("duration_s")
    distance_m = run.get("distance_m")
    pace = (duration / 60) / (distance_m / 1000) if duration and distance_m else None
    if pace: run_metrics["average_pace_min_per_km"].append(pace)
    if run.get("averageHR"): run_metrics["averageHR"].append(run["averageHR"])
    if run.get("vo2max"): run_metrics["vo2max"].append(run["vo2max"])
    if distance_m: run_metrics["distance_km"].append(distance_m / 1000)

# --- Process wellness data ---
steps = []
calories = []

for day in wellness:
    stats = day.get("stats", {})
    steps.append(stats.get("totalSteps"))
    calories.append(stats.get("totalKilocalories"))

# --- Final trend object ---
trend_profile = {
    "running": {
        "average_pace_min_per_km": avg(run_metrics["average_pace_min_per_km"]),
        "average_heart_rate": avg(run_metrics["averageHR"]),
        "average_vo2max": avg(run_metrics["vo2max"]),
        "average_distance_km": avg(run_metrics["distance_km"]),
        "total_runs": len(run_metrics["averageHR"]),
    },
    "wellness": {
        "average_daily_steps": avg(steps),
        "average_daily_calories": avg(calories),
        "days_tracked": len(steps),
    },
    "last_updated": datetime.now().isoformat()
}

# Save
with open("trend_profile.json", "w") as f:
    json.dump(trend_profile, f, indent=2)

print("✅ Trend profile built and saved to trend_profile.json")
