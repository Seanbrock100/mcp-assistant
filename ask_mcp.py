import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load last 14 days of wellness data
try:
    with open("wellness_history.json", "r") as f:
        all_days = json.load(f)
except:
    all_days = []

trimmed_data = []
for day in all_days[-14:]:
    trimmed_data.append({
        "date": day.get("date"),
        "averageHR": day.get("stats", {}).get("averageHR"),
        "steps": day.get("stats", {}).get("totalSteps"),
        "calories": day.get("stats", {}).get("totalKilocalories"),
        "distance_m": day.get("stats", {}).get("totalDistanceMeters"),
    })

# Load last 30 activities
try:
    with open("run_history.json", "r") as f:
        activity_data = json.load(f)
except:
    activity_data = []

activity_data = activity_data[-30:]

print("MCP Assistant ready. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        break

    system_message = "You are a highly intelligent training assistant that analyses Garmin health and activity data to advise on fitness, fatigue, and performance trends."

    user_prompt = f"""
Here is my Garmin wellness summary from the past 14 days:
{json.dumps(trimmed_data, indent=2)}

Here are my last 30 recorded workouts:
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
