import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load Garmin daily data (last 14 days)
try:
    with open("daily_summary.json", "r") as f:
        all_days = json.load(f)

    # Trim down the data to just key metrics
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
    print(f"Error loading or trimming daily_summary.json: {e}")

# Start interaction loop
print("MCP Assistant ready. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        break

    system_message = "You are an intelligent endurance coach and data analyst. Use the Garmin data provided to answer questions."

    user_prompt = f"""
Garmin summary of the last 14 days:

{json.dumps(trimmed_data, indent=2)}

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
