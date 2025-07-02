import os
import subprocess
from actions.utils import speak

def open_application(command: str):
    app_name = command.replace("open", "").strip().lower()

    # Use PowerShell to get all UWP app names and IDs
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-StartApps | ConvertTo-Json"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            speak("I couldn't access installed applications.")
            return

        import json
        apps = json.loads(result.stdout)
        app_map = {}

        for app in apps:
            name = app["Name"].lower()
            app_id = app["AppID"]
            app_map[name] = app_id

        matched_app = None
        for name in app_map:
            if app_name in name:
                matched_app = app_map[name]
                break

        if matched_app:
            os.system(f'start "" shell:AppsFolder\\{matched_app}')
            speak(f"Opening {app_name}")
        else:
            speak(f"I couldn't find {app_name} on your system.")

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong trying to open the app.")
