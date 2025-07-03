import os
import platform
from actions.utils import speak

def restart_system(command: str = ""):
    speak("Restarting your system now.")
    
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")  # /r = restart, /t 1 = 1-second delay
    elif platform.system() == "Linux":
        os.system("sudo reboot")
    elif platform.system() == "Darwin":  # macOS
        os.system("sudo shutdown -r now")
    else:
        speak("Restart is not supported on this operating system.")
