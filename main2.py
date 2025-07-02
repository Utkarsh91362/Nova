import speech_recognition as sr
import os
import uuid
import random
import pygame
from google.cloud import texttospeech

# Set Google credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "nova-va.json"

# Initialize Google TTS client
tts_client = texttospeech.TextToSpeechClient()

# Voice config
voice_params = texttospeech.VoiceSelectionParams(
    language_code="en-IN",
    name="en-IN-Chirp3-HD-Callirrhoe"
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Initialize pygame
pygame.mixer.init()

def speak(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
    
    filename = f"nova-{uuid.uuid4()}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.mixer.init()

    os.remove(filename)

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

# ✅ Main loop — continuous listening for 'nova' or 'shut down'
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Nova is on standBy...")

        while True:
            try:
                print(" Try waking Nova...")
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio).lower()
                print("Heard:", query)

                if "shut down" in query or "shutdown" in query:
                    speak("Powering off. Goodbye.")
                    break

                elif "nova" in query:
                    print("🎙️ Nova Active...")
                    speak(random.choice(wake_responses))

                    # Listen for actual command now
                    command = listen_for_command()
                    if command:
                        command = command.lower()
                        print("Command:", command)

                        if "stop" in command:
                            speak("Very Well")
                            continue  # goes back to waiting for wake word
                        elif "shut down" in command or "shutdown" in command:
                            speak("Powering off.")
                            break
                        else:
                            speak(f"You said: {command}")
                    else:
                        speak("I didn't catch that.")

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"❌ Could not request results: {e}")
