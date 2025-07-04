### ✅ File: actions/productivity_and_tools/clock/clock_commands.py

import re
from datetime import datetime, timedelta
from actions.utils import speak
from .alarm_utils import load_alarms, save_alarms

def set_alarm(command: str):
    try:
        match = re.search(r"(tomorrow\s*)?(\d{1,2})(:(\d{2}))?\s*(a\.?m\.?|p\.?m\.?)?", command.lower())
        if not match:
            speak("I didn't understand the time. Try saying something like 'set alarm for 7:30 a.m. tomorrow'.")
            return

        is_tomorrow = bool(match.group(1))
        hour = int(match.group(2))
        minute = int(match.group(4)) if match.group(4) else 0
        period = match.group(5)

        # Convert to 24-hour format
        if period:
            if "p" in period and hour < 12:
                hour += 12
            elif "a" in period and hour == 12:
                hour = 0

        # Calculate alarm datetime
        now = datetime.now()
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if is_tomorrow or alarm_time <= now:
            alarm_time += timedelta(days=1)

        # Add to alarms.json
        alarms = load_alarms()
        alarms.append({
            "time": alarm_time.strftime("%Y-%m-%d %H:%M"),
            "label": "Alarm"
        })
        save_alarms(alarms)

        speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}.")

    except Exception as e:
        print("Alarm error:", e)
        speak("Something went wrong while setting the alarm.")

def tell_time(_command: str):
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The current time is {current_time}")
