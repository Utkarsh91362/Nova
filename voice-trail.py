from google.cloud import texttospeech
import os

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "virtual-assistant-464710-09a9cb6ee73b.json"

# Create client
client = texttospeech.TextToSpeechClient()

# List all voices
voices = client.list_voices().voices

# Filter only en-IN (Indian English) voices
indian_voices = [v for v in voices if "en-IN" in v.language_codes]

print(f"🇮🇳 Total Indian English voices: {len(indian_voices)}\n")

# Sample text
sample_text = "Hello! I am Nova voice assistant."

# Get user's Music folder
music_folder = os.path.join(os.path.expanduser("~"), "Music", "NovaVoices")
os.makedirs(music_folder, exist_ok=True)

# Loop through and save
for voice in indian_voices:
    print(f"🔊 Synthesizing: {voice.name} ({texttospeech.SsmlVoiceGender(voice.ssml_gender).name})")

    synthesis_input = texttospeech.SynthesisInput(text=sample_text)

    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-IN",
        name=voice.name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )

    filename = os.path.join(music_folder, f"{voice.name}.mp3")
    with open(filename, "wb") as out:
        out.write(response.audio_content)

print(f"\n✅ All {len(indian_voices)} voices saved in your Music folder under 'NovaVoices'")
