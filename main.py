import speech_recognition as sr
import random
import time
import threading

from actions.utils import *
from actions.system_controls.open_application import open_application
from actions.system_controls.close_application import close_application
from actions.system_controls.lock_screen import lock_screen
from actions.system_controls.screenshot import take_screenshot
from actions.system_controls.adjust_volume import adjust_volume
from actions.system_controls.adjust_brightness import adjust_brightness
from actions.system_controls.restart_system import restart_system
from actions.system_controls.shutdown_system import shutdown_system
from actions.browser_and_internet.open_website import open_website
from actions.browser_and_internet.web_query import web_query
from actions.productivity_and_tools.clock.clock_commands import (
    set_alarm, tell_time
)

# 🌟 Wake responses
wake_responses = [
    "Yes?", "How can I help you?", "What can I do for you today?",
    "I'm listening.", "How may I be of assistance?", "Hmm?"
]

# ⭮️ Threaded speak
speaking_thread = None
def speak_async(text):
    global speaking_thread
    if speaking_thread and speaking_thread.is_alive():
        stop_speaking()
    speaking_thread = threading.Thread(target=speak, args=(text,))
    speaking_thread.start()

# 🚦 Core commands
def stop_action():
    speak_async("Very well.")
    time.sleep(1)

def terminate_action():
    speak_async("Terminating program.")
    time.sleep(1)
    exit()

core_commands = {
    "cancel": stop_action,
    "terminate": terminate_action
}

# 🧠 Command mappings
command_map = [
    (lambda cmd: cmd.startswith("open"), open_application),
    (lambda cmd: cmd.startswith("close"), close_application),
    (lambda cmd: "lock" in cmd and "screen" in cmd, lock_screen),
    (lambda cmd: cmd.startswith("take"), take_screenshot),
    (lambda cmd: "volume" in cmd or "mute" in cmd or "unmute" in cmd, adjust_volume),
    (lambda cmd: "brightness" in cmd, adjust_brightness),
    (lambda cmd: "restart" in cmd or "reboot" in cmd, restart_system),
    (lambda cmd: "shutdown" in cmd, shutdown_system),
    (lambda cmd: cmd.startswith("search "), open_website),
    (lambda cmd: any(w in cmd for w in ["what", "who", "when", "where", "tell me", "how", "explain", "define", "formula", "convert", "current", "brief"]), web_query),

    # 🕒 Clock features
    (lambda cmd: "set an alarm" in cmd.lower() or "set alarm" in cmd.lower(), set_alarm),
    (lambda cmd: any(w in cmd.lower() for w in ["what time", "current time", "tell me the time", "time now"]), tell_time),
]

# 🎤 Capture single command
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

# 🚀 Main loop
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

                if "terminate" in wake_query:
                    terminate_action()
                    return

                if "nova" not in wake_query:
                    continue

                stop_speaking()
                print("🎹 Nova Active...")
                speak_async(random.choice(wake_responses))

                command = listen_for_command()
                if not command:
                    speak_async("I didn't catch that.")
                    continue

                if is_dismiss_command(command):
                    speak_async("Okaaay.")
                    continue

                core_match = next((a for k, a in core_commands.items() if k in command), None)
                if core_match:
                    core_match()
                    continue

                matched = False
                for cond, action in command_map:
                    if cond(command):
                        action(command)
                        matched = True
                        break

                if not matched:
                    speak_async("I'm not sure how to handle that.")

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"❌ Could not request results: {e}")

# ✅ Start Nova
if __name__ == "__main__":
    main()
