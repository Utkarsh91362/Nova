import os
import uuid
import pygame
from pathlib import Path
from google.cloud import texttospeech

# Set absolute path to your service account key
base_dir = Path(__file__).resolve().parent.parent
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(base_dir / "nova-va.json")

# Initialize Google TTS client
tts_client = texttospeech.TextToSpeechClient()

# Voice settings
voice_params = texttospeech.VoiceSelectionParams(
    language_code="en-IN",
    name="en-IN-Chirp3-HD-Callirrhoe"
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Initialize pygame mixer
pygame.mixer.init()

def speak(text: str):
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
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()  # ✅ Unload the file
    os.remove(filename)          # ✅ Now it's safe to delete
