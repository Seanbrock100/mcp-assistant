import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialise OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Load Daily Summary Data (unchanged) ----
try:
    with open("daily_summary.json", "r") as f:
        all_days = json.load(f)

    # Reduce to recent 14 days and trim
    trimmed_data = []
    for day in all_days[-14:]:
        trimmed_data.append({
            "date": day.get("date"),
            "averageHR": day.get("stats", {}).get("averageHR"),
            "steps": day.get("stats", {}).get("totalSteps"),
            "calories": day.get("stats", {}).get("totalKilocalories"),
            "distance_m": day.get("stats", {}).get("totalDistanceMeters"),
        })
except Exception as e:
    trimmed_data = []
    print(f"Error loading daily_summary.json: {e}")

# ---- STEP 2 START: Load Recent Activity Data ----
try:
    with open("recent_activities.json", "r") as f:
        activity_data = json.load(f)
except Exception as e:
    activity_data = []
    print(f"Error loading recent_activities.json: {e}")
# ---- STEP 2 END ----

# ---- Assistant Loop ----
print("MCP Assistant ready. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        break

    system_message = "You are an intelligent endurance coach and data analyst. Use Garmin data to help evaluate training and health."

    user_prompt = f"""
Here is my Garmin wellness summary from the past 14 days:
{json.dumps(trimmed_data, indent=2)}

Here is a list of my last 30 recorded workouts:
{json.dumps(activity_data, indent=2)}

Now answer this question:
{user_input}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print(f"MCP: {reply}\n")
    except Exception as e:
        print(f"MCP Error: {e}")
