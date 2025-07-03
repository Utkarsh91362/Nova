import speech_recognition as sr
import random
import time
from actions.utils import speak
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

# 🧠 Core assistant behaviors
def stop_action():
    speak("Very well.")
    time.sleep(1.2)

def shutdown_action():
    speak("Powering off.")
    exit()

core_commands = {
    "stop": stop_action,
    "shut down": shutdown_action,
    "shutdown": shutdown_action,
}

# 🛠️ System control command map (you’ll extend this over time)
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
            print("Try waking Nova...")
            try:
                audio = recognizer.listen(source, timeout=5)
                wake_query = recognizer.recognize_google(audio).lower()
                print("Heard:", wake_query)

                # Allow shutdown without saying "nova"
                matched_shutdown = next(
                    (action for phrase, action in core_commands.items() if phrase in wake_query and "shut" in phrase),
                    None
                )
                if matched_shutdown:
                    matched_shutdown()
                    return

                if "nova" not in wake_query:
                    continue

                print("🎙️ Nova Active...")
                speak(random.choice(wake_responses))

                command = listen_for_command()
                if not command:
                    speak("I didn't catch that.")
                    continue

                # Handle core commands like stop/shutdown
                matched_core = next(
                    (action for phrase, action in core_commands.items() if phrase in command),
                    None
                )
                if matched_core:
                    matched_core()
                    continue

                # Handle mapped system control commands
                matched_system = next(
                    (action for phrase, action in command_map.items() if phrase in command),
                    None
                )
                if matched_system:
                    matched_system()
                    continue

                # Fallback: attempt dynamic application opening
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
