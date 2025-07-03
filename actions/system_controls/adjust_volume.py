# actions/system_controls/adjust_volume.py

import re
from actions.utils import speak
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

def adjust_volume(command: str):
    # Setup volume interface
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

    command = command.lower()

    # Mute or unmute
    if "mute" in command and "unmute" not in command:
        volume_interface.SetMute(1, None)
        speak("Muted.")
        return
    elif "unmute" in command:
        volume_interface.SetMute(0, None)
        speak("Unmuted.")
        return

    # Get current volume level (0.0 to 1.0)
    current_volume = volume_interface.GetMasterVolumeLevelScalar()

    # Match exact volume set (1–10)
    match_set = re.search(r"(?:set volume to|volume at|volume level)\s*(\d+)", command)
    if match_set:
        level = int(match_set.group(1))
        if 1 <= level <= 10:
            volume_interface.SetMasterVolumeLevelScalar(level / 10.0, None)
            speak(f"Volume set to {level * 10} percent.")
        else:
            speak("Please choose a volume between 1 and 10.")
        return

    # Match increase/decrease volume
    match_adjust = re.search(r"(increase|decrease)\s+volume\s*(?:by)?\s*(\d+)?", command)
    if match_adjust:
        direction = match_adjust.group(1)
        amount = int(match_adjust.group(2) or 1)
        delta = (amount * 0.1) if direction == "increase" else -(amount * 0.1)
        new_volume = min(1.0, max(0.0, current_volume + delta))
        volume_interface.SetMasterVolumeLevelScalar(new_volume, None)
        speak(f"Volume {direction}d.")
        return

    speak("I couldn't understand the volume command.")
