import os
import subprocess
from difflib import get_close_matches
from actions.utils import speak, listen_for_command

# 🎯 Predefined command mappings
custom_app_commands = {
    "browser": "chrome",
    "chrome": "chrome",
    "brave": "brave",
    "edge": "msedge",
    "microsoft edge": "msedge"
}

def open_application(command: str):
    app_name = command.replace("open", "").strip().lower()

    # 🔁 Handle custom mapped commands like browsers
    executable = custom_app_commands.get(app_name)
    if executable:
        os.system(f"start {executable}")
        speak(f"Opening {app_name}")
        return

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
        app_map = {app["Name"].lower(): app["AppID"] for app in apps}

        # 🎯 Exact match
        for name, app_id in app_map.items():
            if app_name in name:
                os.system(f'start "" shell:AppsFolder\\{app_id}')
                speak(f"Opening {name}")
                return

        # 🤖 Suggest close match
        close_matches = get_close_matches(app_name, app_map.keys(), n=1, cutoff=0.6)
        if close_matches:
            suggestion = close_matches[0]
            speak(f"Did you mean {suggestion}?")
            print("🎤 Listening for confirmation...")
            response = listen_for_command()
            print("🔁 Heard response:", response)

            if response and any(word in response for word in [
                "yes", "you may", "yup", "yep", "yeah", "sure", "do that", "open", suggestion
            ]):
                os.system(f'start "" shell:AppsFolder\\{app_map[suggestion]}')
                speak(f"Opening {suggestion}")
            else:
                speak("Okay, not opening anything.")
        else:
            speak(f"I couldn't find anything like {app_name} on your system.")

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong trying to open the app.")
