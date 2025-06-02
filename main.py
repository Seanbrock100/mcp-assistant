from modules.garmin_sync import get_daily_garmin_data
from modules.runna_scraper import get_today_plan
from modules.home_assistant import notify_user
from logic.suggestions import generate_training_tip

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HA_URL = "http://homeassistant.local:8123"
HA_TOKEN = "YOUR_LONG_LIVED_TOKEN_HERE"
SPEAKER = "media_player.kitchen_speaker"

@app.route("/api/voice_trigger", methods=["POST"])
def voice_trigger():
    data = request.get_json()
    print(f"Wake word triggered by {data.get('device')}")
    say("Hello Sean, I'm ready.")
    return jsonify({"status": "ok"})

def say(message):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "entity_id": SPEAKER,
        "message": message
    }
    requests.post(f"{HA_URL}/api/services/tts/google_translate_say", headers=headers, json=payload)

def run_jarvis():
    garmin_data = get_daily_garmin_data()
    runna_plan = get_today_plan()
    advice = generate_training_tip(garmin_data, runna_plan)
    notify_user(advice)

if __name__ == "__main__":
    run_jarvis()
    app.run(host="0.0.0.0", port=5000)
