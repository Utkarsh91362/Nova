import os
from actions.utils import speak

def open_file_explorer():
    speak("Opening File Explorer!")
    os.system("explorer")
