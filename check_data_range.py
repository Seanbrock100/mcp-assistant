from datetime import datetime
import json

def get_date_range(data, key):
    dates = [d.get(key) for d in data if d.get(key)]
    dates = [datetime.fromisoformat(d[:10]) for d in dates]
    return min(dates).date(), max(dates).date()

with open("run_history.json") as f:
    runs = json.load(f)
with open("wellness_history.json") as f:
    wellness = json.load(f)

start_r, end_r = get_date_range(runs, "start")
start_w, end_w = get_date_range(wellness, "date")

print(f"Workout data range: {start_r} to {end_r}")
print(f"Wellness data range: {start_w} to {end_w}")
