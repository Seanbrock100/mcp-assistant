def generate_training_tip(garmin_data, runna_plan):
    if garmin_data["sleep_score"] < 60:
        return "You slept poorly. Consider swapping for a recovery run."
    if garmin_data["hrv"] < 50:
        return "Low HRV detected. Keep intensity low today."
    return f"Proceed with your {runna_plan['session']} - looks good!"
