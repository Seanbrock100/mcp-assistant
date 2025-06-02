from modules.garmin_sync import get_daily_garmin_data
from modules.runna_scraper import get_today_plan
from modules.home_assistant import notify_user
from logic.suggestions import generate_training_tip

def run_jarvis():
    garmin_data = get_daily_garmin_data()
    runna_plan = get_today_plan()
    advice = generate_training_tip(garmin_data, runna_plan)
    notify_user(advice)

if __name__ == "__main__":
    run_jarvis()
