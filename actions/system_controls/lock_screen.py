import os
from actions.utils import speak

def lock_screen(command=None):
    speak("Locking your screen.")
    os.system("rundll32.exe user32.dll,LockWorkStation")
