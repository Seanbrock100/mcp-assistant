# ask_mcp.py

from openai import OpenAI
import os
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load trend data
try:
    with open("trend_profile.json") as f:
        trend_data = json.load(f)
except FileNotFoundError:
    trend_data = {}
    print("⚠️ No trend_profile.json found. Responses may be limited.")

# Build system prompt
system_prompt = (
    "You are a highly contextual running and wellness assistant named MCP.\n"
    "Use the user's fitness trends below to answer questions with insight.\n\n"
    f"Here is the current trend profile:\n{json.dumps(trend_data, indent=2)}\n"
)

print("MCP Assistant ready. Type 'exit' to quit.")

# Main loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print("MCP:", reply)

    except Exception as e:
        print("MCP Error:", e)
