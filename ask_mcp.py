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
        recent_data = all_days[-14:]
except Exception as e:
    recent_data = []
    print(f"Error loading daily_summary.json: {e}")

print("MCP Assistant ready. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        break

    system_message = "You are an intelligent endurance coach and data analyst. Use Garmin data to answer fitness and recovery questions."

    user_prompt = f"""
Garmin daily summary for the past 14 days:
{json.dumps(recent_data, indent=2)}

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
