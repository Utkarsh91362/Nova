import webbrowser
import re
import shutil
from actions.utils import speak

BROWSER_PATHS = {
    "chrome": shutil.which("chrome") or r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "brave": shutil.which("brave") or r"C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    "edge": shutil.which("msedge") or r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
}

def open_website(command: str):
    command = command.lower()

    # Extract platform (e.g., youtube, google)
    platform_match = re.search(r"search (.+?) on (youtube|google|chrome|brave|edge)", command)
    browser = None
    url = None

    if platform_match:
        query = platform_match.group(1).strip()
        target = platform_match.group(2)

        if target == "youtube":
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        elif target in BROWSER_PATHS:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            browser = BROWSER_PATHS[target]
    else:
        # Default Google search if no browser/platform mentioned
        generic_match = re.search(r"search (.+)", command)
        if generic_match:
            query = generic_match.group(1).strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    if url:
        speak("Searching now.")
        if browser:
            webbrowser.get(f'"{browser}" %s').open(url)
        else:
            webbrowser.open(url)
    else:
        speak("I couldn't understand what to search.")
