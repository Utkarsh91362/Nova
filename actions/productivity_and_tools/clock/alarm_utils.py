# actions/productivity_and_tools/clock/alarm_utils.py

import json
from pathlib import Path

ALARMS_FILE = Path(__file__).parent / "alarms.json"

def load_alarms():
    if not ALARMS_FILE.exists():
        return []
    with open(ALARMS_FILE, "r") as f:
        return json.load(f)

def save_alarms(alarms):
    with open(ALARMS_FILE, "w") as f:
        json.dump(alarms, f, indent=2)
