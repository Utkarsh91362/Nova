from googlesearch import search
import requests
from bs4 import BeautifulSoup
from actions.utils import speak
import re

def extract_best_fact(soup):
    # 1. Try formulas/code
    for tag in soup.find_all(["code", "pre", "tt"]):
        text = tag.get_text(strip=True)
        if text and any(char in text for char in "=√+-*/"):
            return text

    # 2. Try strong sentences with math symbols
    for para in soup.find_all("p"):
        text = para.get_text(strip=True)
        if len(text) > 30 and any(sym in text for sym in "=√+-*/") and text[-1] in ".!?":
            return text

    # 3. Fallback: return a short paragraph
    for para in soup.find_all("p"):
        text = para.get_text(strip=True)
        if len(text) > 50:
            return text.split(".")[0] + "."

    return None

def web_query(command: str):
    query = command.strip()

    try:
        results = list(search(query, num_results=1))
        if not results:
            speak(f"Sorry, I couldn't find anything about {query}.")
            return

        url = results[0]
        resp = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        fact = extract_best_fact(soup)

        if fact:
            speak(f"Here's what I found: {fact[:300]}")
        else:
            speak("I found a page, but couldn't extract a clear formula or summary.")
    except Exception as e:
        print("Web query error:", e)
        speak("Sorry, I ran into a problem fetching the info.")
