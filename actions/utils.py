import os
import uuid
import pygame
import threading
import speech_recognition as sr
from pathlib import Path
from google.cloud import texttospeech

# Set credentials
base_dir = Path(__file__).resolve().parent.parent
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(base_dir / "nova-va.json")

# TTS client setup
tts_client = texttospeech.TextToSpeechClient()
voice_params = texttospeech.VoiceSelectionParams(
    language_code="en-IN",
    name="en-IN-Chirp3-HD-Callirrhoe"
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Initialize mixer
pygame.mixer.init()

interrupted = False

def speak(text: str):
    global interrupted
    interrupted = False

    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )

    filename = f"nova-{uuid.uuid4()}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        if interrupted:
            pygame.mixer.music.stop()
            break
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(filename)


def stop_speaking():
    global interrupted
    interrupted = True


def is_dismiss_command(text: str) -> bool:
    if not text:
        return False
    dismiss_phrases = ["nevermind", "never mind", "nothing", "leave it", "forget it"]
    return any(phrase in text.lower() for phrase in dismiss_phrases)


def listen_for_command(timeout: int = 6):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("🎤 Listening for confirmation...")
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio).lower()
            return command
        except:
            return None
