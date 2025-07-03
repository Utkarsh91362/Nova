import os
from datetime import datetime
from pathlib import Path
from PIL import ImageGrab
from actions.utils import speak

def take_screenshot(command: str):
    if not any(word in command for word in ["screenshot", "capture", "screen"]):
        return

    try:
        # Set screenshot path
        screenshots_dir = Path(__file__).resolve().parent.parent.parent / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Generate file name
        filename = datetime.now().strftime("screenshot-%Y%m%d-%H%M%S.png")
        filepath = screenshots_dir / filename

        # Capture and save
        image = ImageGrab.grab()
        image.save(filepath)

        speak(f"took screenshot")

    except Exception as e:
        print("❌ Screenshot error:", e)
        speak("I couldn't take the screenshot. Something went wrong.")
