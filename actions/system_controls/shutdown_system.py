import os
import platform
from actions.utils import speak

def shutdown_system(command: str = ""):
    speak("Shutting down your system now.")
    
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")  # /s = shutdown, /t 1 = 1-second delay
    elif platform.system() == "Linux":
        os.system("sudo shutdown now")
    elif platform.system() == "Darwin":  # macOS
        os.system("sudo shutdown -h now")
    else:
        speak("Shutdown is not supported on this operating system.")
