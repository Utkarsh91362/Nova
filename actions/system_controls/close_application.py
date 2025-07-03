import os
import psutil
import subprocess
from difflib import get_close_matches
from actions.utils import speak, listen_for_command

def close_application(command: str):
    app_name = command.replace("close", "").strip().lower()

    matches = []
    bg_matches = []
    window_matches = []

    for p in psutil.process_iter(['pid', 'name']):
        try:
            pname = p.info['name'].lower()
            if app_name in pname or get_close_matches(app_name, [pname], cutoff=0.7):
                matches.append(p)
                try:
                    if p.windows()[0].title():
                        window_matches.append(p)
                    else:
                        bg_matches.append(p)
                except Exception:
                    bg_matches.append(p)
        except Exception:
            continue

    if not matches:
        # Try fallback with PowerShell (UWP apps)
        try:
            script = f'''
            $found = Get-Process | Where-Object {{
                $_.MainWindowTitle -and $_.MainWindowTitle.ToLower().Contains("{app_name}")
            }}
            if ($found) {{
                $found | ForEach-Object {{ $_.CloseMainWindow() | Out-Null }}
                Write-Output "Closed"
            }} else {{
                Write-Output "NotRunning"
            }}
            '''
            result = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True)
            if "Closed" in result.stdout:
                speak(f"Closed {app_name}")
            else:
                speak(f"{app_name} is not running right now.")
        except Exception as e:
            print("Error:", e)
            speak("Something went wrong trying to close the app.")
        return

    if len(matches) == 1:
        try:
            matches[0].terminate()
            speak(f"Closed {app_name}")
        except:
            speak(f"Failed to close {app_name}")
        return

    # Multiple matches
    speak(f"I found {len(matches)} instances of {app_name}. Should I close all?")
    print("🎤 Listening for confirmation...")
    response = listen_for_command()
    print("🔁 Heard response:", response)

    if response and any(word in response for word in ["yes", "yup", "do that", "sure", "close all", "yeah"]):
        for p in matches:
            try:
                p.terminate()
            except:
                continue
        speak(f"Closed all {app_name} windows.")
    elif response and "current" in response:
        if window_matches:
            try:
                window_matches[0].terminate()
                speak(f"Closed the current window of {app_name}")
            except:
                speak("Couldn't close the current window.")
        else:
            speak("I couldn't detect a current window.")
    elif response and "background" in response:
        if bg_matches:
            for p in bg_matches:
                try:
                    p.terminate()
                except:
                    continue
            speak(f"Closed background {app_name} processes.")
        else:
            speak("No background processes found.")
    else:
        speak("Okay, not closing anything.")
