# actions/system_controls/adjust_brightness.py
import re
import subprocess
from actions.utils import speak

def adjust_brightness(command: str):
    def get_current_brightness():
        result = subprocess.run(["powershell", "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"], capture_output=True, text=True)
        try:
            return int(result.stdout.strip().splitlines()[-1])
        except:
            return 50

    current = get_current_brightness()
    current_level = round(current / 10)

    delta_match = re.search(r"(increase|raise|up|decrease|lower|reduce)\s+brightness\s+(by\s+)?(\d+)", command)
    absolute_match = re.search(r"(set|brightness)\s+(to\s+)?(\d+)", command)

    if delta_match:
        change = int(delta_match.group(3))
        if any(w in command for w in ["decrease", "lower", "reduce"]):
            new_level = max(1, current_level - change)
        else:
            new_level = min(10, current_level + change)
    elif absolute_match:
        new_level = int(absolute_match.group(3))
        new_level = max(1, min(10, new_level))
    else:
        speak("Please say a valid brightness level.")
        return

    brightness = new_level * 10
    subprocess.run(["powershell", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})"], shell=True)
    speak(f"Brightness set to {brightness} percent.")
