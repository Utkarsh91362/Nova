import speech_recognition as sr
import random
import time
import threading
from actions.utils import *
from actions.system_controls.open_application import open_application

# 🌟 Wake responses
wake_responses = [
    "Yes?",
    "How can I help you?",
    "What can I do for you today?",
    "I'm listening.",
    "How may I be of assistance?",
    "hmmm"
]

# 🔄 Thread for speaking
speaking_thread = None

def speak_async(text):
    global speaking_thread
    if speaking_thread and speaking_thread.is_alive():
        stop_speaking()
    speaking_thread = threading.Thread(target=speak, args=(text,))
    speaking_thread.start()

# 🧠 Core assistant behaviors
def stop_action():
    speak_async("Very well.")
    time.sleep(1.2)

def shutdown_action():
    speak_async("Powering off.")
    time.sleep(1.2)
    exit()

core_commands = {
    "stop": stop_action,
    "shut down": shutdown_action,
    "shutdown": shutdown_action,
}

# 🛠️ System control command map (extendable)
command_map = {
    # "lock screen": lock_screen,
    # "take screenshot": take_screenshot,
}

# 🎤 Listen for one command
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=8)
            command = recognizer.recognize_google(audio).lower()
            print("Command:", command)
            return command
        except:
            return None

# 🚀 Nova's main loop
def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Nova is on standby...")

        while True:
            try:
                print("Try waking Nova...")
                audio = recognizer.listen(source, timeout=5)
                wake_query = recognizer.recognize_google(audio).lower()
                print("Heard:", wake_query)

                # 🔌 Allow shutdown without saying Nova
                shutdown_match = next(
                    (action for phrase, action in core_commands.items() if phrase in wake_query and "shut" in phrase),
                    None
                )
                if shutdown_match:
                    shutdown_match()
                    return

                # 🔄 Interrupt speech if Nova is heard
                if "nova" not in wake_query:
                    continue

                stop_speaking()  # ⛔ Interrupt current speech
                print("🎙️ Nova Active...")
                speak_async(random.choice(wake_responses))

                command = listen_for_command()
                if not command:
                    speak_async("I didn't catch that.")
                    continue

                # 👋 Dismiss listening if user says nevermind
                if is_dismiss_command(command):
                    speak_async("Okaaay.")
                    continue

                # Handle core commands
                core_match = next((a for k, a in core_commands.items() if k in command), None)
                if core_match:
                    core_match()
                    continue

                # Handle system control mapped commands
                system_match = next((a for k, a in command_map.items() if k in command), None)
                if system_match:
                    system_match()
                    continue

                # 🧠 Fallback: try dynamic app open
                open_application(command)

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"❌ Could not request results: {e}")

# 🟢 Start Nova
if __name__ == "__main__":
    main()
