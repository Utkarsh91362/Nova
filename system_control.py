import os
import pyttsx3

engine= pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_file_explorer():
    speak("Opening File Explorer!")
    os.system("explorer")