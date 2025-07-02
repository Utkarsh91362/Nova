import speech_recognition as sr
import random
import time
from actions.utils import speak  # import speak from utils

# Wake response options
wake_responses = [
    "Yes?",
    "How can I help you?",
    "What can I do for you today?",
    "I'm listening.",
    "How may I be of assistance?"
]

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=7)
            command = recognizer.recognize_google(audio)
            print("Command:", command)
            return command
        except:
            return None

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Nova is on standby...")

        while True:
            try:
                print("Try waking Nova...")
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio).lower()
                print("Heard:", query)

                if "shut down" in query or "shutdown" in query:
                    speak("Powering off.")
                    break

                elif "nova" in query:
                    print("🎙️ Nova Active...")
                    speak(random.choice(wake_responses))

                    command = listen_for_command()
                    if command:
                        command = command.lower()

                        if "stop" in command:
                            speak("Very well.")
                            time.sleep(1.2)
                            continue
                        elif "shut down" in command or "shutdown" in command:
                            speak("Powering off.")
                            break
                        else:
                            speak(f"You said: {command}")
                            time.sleep(1.2)
                    else:
                        speak("I didn't catch that.")
                        time.sleep(1.2)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"❌ Could not request results: {e}")
